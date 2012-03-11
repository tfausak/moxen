# Bauble

A [Magic: The Gathering][1] card database.

## Setup

By default, this project uses an SQLite database. It's in the source
tree, but it needs to be removed from the index.

    git update-index --assume-unchanged db.sq3

The database is empty to start with. At the very least, it needs a
superuser and the included fixtures.

    python manage.py syncdb

You could manually enter all the card data, but with more than
12,000 cards you'd be at it for a while. Use the built-in `liberate`
command to get card information from the [Gatherer][2].

    python manage.py liberate 'http://gatherer.wizards.com/Pages/Search/' \
        '?output=spoiler&method=text&special=true&format=+![%22Un-Sets%22]'

(Getting all the cards at once, as the command above does, takes a
long time. It depends on a lot of things, but you can expect it to
take at least 10 minutes.)

You'll have to manually combine double-faced, flip, and split cards.
The easiest way to do that is through the admin interface. Fire up
the server with `python manage.py runserver` and point your browser
to `localhost:8000/admin`. You only need to set one side of the
relation; the other will be set automatically. For instance, settings
Assault's other to Battery automatically set's Battery's to Assault.

[1]: http://en.wikipedia.org/wiki/Magic:_The_Gathering
[2]: http://gatherer.wizards.com/
