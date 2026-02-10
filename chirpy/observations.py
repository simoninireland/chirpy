# chirpy observations
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
# along with this software. If not, see <http://www.gnu.org/licenses/gpl.html>.

import chirpy
from datetime import datetime
from sys import stdout
import json


def makeObservation(timestamp, mli, confidence, node):
    """Create an observation record.

    The record is suitable for transmitting as a JSON object and
    contains the following fields:

    type: the object type ("observation")
    timestamp: an ISO8601-format timestamp
    id: the BirdNET index for the bird observed
    confidence: the confidence score for the observation
    common: the common name of the bird
    sci: the scientific name of the bird

    @param timestamp: the timestamp for the observation we classified
    @param mli: the most likely index of the observed bird
    @param confidence: the confidence of this observation
    @param node: identifier of node making the observation
    @returns: a dict
    """
    common, sci = chirpy.identify(mli)

    return {'type': 'observation',
            'timestamp': timestamp,
            'nodeIdentifier': node,
            'id': int(mli),
            'confidence': float(confidence),
            'common': common,
            'sci': sci}


def printObservation(timestamp, mli, confidence, node, str = stdout):
    """Output an observation as a standard JSON record to str.

    @param timestamp: the timestamp for the observation we classified
    @param mli: the most likely index of the observed bird
    @param confidence: the confidence of this observation
    @param node: identifier of node making the observation
    @param str: (optional) the stream (defaults to stdout)
    """
    observation = makeObservation(timestamp, mli, confidence, node)
    print(json.dumps(observation), file=str)
    print(file=str)
    str.flush()
