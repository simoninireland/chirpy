Configuration values
====================

``chirpy`` can be configured in several ways:

- Most values have sensible defaults where possible
- Scripts take command-line options that can set some configuration
  values
- The values can be set programmatically by accessing variables in
  ``chirpy.config``
- Some values can also be set from a program's environment by setting
  corresponding environment variables.

Node identification
-------------------

+--------------------+------------------+----------------------------------------+--------------------------+
| Variable           | Default          | Description                            | Environment variable     |
+====================+==================+========================================+==========================+
| ``nodeIdentifier`` | "chirpy"         | Node identification string, needed for | ``CHIRPY_NODE``          |
|                    |                  | systems with several sensors           |                          |
+--------------------+------------------+----------------------------------------+--------------------------+
| ``nodeLatitude``   | 56.33404         | Node latitude                          | ``CHIRPY_NODE_LAT``      |
+--------------------+------------------+----------------------------------------+--------------------------+
| ``nodeLongitude``  | -2.79955         | Node longitude                         | ``CHIRPY_NODE_LON``      |
+--------------------+------------------+----------------------------------------+--------------------------+

The node identifier will be passed in all JSON objects within
``chirpy``, allowing the source of observations to be determined.

The latitude and longitude are used when computing sunrise and sunset
times (for avoiding sampling at night), and defaults to `St Andrews`_.
There's no need to be too precise about these values: within a degree
will be enough to enable the functionality.

System tuning
-------------

These tuning values all have sensible defaults.

+-------------------------+--------------------+---------------------------------------+----------------------+
| Variable                | Default            | Description                           | Environment variable |
+=========================+====================+=======================================+======================+
| ``logLevel``            | ``logging.INFO``   | Log level                             | ``CHIRPY_LOG_LEVEL`` |
+-------------------------+--------------------+---------------------------------------+----------------------+
| ``sampleDuration``      | 5                  | Length of each acoustic sample (s)    |                      |
+-------------------------+--------------------+---------------------------------------+----------------------+
| ``confidenceThreshold`` | 0.2                | Minimal confidence for an             |                      |
|                         |                    | observation to be reported            |                      |
+-------------------------+--------------------+---------------------------------------+----------------------+
| ``nighttimeOffset``     | 60                 | Time in minutes from sunrise/sunset   |                      |
|                         |                    | considered to be night-time           |                      |
+-------------------------+--------------------+---------------------------------------+----------------------+

The ``CHIRPY_LOG_LEVEL`` value can be a number or an expression. It is
evaluated in an environment where the ``logging`` module is imported,
so a value such as "logging.CRITICAL" will set the logging level to
``logging.CRITICAL``.

MQTT broker
-----------

These values are used only when reporting observations *via* an MQTT broker.

+-------------------+------------------+---------------------------------------+--------------------------+
| Variable          | Default          | Description                           | Environment variable     |
+===================+==================+=======================================+==========================+
| ``mqttHost``      | None             | MQTT broker hostname or IP address    | ``CHIRPY_MQTT_HOST``     |
+-------------------+------------------+---------------------------------------+--------------------------+
| ``mqttUsername``  | None             | MQTT username                         | ``CHIRPY_MQTT_USERNAME`` |
+-------------------+------------------+---------------------------------------+--------------------------+
| ``mqttPassword``  | None             | MQTT password                         | ``CHIRPY_MQTT_PASSWORD`` |
+-------------------+------------------+---------------------------------------+--------------------------+

SQLite database
---------------

These variables set up the SQLite database used for storing observations.

+-------------------+------------------+---------------------------------------+----------------------+
| Variable          | Default          | Description                           | Environment variable |
+===================+==================+=======================================+======================+
| ``sqlitedb``      | ``chirpy.db``    | File name for SQLite database         | ``CHIRPY_SQLITE_DB`` |
+-------------------+------------------+---------------------------------------+----------------------+


.. _St Andrews: https://en.wikipedia.org/wiki/St_Andrews
