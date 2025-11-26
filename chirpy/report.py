# MQTT event reporting
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

import paho.mqtt.client as mqtt
import config


# Connect to the MQTT broker
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(config.mqtt_username, config.mqtt_password)
client.connect(config.mqtt_host)
client.loop_start()


def report(payload, topic = None):
    """Report the payload to the MQTT server under the desired topic.

    @param payload: the message
    @param topic: (optional) topic to report against (defaults to configured mqtt_topic)
    """
    if topic is None:
        topic = config.mqtt_topic

    client.publish(topic, payload)
