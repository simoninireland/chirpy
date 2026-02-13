Use cases
=========

Here are some common use cases for the ``chirpy`` shell scripts.


On-device classification with local logging
-------------------------------------------

Local audio sampling and classification, storing observations in a
local database.

.. code:: shell

   chirpy-sample | chirpy-classify | chirpy-logger


On-device classification send observations to MQTT
--------------------------------------------------

Local audio sampling and classification, with observations being sent
to an MQTT topic.

.. code:: shell

   chirpy-sample | chirpy-classify | chirpy-mqtt --to "chirpy.bird"


Centralised storage populated from MQTT
---------------------------------------

A logger taking observation records from MQTT and saving them into a
local database,

.. code:: shell

   chirpy-mqtt --from "chirpy.bird" | chirpy-logger


Long-term unattended capture
----------------------------

An audio sampler with local storage that stops running at night.

.. code:: shell

   chirpy-sample --nighttime | chirpy-classify | chirpy-logger


The significance of this is that pausing sampling automatically
pauses the rest of the pipeline, which in turn reduces power
consumption from its level during inference to its idle level, which
can result in considerable power savings. One could of course replace
local logging with MQTT messaging.
