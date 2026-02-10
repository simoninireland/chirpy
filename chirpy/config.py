# Configuration variables
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

# ---------- Node identifier ----------

nodeIdentifier = "chirpy"
nodeLatitude = 56.33404
nodeLongitude = -2.79955


# ---------- MQTT broker ----------

mqttHost = None
mqttUsername = None
mqttPassword = None


# ---------- MQTT topics ----------

mqttTopic = {'observation': 'chirpy.bird',
             'coreTemperature': 'chirpy.coretemp',
             }


# ---------- SQLite database ----------

sqlitedb = "chirpy.db"


# ---------- System tuning ----------

import logging

logLevel = logging.INFO
sampleDuration = 5
confidenceThreshold = 0.2
nighttimeOffset = 60
