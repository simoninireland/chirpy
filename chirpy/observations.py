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


def makeObservation(mli, confidence):
    """Create an observation record.

    The record is suitable for transmitting as a JSON object and
    contains the following fields:

    timestamp: an ISO8601-format timestamp
    id: the BirdNET index for the bird observed
    confidence: the confidence score for the observation
    common: the cmmon name of the bird
    sci: the scientific name of the bird

    @param mli: the most likely index of the observed bird
    @param confidence: the confidence of this observation
    @returns: a dict
    """
    ts = datetime.now().isoformat()
    common, sci = chirpy.identify(mli)

    return {'timestamp': ts,
            'id': mli,
            'confidence': confidence,
            'common': common,
            'sci': sci}
