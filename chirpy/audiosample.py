# Audio sampling
#
# Copyright (C) 2025 Simon Dobson
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

import pyaudio
import struct
import numpy as np


device = pyaudio.PyAudio()


def record(sampleTime, sampleRate = 44100):
    """Record a sample from the default audio device.

    @param sampleTime: the time in seconds to record
    @param sampleRate: (optional) the sample rate (defaults to 441009Hz)
    @returns: the signal as an array of floats"""

    chunkSize = 1024
    str = device.open(format=pyaudio.paFloat32,
                      channels=1,
                      rate=sampleRate,
                      frames_per_buffer=chunkSize,
                      input=True)

    # take the recording
    samples = sampleTime * sampleRate
    chunks = int(np.ceil(samples / chunkSize))
    buffer = np.ndarray(samples, dtype=np.float32)
    start = 0
    for k in range(chunks):
        end = min(start + chunkSize, samples)
        data = str.read(end - start)

        # unpack each 4-byte sample as a float32
        b = 0
        for i in range(end - start):
            f = struct.unpack(">f", data[b:b + 4])[0]
            buffer[start + i] = f
            b += 4

        start += chunkSize

    return buffer
