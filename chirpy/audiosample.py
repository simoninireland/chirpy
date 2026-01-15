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

import sounddevice as sd
import numpy as np


chunkSize = 1024
sampleRate = 48000


def record(sampleTime):
    """Record a sample from the default audio device.

    @param sampleTime: the time in seconds to record
    @returns: the signal as an array of floats, and the sample rate"""
    samples = sampleTime * sampleRate

    sig = sd.rec(samples,
                 samplerate=sampleRate,
                 channels=1,
                 dtype=np.float32)
    sd.wait()

    # convert the signal to a flat array of values, rather than an
    # array of lists of per-channel values
    sig = np.ravel(sig, order='C')

    return sig, sampleRate
