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
