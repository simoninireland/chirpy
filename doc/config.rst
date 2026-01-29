Configuration values
====================

``chirpy`` can be configured using the following values.


System tuning
-------------

These values tune various aspects of ``chirpy``. They all have sensible defaults.

+-------------------------+--------------------+---------------------------------------+
| Variable                | Default            | Description                           |
+=========================+====================+=======================================+
| ``logLevel``            | ``logging.INFO``   | Log level                             |
+-------------------------+--------------------+---------------------------------------+
| ``sampleDuration``      | 5                  | Length of each acoustic sample (s)    |
+-------------------------+--------------------+---------------------------------------+
| ``confidenceThreshold`` | 0.2                | Minimal confidence for an             |
|                         |                    | observation to be reported            |
+-------------------------+--------------------+---------------------------------------+

MQTT broker
-----------

These values are used only when reporting observations *via* an MQTT broker.

+-------------------+------------------+---------------------------------------+
| Variable          | Default          | Description                           |
+===================+==================+=======================================+
| ``mqttClient``    | ``"chirpy"``     | Client identification (not essential) |
+-------------------+------------------+---------------------------------------+
| ``mqttHost``      | ``None``         | MQTT broker hostname or IP address    |
+-------------------+------------------+---------------------------------------+
| ``mqttUsername``  | ``None``         | MQTT username                         |
+-------------------+------------------+---------------------------------------+
| ``mqttPassword``  | ``None``         | MQTT password                         |
+-------------------+------------------+---------------------------------------+

SQLite database
---------------

These variables set up the SQLite database used for storing observations.

+-------------------+------------------+---------------------------------------+
| Variable          | Default          | Description                           |
+===================+==================+=======================================+
| ``sqlitedb``      | ``chirpy.db``    | File name for SQLite database         |
+-------------------+------------------+---------------------------------------+
