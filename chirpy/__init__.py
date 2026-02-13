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

from .config import *
import os
import logging

# update configuration variables from the environment where defined
# -- node identification and location
config.nodeIdentifier = os.getenv("CHIRPY_NODE", config.nodeIdentifier)
config.nodeLatitude = os.getenv("CHIRPY_NODE_LAT", config.nodeLatitude)
config.nodeLongitude = os.getenv("CHIRPY_NODE_LON", config.nodeLongitude)

# -- MQTT
config.mqttHost = os.getenv("CHIRPY_MQTT_HOST", config.mqttHost)
config.mqttUsername = os.getenv("CHIRPY_MQTT_USERNAME", config.mqttUsername)
config.mqttPassword = os.getenv("CHIRPY_MQTT_PASSWORD", config.mqttPassword)

# -- logging
try:
    config.logLevel =  eval(os.getenv("CHIRPY_LOG_LEVEL", "config.logLevel"))
except Exception:
    pass

# -- SQLite database
config.sqlitedb = os.getenv("CHIRPY_SQLITE_DB", config.sqlitedb)

# configure the system logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=config.logLevel)


from . import logger
from .utils import readJSON, filenameForTimestamp
from .audiofiles import load
from .audiosample import record, makeSample, printSample
from .classify import loadModel, loadLabels, segment, classify, mostLikelyIndex, identify, getLabelsMapping
from .observations import makeObservation, printObservation
from .mqtt import mqttConnect, mqttSendMessage
from .db import dbOpenConnection, dbRecordObservation, dbAllObservationsOf, dbAllObservationsBetween, dbCountObservationsBetween
