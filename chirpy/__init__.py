# Package file for chirpy, the St Andrews bird counting sensor suite
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

import config

# configure the system logger
import logging
logger = logging.getLogger(__name__)
logLevel = logging.INFO
try:
    logLevel = int(config.logLevel)
except(ValueError):
    try:
        logLevel = eval(config.logLevel)
    except(RuntimeError):
        logger.error(f"Can't set logging level to {config.logLevel}, using {logLevel}")
logging.basicConfig(level=logLevel)


from . import logger
from .audiofiles import load
from .audiosample import record, makeSample, printSample
from .classify import loadModel, loadLabels, segment, classify, mostLikelyIndex, identify, getLabelsMapping
from .observations import makeObservation, printObservation
from .mqtt import mqttConnect, mqttReportObservation
from .db import dbOpenConnection, dbRecordObservation, dbAllObservationsOf, dbAllObservationsBetween
