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
import sqlite3


# Global database connection
connection = None


def dbCreate():
    """Create the tables for a new database."""
    global connection
    cursor = connection.cursor()

    # create labels table from labels list
    cursor.execute("CREATE TABLE bird(id, common_name, scientific_name)")
    for i in range(len(chirpy.labels)):
        common, sci = chirpy.labels[i]
        cursor.execute("INSERT INTO bird VALUES(?, ?, ?)", [id, common, sci])

    # create an empty spots table
    cursor.execute("CREATE TABLE observation(timestamp, id, confidence)")

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
    else:
        # doesn't exist, create it
        connection = sqlite3.connect(fn)
        createDatabase()


def dbRecordObservation(observation):
    """Record an observation into the database.

    @param observetion: the observation"""
    global connection
    cursor = connection.cursor()

    cursor.execute("INSERT INTO observation VALUES(?, ?, ?)", [observation['timestamp'],
                                                               observation['id'],
                                                               observation['confidence']])
    connection.commit()


def dbAllObservationsOf(id):
    """Return a list of all the observations of the given bird species.

    The list returned is a list of timestamps and confidences.

    @param id: the species id
    @returns: a list of (timestamp, confidence) lists"""
    global connection
    cursor = connection.cursor()

    cursor.execute("SELECT timestamp, confidence FROM observation WHERE id = ?", id)
    return cursor.fetchall()
