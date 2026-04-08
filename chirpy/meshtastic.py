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
import meshtastic.serial_interface
from pubsub import pub


# Global Meshtastic device
meshtasticInterface: meshtastic.mesh_interface = None


def meshtasticConnect(host = None, port = None,
                      callback = None):
    """Connect to a Meshtastic device.

    This function should ebe called before any observations are reported.

    Neither host nor port needs to be specified. If both are provided,
    the port is used; if neither is provided, we use the globally-configured
    host if there is one, or the globally-configured port if not.

    The callback, if provided, should take ther received message as a
    parameter.

    @param host: (optional) the Meshtastic host
    @param port: (optional) the device serial port
    @param callback: (optional) callback for each message received

    """
    global meshtasticInterface

    # sort out the logic of the various connection options
    if host is None and port is None:
        host = chirpy.config.meshHost
        if host is None:
            port = chirpy.config.meshPort
    elif host is not None and port is not None:
        chirpy.logger.warn("Preferring the port specified for Meshtastic")
        host = None

    # connect to the mesh
    if host is None:
        meshtasticInterface = meshtastic.serial_interface.SerialInterface(port)
        chirpy.logger.info(f"Connected to Meshtastic network using device {port}")
    else:
        meshtasticInterface = meshtastic.tcp_interface.TCPInterface(host)
        chirpy.logger.info(f"Connected to Meshtastic network using device at {host}")

    # install callback if provided
    if callback is not None:
        # define the Meshtastic-level callback to call the chirpy-level callback
        def onReceive(packet, interface):
            # parse the message
            message = json.loads(packet)
            payload = message.get("payload", None)
            if payload is not None:
                # check that the payload is of a type we recognise
                if chirpy.isObservation(payload):
                    # yes, call the callback
                    callback(payload)
                else:
                    chirpy.logger.debug("Dropped non-chirpy message")

        # subscribe the the message channel
        pub.subscribe(onReceive, "meshtastic.receive")


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
