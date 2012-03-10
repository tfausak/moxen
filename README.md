# Bauble

A [Magic: The Gathering][1] card database.

## Setup

Remove the SQLite database from git's index:

    git update-index --assume-unchanged db.sq3

Create a superuser and install objects from fixtures:

    python manage.py syncdb

[1]: http://en.wikipedia.org/wiki/Magic:_The_Gathering
