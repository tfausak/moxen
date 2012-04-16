# Bauble [![Build status][]][Travis CI]

A [Magic: the Gathering][] card database.

## Setup

```sh
# Get source.
git clone https://github.com/tfausak/bauble.git
cd bauble

# Load dependencies.
pip install -r requirements.txt

# Run tests.
python manage.py test bauble magic

# Fill database.
python manage.py syncdb
python manage.py loaddata color manasymbol manacost \
    supertype cardtype subtype \
    set rarity block format \
    card printing legality ruling

# Run server.
python manage.py runserver
```

## Requirements

-   [Python][] 2.7
-   [Django][] 1.4
-   [BeautifulSoup][] 3.2
-   [django-profiles][] 0.2
-   [django-registration][] 0.7

[build status]: <https://secure.travis-ci.org/tfausak/bauble.png> "Travis CI build status"
[travis ci]: <http://travis-ci.org/tfausak/bauble> "Travis CI"
[magic: the gathering]: <http://wizards.com/magic> "Magic: the Gathering"
[python]: <http://python.org/> "Python"
[django]: <https://www.djangoproject.com/> "Django"
[beautifulsoup]: <http://www.crummy.com/software/BeautifulSoup> "BeautifulSoup"
[django-profiles]: <https://bitbucket.org/ubernostrum/django-profiles> "django-profiles"
[django-registration]: <https://bitbucket.org/ubernostrum/django-registration> "django-registration"
