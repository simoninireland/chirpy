.. _scripts:

Shell scripts
=============

The shell scripts are a convenient way to interact with ``chirpy``.
They are intended to be pipelined together to provide a complete
sampling, classification, reporting, and storage pipeline, with
optional networking components. See :ref:`use-cases` for examples of
common scenarios.

Below we provide brief descriptiosn of the tools and their
command-line options. Where applicable we relate the options to
configuration variables that can be set in the tools' environment. See
:ref:`config` for more details of the configuration possibilities.

``chirpy-sample``
-----------------

This script samples audio from the default sound input device --
typically there will be only one on a sensor -- and outputs it as a
JSON sample object holding the timestamped sample. Sampling continues
indefinitely by default, but this can be changed using the following
options.

+---------------------+-------------------------------+----------------+
| Option              | Description                   | Default        |
+=====================+===============================+================+
| - ``--nighttime``   | Pause sampling at night       | False          |
| - ``-p``            |                               |                |
+---------------------+-------------------------------+----------------+
| - ``--samples`` <n> | Take n samples before exiting | Unbounded      |
| - ``-n`` <n>        |                               |                |
+---------------------+-------------------------------+----------------+

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

This script bridges ``chirpy``'s shell pipelines to and from an MQTT
message broker. The script works in three different ways:

- sending messages to a topic;
- accepting messages from a topic; and
- passing messages between topics.

The MQTT connection is set by the ``mqttHost``, ``mqttUsername``, and
``mqttPassword`` configuration values. The topics are set using
command-line options.

+--------------------------------+---------------------------------+----------------+
| Option                         | Description                     | Default        |
+================================+=================================+================+
| - ``--from`` <topic>           | Topic to take messages from     | ``sys.stdin``  |
| - ``-f`` <topic>               |                                 |                |
+--------------------------------+---------------------------------+----------------+
| - ``--to`` <topic>             | Topic to send messages to       | ``sys.stdout`` |
| - ``-t`` <topic>               |                                 |                |
+--------------------------------+---------------------------------+----------------+
| - ``--disencapsulate`` <field> | Extract message payload         |                |
| - ``-d`` <field>               |                                 |                |
+--------------------------------+---------------------------------+----------------+
| - ``--all``                    | Pass all messages               | False          |
| - ``-a``                       |                                 |                |
+--------------------------------+---------------------------------+----------------+
| - ``--roottopic``              | Subscribe to messages from      |                |
| - ``-r``                       | Meshtastic with this root topic |                |
+--------------------------------+---------------------------------+----------------+

By default the script takes messages from standard input and sends
them to standard output, either of which can be re-directed to a
topic. The messages sent must be JSON-encoded.

By default the whole message is passed. However, in some systems the
incoming message is actually encapsulated as the payload in a larger
message. (This happens in Meshtastic, for example.) To deal with the,
the ``--disencapsulate`` option will extract he field carrying the
actual message we're interested in (the payload) from the larger
message and forward that. This saves other tools from being able to
process larger message formats.

The ``--all`` flag causes the script to pass all messages it receives.
Without this flag, it only passes messages that are recognises by
``chirpy``.

One can integrate MQTT with Meshtastic to retrieve observations from a
mesh (see :ref:`mesh-networking`). To simplify this integration, the
``--roottopic`` option takes the root topic set at the Meshtastic node
that is reporting messages to MQTT. It subscribes to the appropriate
reporting topic and sets the disencapsulation to extract the message
payload [1]_.

``chirpy-mesh``
---------------

This script bridges ``chirpy``'s shell pipelines to a Meshtastic
network for transmission over LoRa radios. The script has two modes:

- injecting messages to a Meshtastic mesh *via* a device; and
- taking messages from the mesh and placing them into a pipeline.

By default the script reads messages from its standard input and sends
them to Meshtastic on the specified channel. Alternatively, the script
will read messages *from* the Meshtastic channel and place their
payloads on standard output, having removed disencapsulated the
payload from the Meshtastic message frame. Usually only
``chirpy``-recognised messages are output, although this can be
changed to all messages for debugging purposes.

+----------------------+-------------------------------+----------------------+
| Option               | Description                   | Default              |
+======================+===============================+======================+
| - ``--channel`` <ch> | Meshtastic channel            | 0                    |
| - ``-c`` <ch>        |                               |                      |
+----------------------+-------------------------------+----------------------+
| - ``--host`` <host>  | Meshtastic device hostname    | ``CHIRPY_MESH_HOST`` |
| - ``-H`` <host>      |                               |                      |
+----------------------+-------------------------------+----------------------+
| - ``--port`` <port>  | Meshtastic device serial port | ``CHIRPY_MESH_PORT`` |
| - ``-P`` <port>      |                               |                      |
+----------------------+-------------------------------+----------------------+
| - ``--from``         | Take messages from Meshtastic | False                |
| - ``-f``             |                               |                      |
+----------------------+-------------------------------+----------------------+
| - ``--all``          | Take all messages             | False                |
| - ``-a``             |                               |                      |
+----------------------+-------------------------------+----------------------+

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

+---------------------+-------------------------------+----------------+
| Option              | Description                   | Default        |
+=====================+===============================+================+
| - ``--from`` <time> | Start time for observations   | Start of today |
| - ``-f`` <time>     |                               |                |
+---------------------+-------------------------------+----------------+
| - ``--to`` <time>   | End time for observations     | Now            |
| - ``-t`` <time>     |                               |                |
+---------------------+-------------------------------+----------------+
| - ``--csv``         | Output observations as CSV    | False          |
| - ``-c``            |                               |                |
+---------------------+-------------------------------+----------------+
| - ``--number``      | Output counts of species      | False          |
| - ``-n``            |                               |                |
+---------------------+-------------------------------+----------------+

The start and end times accept strings in any format accepted by the
`dateutil`_ package, for example "10:33" to a time today or "9 feb"
for a specific date.

``chirpy-heartbeat``
--------------------

This script generates periodic "heartbeat" messages to indicate that
the node is still alive.

+-------------------------+-------------------------------+----------------------+
| Option                  | Description                   | Default              |
+=========================+===============================+======================+
| - ``--interval`` <time> | Interval in seconds           | ``config.heartbeat`` |
| - ``-t`` <time>         |                               |                      |
+-------------------------+-------------------------------+----------------------+


.. _dateutil: https://dateutil.readthedocs.io/en/stable/

.. rubric:: Footnotes

.. [1] In detail, if the root topic is "chirpy" then the
       ``--roottopic`` option will subscribe to the wildcard channel
       "chirpy/2/json/#" and disencapsulate the "payload" field.
