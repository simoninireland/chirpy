Networking
==========

Connecting sensors to base almost always requires networking. There
are several possible ways to make these connections (sometimes
referred to as the **backhaul**), and ``chirpy`` supports several
common approaches.

Local sensor
------------

The simplest case involves a sensor on the same platform as the rest
of the processing. In this case the results of a ``chirpy`` pipeline
can be processed directly using shell pipelines and tools. See the
:ref:`on-device-use-case` use case for an example.

.. _mqtt-networking:

Using MQTT
----------

`MQTT`_ is the most common messaging framework used for communication
in the Internet of Things. It provides a `publish and subscribe`_
pattern whereby devices publish messages to **topics** that can be
subscribed to by other devices or services. Messages are freeform but
typically use JSON.

A typical set-up is for an application to provide a single MQTT
**broker** that is used by all its component devices and services.
This server, and the devices and services, can in principle be located
anywhere on the internet. This allows for very flexible messaging.

``chirpy`` pipelines can be interfaced to MQTT using the
``chirpy-mqtt`` script. This needs to be provided with the address and
credentials of the MQTT broker, which can be set in the global
configuration (see :ref:`mqtt-config`). The script can pass ``chirpy`` messages
to MQTT for onward transmission (see the :ref:`mqtt-client-use-case`
use case), or retrieve messages from MQTT for processing and storage
(see the :ref:`mqtt-server-use-case` use case).

Using Meshtastic
----------------

`Meshtastic`_ is a **mesh network**. It sits on top of `LoRa`_, a radio
protocol used for applications that need to run off-grid with long
range and low power in the absence of the sorts of infrastructure
needed for wifi or cellular communication.

As a mesh network, all Meshtastic **nodes** co-operate to transmit
messages across the mesh. Any new nodes that are in radio range of one
or more others will join the mesh, so extending range is very
straightforward: just add nodes to the edge.

Nodes are intended to be part of the Internet of Things, so the
firmware of each Meshtastic device can be instructed to forward
messages to an MQTT server automatically -- assuming the node has a
connection to the internet, of course. Only one node typically needs
to have this feature enabled, and will typically be a "gateway" base
station that forwards messages from the mesh to the wider internet.

``chirpy`` can interact with Meshtastic in two ways. The
``chirpy-mesh`` script acts like ``chirpy-mqtt`` in forwarding message
to the mesh or retrieving them for processing. Alternatively, if there
is a node in the mesh forwarding to MQTT, ``chirpy-mqtt`` can be used
as detailed above to extract the forwarded messages directly from the
MQTT broker.


.. _MQTT: https://en.wikipedia.org/wiki/MQTT

.. _publish and subscribe: https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern

.. _Meshtastic: https://meshtastic.org/

.. _LoRa: https://en.wikipedia.org/wiki/LoRa
