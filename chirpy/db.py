# Spotter database
#
# Copyright (C) 2025--2026 Simon Dobson
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software. If not, see <http://www.gnu.org/licenses/gpl.html>.

import chirpy
from os.path import exists, isfile
from datetime import datetime
import sqlite3


# Global database connection
connection = None


def dbCreate():
    """Create the tables for a new database."""
    cursor = connection.cursor()

    # create labels table from labels list
    cursor.execute("""CREATE TABLE species(
    id INTEGER,
    common_name VARCHAR(200),
    scientific_name VARCHAR(200)
    )""")
    labels = chirpy.getLabelsMapping()
    for i in range(len(labels)):
        sci, common = labels[i]
        cursor.execute("INSERT INTO species VALUES(?, ?, ?)", [i, common, sci])
    chirpy.logger.info(f"Created species table ({len(labels)} classes)")

    # create an empty spots table
    cursor.execute("""CREATE TABLE observation(
    timestamp INTEGER,
    node VARCHAR(100),
    id INTEGER,
    confidence REAL
    )""")
    chirpy.logger.info("Created observations table")

    connection.commit()


def dbOpenConnection(fn):
    """Open a database connection to the given filename.

    If the file doesn't exist, create a database.

    Opening a connection twice does nothing, even if the filenames
    given are different.

    @param fn: the database file

    """
    global connection

    # no-op if we're already open
    if connection is not None:
        return

    if exists(fn):
        if not isfile(fn):
            # exists but not a file
            raise ValueError(f"Can't open {fn} as database file")
        else:
            # exists and is file, connect
            connection = sqlite3.connect(fn)
            chirpy.logger.info(f"Using database in {fn}")
    else:
        # doesn't exist, create it
        chirpy.logger.info(f"Creating database in {fn}")
        connection = sqlite3.connect(fn)
        dbCreate()


def dbRecordObservation(observation):
    """Record an observation into the database.

    @param observetion: the observation"""
    cursor = connection.cursor()

    try:
        # convert datetime object to timestamp
        ts = round(datetime.fromisoformat(observation['timestamp']).timestamp())

        cursor.execute("INSERT INTO observation VALUES(?, ?, ?, ?)", [ts,
                                                                      observation['nodeIdentifier'],
                                                                      observation['id'],
                                                                      observation['confidence']])
        connection.commit()
        chirpy.logger.debug(f"Recorded observation {json.dumps(observation)}")
    except ValueError:
        chirpy.logger.error(f"Can't parse timestamp {observation['timestamp']}")
    except Exception as e:
        chirpy.logger.error(f"Error storing observation: {e}")


def dbAllObservationsOf(id):
    """Return a list of all the observations of the given bird species.

    The list returned is a list of timestamps and confidences.

    @param id: the species id
    @returns: a list of (timestamp, confidence) lists"""
    cursor = connection.cursor()

    cursor.execute("SELECT timestamp, confidence FROM observation WHERE id = ?", id)
    return cursor.fetchall()


def dbAllObservationsBetween(start, end = None):
    """Return a list of all the observations between two timestamps.

    If the end timestamp is omitted, observations are selected up until now,

    The list elements are timestamp, confidence, common name, and scientific name.
    The list is ordered by timestamp, earliest observation first.

    @param start: the start time
    @param end: (optional) the end time (defaults to now)
    @returns: the list of observations"""
    cursor = connection.cursor()

    if end is None:
        end = datetime.now()

    # convert datetime objects to timestamps
    sts = start.timestamp()
    ets = end.timestamp()

    cursor.execute("""SELECT timestamp, confidence, common_name, scientific_name
    FROM observation INNER JOIN species ON species.id = observation.id
    WHERE timestamp BETWEEN ? AND ?
    ORDER BY timestamp""", [sts, ets])

    # map timestamps to datetimes
    observations = cursor.fetchall()
    return map(lambda obs: [ datetime.fromtimestamp(obs[0]), obs[1], obs[2], obs[3] ], observations)


def dbCountObservationsBetween(start, end = None):
    """Return a dict mapping species names to count of observations between teo timestamps.

    If the end timestamp is omitted, observations are selected up until now,

    @param start: the start time
    @param end: (optional) the end time (defaults to now)
    @returns: the dict of counts"""
    cursor = connection.cursor()

    if end is None:
        end = datetime.now()

    # convert datetime objects to timestamps
    sts = start.timestamp()
    ets = end.timestamp()

    cursor.execute("""SELECT common_name, COUNT(*) AS count
    FROM observation INNER JOIN species ON species.id = observation.id
    WHERE timestamp BETWEEN ? AND ?
    GROUP BY observation.id""", [sts, ets])

    # convert to a dict
    observations = cursor.fetchall()
    counts = {}
    for obs in observations:
        counts[obs[0]] = obs[1]
    return counts
