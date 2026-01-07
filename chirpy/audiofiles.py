# Audio file handling
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
# along with this software. If not, see <http://www.gnu.org/licenses/gpl.html>.

import soundfile as sf


def load(fn, sampleRate = None):
    """Load an audio file and return the signal.

    @param fn: the file name
    @param sampleRate: the sample rate in Hz (defaults to the file's own sample rate)
    @returns: the signal as an array and the actual sample rate"""
    sig, rate = sf.read(fn, samplerate=sampleRate)

    return sig, rate
