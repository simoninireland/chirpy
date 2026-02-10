Shell scripts
=============

``chirpy-sample``
-----------------

This script samples audio from the default sound input device --
typically there will be only one on a sensor -- and outputs it as a
JSON sample object holding the timestamped sample. Sampling continues
indefinitely.

The duration of a sample is set by the ``sampleDuration``
configuration variable.

``chirpy-classify``
------------------

This script accepts a JSON-encoded sample and runs it through the
classification model. If an observation is made, it outputs a JSON
object observation holding the timestamp, class identifier, confidence
value, common and scientific names of the bird. Spotting continues as
long as there are samples presented.

Some classes of sound are recognised and ignored, notably human
speech. Classifications with confidence falling below the value of the
``confidenceThreshold`` configuration value are ignored.

``chirpy-mqtt-reporter``
------------------------

This script accepts a JSON-encoded observation and transmits is by
MQTT to a broker. Reporting continues as long a there are observations
being sent.

The MQTT connection is set by the ``mqttHost``, ``mqttUsername``, and
``mqttPassword`` configuration values. The ``mqttTopic`` value
specifies what topic observations are sent to.

``chirpy-mqtt-logger``
----------------------

This script reads observations from the MQTT broker and stores them in
an SQLite database. (See :doc:`db-schema` for the SQL schema
used.)Storage happens as long as new observations are reported.

In addition to the MQTT configuration values, the ``sqlitedb`` value
specifies the filename for the SQLite database. This will be created
if it doesn't exist.

``chirpy-list``
---------------

This script returns a list of observations from the database.

The defaults are to print a human-readable list of timestamp and
common species name for all observations between start-of-day and now.
This can be change using the following command-line options.

+-------------------+-------------------------------+----------------+
| Option            | Description                   | Default        |
+===================+===============================+================+
| ``--from`` <time> | Start time for observations   | Start of today |
| ``-f`` <time>     |                               |                |
+-------------------+-------------------------------+----------------+
| ``--to`` <time>   | End time for observations     | Now            |
| ``-t`` <time>     |                               |                |
+-------------------+-------------------------------+----------------+
| ``--csv``         | Output observations as CSV    | False          |
| ``-c``            |                               |                |
+-------------------+-------------------------------+----------------+
| ``--number``      | Output counts of species      | False          |
| ``-n``            |                               |                |
+-------------------+-------------------------------+----------------+

The start and end times accept strings in any format accepted by the
`dateutil`_ package, for example "10:33" to a time today or "9 feb"
for a specific date.


.. _dateutil: https://dateutil.readthedocs.io/en/stable/
