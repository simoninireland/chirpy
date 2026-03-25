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
import meshtastic
import meshtastic.tcp_interface
from pubsub import pub


# Global Meshtastic device
meshtasticInterface: meshtastic.mesh_interface = None


def onConnect(interface, topic = pub.AUTO_TOPIC):
    """Meshtastic device connection."""
    chirpy.logger.debug("Connected to Meshtastic device")


def meshtasticConnect(host = "localhost"):
    """Connect to a local Meshtastic device."""
    meshtasticInterface = meshtastic.tcp_interface.TCPInterface(host)
    chirpy.logger.info(f"Connected to Meshtastic network using device at {host}")


def meshtasticSendMesage(msg, topic):
     """Report an a message on Meshtastic against the given topic.

    The message should be JSON encoded.

    @param message: the message
    @param topic: topic to report against
    """
    payload = json.dumps(msg)
    pub.sendMessage(topic, payload=payload)
