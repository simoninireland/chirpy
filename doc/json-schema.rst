JSON object schemata
====================

Signal objects
--------------

+-------------+--------------+--------------------------------+
| Column name | Type         | Description                    |
+=============+==============+================================+
| timestamp   | datetime     | Start of sample period         |
+-------------+--------------+--------------------------------+
| duration    | float        | Sample length (s)              |
+-------------+--------------+--------------------------------+
| sampleRate  | long         | Sample rate (Hz)               |
+-------------+--------------+--------------------------------+
| signal      | float array  | Signal values                  |
+-------------+--------------+--------------------------------+
| stored      | boolean      | Whether signal has been stored |
+-------------+--------------+--------------------------------+

The length of ``sig`` will be ``duraction * sampleRate`` samples.


Observation objects
-------------------

+-------------+--------------+--------------------------------+
| Column name | Type         | Description                    |
+=============+==============+================================+
| timestamp   | datetime     | Start of observation period    |
+-------------+--------------+--------------------------------+
| id          | int          | Species index                  |
+-------------+--------------+--------------------------------+
| confidence  | float        | Confidence value               |
+-------------+--------------+--------------------------------+
| common      | string       | Species common name            |
+-------------+--------------+--------------------------------+
| sci         | string       | Species scientific name        |
+-------------+--------------+--------------------------------+
