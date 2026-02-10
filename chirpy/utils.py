# Some utility functions
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

from sys import stdin
import os.path
import json


def readJSON(str = stdin):
    """Read a single JSON record from str.

    The stream can contain multiple records, separated by blank lines.

    Returns None if the stream closes or a record fails to parse
    properly. (These two conditions are indistinguishable.)

    @param str: (optional) the stream (defaults to stdin
    @returns: a dict representing the parsed JSON record

    """

    # read a single blank-line-delimited record
    buf = ''
    while True:
        line = str.readline().strip()
        if(line == ''):
            break
        buf = buf + line

    # decode as JSON
    try:
        return json.loads(buf)
    except(json.decoder.JSONDecodeError):
        return None


def filenameForTimestamp(timestamp, dir = None):
    """Generate a filename for saving a sample captured at the given time.

    The filename is local unless dir is given, in which case it exists in
    that directory,

    @param timestamp: the sample timestamp
    @param dir: (optional) directory for filename"""

    # construct the basename
    ts = timestamp.timetuple()
    basename = f"{ts[0]:04d}-{ts[1]:02}-{ts[2]:02d}T{ts[3]:02d}-{ts[4]:02d}-{ts[5]:02d}.wav"

    # attach to directory if provided
    if dir is None:
        return basename
    else:
        return os.path.join(dir, basename)
