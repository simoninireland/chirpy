Database schema
===============

The observations database consists of two tables, for species and
observations.

``species`` table
-----------------

+-----------------+--------------+--------------------------------+
| Column name     | Type         | Description                    |
+=================+==============+================================+
| id              | INTEGER      | Species class                  |
+-----------------+--------------+--------------------------------+
| common_name     | VARCHAR(200) | Common name of the species     |
+-----------------+--------------+--------------------------------+
| scientific_name | VARCHAR(200) | Scientific name of the species |
+-----------------+--------------+--------------------------------+

When the database is first created the species table is populated from
the labels associated with the classification model. The ``id`` field
corresponds to the index in the model's classification vector.

``observation`` table
---------------------

+-------------+--------------+--------------------------------+
| Column name | Type         | Description                    |
+=============+==============+================================+
| timestamp   | TIMESTAMP    | Species class                  |
+-------------+--------------+--------------------------------+
| node        | VARCHAR(100) | Node identifier                |
+-------------+--------------+--------------------------------+
| id          | INTEGER      | Foreign key to ``soecies``     |
+-------------+--------------+--------------------------------+
| confidence  | REAL         | Confidence value               |
+-------------+--------------+--------------------------------+
