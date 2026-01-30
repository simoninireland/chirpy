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

``chirpy-spotter``
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
