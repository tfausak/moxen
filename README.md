# Bauble

A [Magic: The Gathering][1] card database.

## Requirements

-   [Python 2.7.1][2]
-   [Django 1.3.1][3]
-   [BeautifulSoup 3.2.1][4]
-   [Docutils 0.8.1][5]
-   [django-registration 0.7][6]
-   [django-profiles 0.2][7]

## Setup

Before getting any card information, the database needs to be populated
with types, expansions, etc.

    python manage.py syncdb
    python manage.py loaddata supertype cardtype subtype set rarity color block format

You could manually enter all the card data, but with more than
12,000 cards you'd be at it for a while. Use the built-in `liberate`
command to get card information from the [Gatherer][8].

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

[1]: http://en.wikipedia.org/wiki/Magic:_The_Gathering
[2]: http://python.org/
[3]: https://www.djangoproject.com/
[4]: http://www.crummy.com/software/BeautifulSoup/
[5]: http://docutils.sourceforge.net/
[6]: https://bitbucket.org/ubernostrum/django-registration/
[7]: https://bitbucket.org/ubernostrum/django-profiles/
[8]: http://gatherer.wizards.com/
