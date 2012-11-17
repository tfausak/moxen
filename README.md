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
python manage.py test

# Fill database.
python manage.py syncdb
python manage.py loaddata color manasymbol manacost \
    supertype cardtype subtype \
    set rarity block format \
    ruling card printing legality

# Run server.
python manage.py runserver
```

## Fixtures

Card data is provided in JSON fixtures. If you update the card data,
either with the scraper or manually, you should repopulate all the
fixtures to keep them current.

```sh
fixtures=( Block Card CardType Color Format Legality ManaCost ManaSymbol
    Printing Rarity Ruling Set SubType SuperType )
for fixture in ${fixtures[@]}
do
    python manage.py dumpdata magic.$fixture |
    python -m json.tool |
    sed 's/ $//' > \
        magic/fixtures/$(echo $fixture | tr '[:upper:]' '[:lower:]').json
done
```

## Requirements

-   [Python][] 2.7
-   [Django][] 1.4
-   [BeautifulSoup][] 4.1
-   [django-profiles][] 0.2
-   [django-registration][] 0.8

[build status]: <https://secure.travis-ci.org/tfausak/bauble.png> "Travis CI build status"
[travis ci]: <http://travis-ci.org/tfausak/bauble> "Travis CI"
[magic: the gathering]: <http://wizards.com/magic> "Magic: the Gathering"
[python]: <http://python.org/> "Python"
[django]: <https://www.djangoproject.com/> "Django"
[beautifulsoup]: <http://www.crummy.com/software/BeautifulSoup> "Beautiful Soup"
[django-profiles]: <https://bitbucket.org/ubernostrum/django-profiles> "django-profiles"
[django-registration]: <https://bitbucket.org/ubernostrum/django-registration> "django-registration"
