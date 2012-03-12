# Bauble

[![Build Status][1]][2]
A [Magic: The Gathering][3] card database.

## Requirements

-   [Python 2.7.1][4]
-   [Django 1.3][5]
-   [BeautifulSoup 3.2][6]
-   [Docutils 0.8][7]
-   [django-registration 0.7][8]
-   [django-profiles 0.2][9]

## Setup

Before getting any card information, the database needs to be populated
with types, expansions, etc.

    python manage.py syncdb
    python manage.py loaddata supertype cardtype subtype set rarity color block format

You could manually enter all the card data, but with more than
12,000 cards you'd be at it for a while. Use the built-in `liberate`
command to get card information from the [Gatherer][10].

    python manage.py liberate 'http://gatherer.wizards.com/Pages/Search/?output=spoiler&method=text&special=true&format=+![%22Un-Sets%22]'

(Getting all the cards at once, as the command above does, takes a
long time. It depends on a lot of things, but you can expect it to
take at least 10 minutes.)

You'll have to manually combine double-faced, flip, and split cards.
The easiest way to do that is through the admin interface. Fire up
the server with `python manage.py runserver` and point your browser
to `localhost:8000/admin`. You only need to set one side of the
relation; the other will be set automatically. For instance, settings
Assault's other to Battery automatically set's Battery's to Assault.

[1]: https://secure.travis-ci.org/tfausak/bauble.png?branch=master
[2]: http://travis-ci.org/tfausak/bauble
[3]: http://en.wikipedia.org/wiki/Magic:_The_Gathering
[4]: http://python.org/
[5]: https://www.djangoproject.com/
[6]: http://www.crummy.com/software/BeautifulSoup/
[7]: http://docutils.sourceforge.net/
[8]: https://bitbucket.org/ubernostrum/django-registration/
[9]: https://bitbucket.org/ubernostrum/django-profiles/
[10]: http://gatherer.wizards.com/
