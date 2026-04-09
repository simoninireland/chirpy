.. _use-cases:

Use cases
=========

Here are some common use cases for the ``chirpy`` :ref:`shell scripts <scripts>`.


.. _on-device-use-case:

On-device classification with local logging
-------------------------------------------

Local audio sampling and classification, storing observations in a
local database.

.. code:: shell

   chirpy-sample | chirpy-classify | chirpy-logger


.. _mqtt-client-use-case:

On-device classification send observations to MQTT
--------------------------------------------------

Local audio sampling and classification, with observations being sent
to an MQTT topic.

.. code:: shell

   chirpy-sample | chirpy-classify | chirpy-mqtt --to "chirpy.bird"


.. _mqtt-server-use-case:

Centralised storage populated from MQTT
---------------------------------------

A logger taking observation records from MQTT and saving them into a
local database,

.. code:: shell

   chirpy-mqtt --from "chirpy.bird" | chirpy-logger


Local *and* centralised storage
-------------------------------

We might want to combine both local storage and reporting to a
centralised database, for robustness in case messages get lost in
flight. To do this we need to modify our pipeline so that we take a
copy of all messages being sent over the network and store them
locally.

We can do this by using a couple of Linux tools:

- ``tee``, that sends data to a file as well as passing it along the
  pipeline; and
- ``mkfifo``, that creates a file that's actually a first-in/first-out
  pipe (a FIFO).

The trick is to capture the messages into a FIFO and use that to feed
another pipeline.

.. code:: shell

   # create the FIFO
   mkfifo /tmp/chirpyfifo

   # run the classifier/reporting pipeline, capturing to the FIFO
   chirpy-sample | chirpy-classify | tee /tmp/chirpyfifo | chirpy-mqtt --to "chirpy.bird" &

   # use the data coming down the FIFO for the local logger
   cat /tmp/chirpyfifo | chirpy-logger


.. _mesh-client-use-case:

On-device classification shared over Meshtastic
-----------------------------------------------

A classifier sends its observations to Meshtastic *via* a local radio.

.. code:: shell

   chirpy-sample | chirpy-classify | chirpy-mesh


Some Meshtastic nodes connect to their radio over a serial port.
Typically this will be ``/dev/ttyACM0`` on Linux (or sometimes
``/dev/ttyUSB0``). In this case we need to connect over this port.

.. code:: shell

   chirpy-sample | chirpy-classify | chirpy-mesh --port /dev/ttyACM0


.. _mesh-server-mqtt-use-case:

Centralised storage populated from Meshtastic *via* MQTT
--------------------------------------------------------

The Meshtastic firmware can automatically pass messages to MQTT, which
is very useful. However, the topics for these messages are largely
fixed, and their format includes a lot of additional Meshtastic
information and not just the message we want to send. To deal with
this we can subscribe to an MQTT **wildcard** topic that picks up
messages sent from the mesh, and disencapsulate the received messages
to extract only the ``chirpy``-relevant payload.

.. code:: shell

   chirpy-mqtt --from 'chirpy/#' --disencapsulate 'payload' | chirpy-logger

The topic ending in # is an MQTT wildcard that matches *all* topics
starting with "chirpy/". If we use this as the "root topic" from
Meshtastic, then this will pick up all messages sent from the mesh
[1]_.

The ``disencapsulate`` option extracts the field named "payload" from
the message, discarding all the extra Meshtastic information (which
may be useful in itself in some applications).


Long-term unattended capture
----------------------------

An audio sampler with local storage that stops running at night.

.. code:: shell

   chirpy-sample --nighttime | chirpy-classify | chirpy-logger


The significance of this is that pausing sampling automatically
pauses the rest of the pipeline, which in turn reduces power
consumption from its level during inference to its idle level, which
can result in considerable power savings. One could of course replace
local logging with messaging.


.. rubric:: Footnotes

.. [1] You may see errors relating to undecodeable JSON in the logs.
       This is because the wildcard is slightly *too* wild, and
       captures plain-text as well as JSON versions of the message.
       To fix this, use a narrower wildcard such as "chirpy/2/json/#".
       This captures all messages sent to the "chirpy" root topic that
       use version 2 of the Meshtastic protocol and are JSON-encoded.
