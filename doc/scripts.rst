Shell scripts
=============

``chirpy-sample``
-----------------

This script samples audio from the default sound input device --
typically there will be only one on a sensor -- and outputs it as a
JSON sample object holding the timestamped sample. Sampling continues
indefinitely by default, but this can be changed using the following
options.

+-------------------+-------------------------------+----------------+
| Option            | Description                   | Default        |
+===================+===============================+================+
| ``--nighttime``   | Pause sampling at night       | False          |
| ``-n``            |                               |                |
+-------------------+-------------------------------+----------------+
| ``--samples`` <n> | Take n samples before exiting | Unbounded      |
| ``-N`` <n>        |                               |                |
+-------------------+-------------------------------+----------------+

The duration of each sample is set by the ``sampleDuration``
configuration variable. Night-time is defined by the local sunset and
sunrise times, offset by the value of the ``nighttimeOffset``
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

``chirpy-mqtt``
---------------

This script bridges ``chirpy``'s shall pipelines to and from an MQTT
message broker. The script works in three different ways:

- sending messages to a topic;
- accepting messages from a topic; and
- passing messages between topics.

The MQTT connection is set by the ``mqttHost``, ``mqttUsername``, and
``mqttPassword`` configuration values. Thetopics are set using
command-line options.

+--------------------+-------------------------------+----------------+
| Option             | Description                   | Default        |
+====================+===============================+================+
| ``--from`` <topic> | Topic to take messages from   | ``sys.stdin``  |
| ``-f`` <topic>     |                               |                |
+--------------------+-------------------------------+----------------+
| ``--to`` <topic>   | Topic to send messages to     | ``sys.stdout`` |
| ``-t`` <topic>     |                               |                |
+--------------------+-------------------------------+----------------+

By default the script takes messages from standard input and sends
them to standard output, either of which can be re-directed to a
topic. The messages sent must be JSON-encoded.

``chirpy-logger``
-----------------

This script reads observations stores them in an SQLite database. (See
:doc:`db-schema` for the SQL schema used.) Storage happens as long as
new observations are reported.

The ``sqlitedb`` configuration value specifies the filename for the
SQLite database. This will be created if it doesn't exist.

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
