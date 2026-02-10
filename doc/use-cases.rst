Use cases
=========

Here are some common use cases for the ``chirpy`` shell scripts.


On-device classification
------------------------

Local audio sampling and classification, reporting observations by
MQTT to a remote broker.

.. code:: shell

   chirpy-sample | chirpy-classify | chirpy-mqtt-reporter


Centralised logging
-------------------

A logger taking observation records from MQTT and saving them into a
local database,

.. code:: shell

   chirpy-mqtt-logger


Long-term unattended capture
----------------------------

An audio sampler and classification that stops running at night.

.. code:: shell

   chirpy-sample --nighttime | chirpy-classify | chirpy-mqtt-reporter


The significance of this is that pausing sampling automatically
pauses the rest of the pipeline, which in turn reduces power
consumption from its level during inference to its idle level, which
can result in considerable power savings.
