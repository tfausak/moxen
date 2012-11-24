# Moxen [![Build status][]][Travis CI]

A [Magic: the Gathering][] card database.

## Setup

### Development

```sh
git clone https://github.com/tfausak/moxen
cd moxen
pip install -r requirements/development.txt  # You should use virtualenv.
fab test  # Optional, but recommended.
fab setup  # Might take a while.
fab runserver
# http://localhost:8000/
```

### Production

```sh
fab bootstrap  # First time only.
fab deploy  # Might take a while.
# heroku open
```

[build status]: https://travis-ci.org/tfausak/moxen.png
[travis ci]: https://travis-ci.org/tfausak/moxen
[magic: the gathering]: http://wizards.com/magic
