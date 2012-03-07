# Bauble

A [Magic: The Gathering][1] card database.

## Setup

The SQLite database is required, but changes to it shouldn't be
tracked by git.

    git update-index --assume-unchanged db.sq3

As with all Django projects, this one needs to set up some database
stuff.

    python manage.py syncdb

Running the server is just like everything else Django.

    python manage.py runserver

## Development

Want to help out? Awesome. Make sure that everything you do passes
pylint with flying colors.

    find . -name '*.py' | xargs pylint -i y -f colorized

[1]: http://en.wikipedia.org/wiki/Magic:_The_Gathering
