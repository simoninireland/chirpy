# Audio sampling
#
# Copyright (C) 2025--2026 Simon Dobson
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License

from pyaudio import PyAudio, paFloat32
import os
import struct
import numpy as np


# Silencing the junk that PyAudio emits when it starts
# See https://stackoverflow.com/questions/67765911/how-do-i-silence-pyaudios-noisy-output

class pyaudio:
    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]

        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

        self.pyaudio = None


    def __enter__(self) -> PyAudio:
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

        self.pyaudio = PyAudio()

        return self.pyaudio


    def __exit__(self, *_):
        # We leave audio running when we exit the context manager
        #self.pyaudio.terminate()

        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)

        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)


# Audio device access
device : PyAudio = None
with pyaudio() as silenced:
    device = silenced

chunkSize = 1024
sampleRate = 44100
stream = device.open(format=paFloat32,
                     channels=1,
                     rate=sampleRate,
                     frames_per_buffer=chunkSize,
                     input=True)


def record(sampleTime):
    """Record a sample from the default audio device.

    @param sampleTime: the time in seconds to record
    @returns: the signal as an array of floats"""
    samples = sampleTime * sampleRate
    chunks = int(np.ceil(samples / chunkSize))
    buffer = np.ndarray(samples, dtype=np.float32)
    start = 0
    for _ in range(chunks):
        end = min(start + chunkSize, samples)
        data = stream.read(end - start)

        # unpack each 4-byte sample as a float32
        b = 0
        for i in range(end - start):
            f = struct.unpack(">f", data[b:b + 4])[0]
            buffer[start + i] = f
            b += 4

        start += chunkSize

    return buffer
