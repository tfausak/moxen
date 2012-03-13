# Bauble [![][1]][2]

A [Magic: The Gathering][3] card database.

## Requirements

-   [Python][4] 2.7
-   [Django][5] 1.3
-   [BeautifulSoup][6] 3.2
-   [Docutils][7] 0.8
-   [django-profiles][8] 0.2
-   [django-registration][9] 0.7

## Installation

    # Get the source.
    git clone https://github.com/tfausak/bauble.git
    cd bauble

    # Automatically get all the requirements.
    pip install -r requirements.txt

    # Run the unit tests.
    python manage.py test

    # Fill the database with data.
    python manage.py syncdb
    python manage.py loaddata color supertype cardtype subtype set rarity block format card printing legality

    # Fire up the server.
    python manage.py runserver
    # http://localhost:8000/

## Configuration

You should go to the admin page (usually `localhost:8000/admin`)
to change the site name and domain. "example.com" isn't very catchy.

Django's `settings.py` is split into two sections. In the top
section, you'll find things you'll probably want to change. Use a
different database, change the administrator, turn off debug mode,
etc.

You should probably avoid editing the bottom section unless you
know what you're doing.

[1]: https://secure.travis-ci.org/tfausak/bauble.png
[2]: http://travis-ci.org/tfausak/bauble
[3]: http://www.wizards.com/magic/
[4]: http://python.org/
[5]: https://www.djangoproject.com/
[6]: http://www.crummy.com/software/BeautifulSoup/
[7]: http://docutils.sourceforge.net/
[8]: https://bitbucket.org/ubernostrum/django-profiles/
[9]: https://bitbucket.org/ubernostrum/django-registration/
