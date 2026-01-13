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

import chirpy
import paho.mqtt.client as mqtt
import json
import config
from copy import copy
from typing import Hashable, Callable


# Global MQTT client connection
mqttClient: mqtt.Client = None
mqttTopics: dict[str, Callable[[str], None]] = None


def onConnect(client, userData, flags, reason_code, properties):
    """MQTT callback on connection.

    This subscribes the client to all the topics requested.
    """
    global mqttClient, mqttTopics

    for topic in mqttTopics.keys():
        mqttClient.subscribe(topic)
        print(f"Subscribed to {topic}")


def onMessage(client, userData, message):
    """MQTT callback for each message.

    This calls the user-supplied callbacks, so the user code can work
    in terms of observations rather than strings.
    """
    topic, payload = message.topic, message.payload
    callback = mqttTopics.get(topic, None)
    if callback is None:
        print("Received an unexpected message...")
    else:
        observation = json.loads(payload)
        callback(observation)


def mqttConnect(host = None, username = None, password = None, topics = None):
    """Connect to an MQTT broker.

    This function should be called before any observations are reported.

    The parameters are all optional, and are picked up from the global
    configuration if omitted, with no topic subscriptions or callbacks
    by default. A topic callback should take the payload as a
    parameter

    @param host: (optional) the MQTT broker
    @param username: (optional) the MQTT username
    @param password: (optional) the MQTT password
    @param topics: (optional) dict or list of pairs of topics and callbacks to subscribe to (defaults to none)
    """
    global mqttClient, mqttTopics

    if host is None:
        host = config.mqtt_host
    if username is None:
        username = config.mqtt_username
    if password is None:
        password = config.mqtt_password

    mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttClient.username_pw_set(username, password)
    if topics is not None:
        if isinstance(topics, dict):
            print("grabbed hash table")
            mqttTopics = copy(topics)
        else:
            mqttTopics = dict()
            for tc in topics:
                topic, callback = tc[0], tc[1]
                mqttTopics[topic] = callback
        mqttClient.on_connect = onConnect
        mqttClient.on_message = onMessage
    mqttClient.connect(host)
    print(f"Connected to MQTT broker at {host}")
    mqttClient.loop_start()


def mqttReportObservation(observation, topic = None):
    """Report an observation on MQTT against the given topic.

    @param observation: the observation
    @param topic: (optional) topic to report against (defaults to configured mqtt_topic)
    """
    if topic is None:
        topic = config.mqtt_topic

    payload = json.dumps(observation)
    mqttClient.publish(topic, payload)
