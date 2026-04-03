# Meshtastic event reporting
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
import json
import meshtastic
import meshtastic.tcp_interface


# Global Meshtastic device
meshtasticInterface: meshtastic.mesh_interface = None


def meshtasticConnect(host = "localhost"):
    """Connect to a local Meshtastic device."""
    global meshtasticInterface

    meshtasticInterface = meshtastic.tcp_interface.TCPInterface(host)
    chirpy.logger.info(f"Connected to Meshtastic network using device at {host}")


def meshtasticSendMessage(msg):
    """Report an a message on Meshtastic.

    The message can then be retrieved from any node on the mesh or (more
    likely) bridged to MQTT or a similar messaging platform.

    The message should be JSON encoded.

    @param message: the message
    """
    payload = json.dumps(msg)
    packet = meshtasticInterface.sendText(payload)
    chirpy.logger.debug(packet)
