# Moxen [![Build status][]][Travis CI]

A [Magic: the Gathering][] card database.

This project is more or less stuck in development hell. It will
probably never be finished. It's a pretty sweet production-ready
Django application, though!

## Setup

### Development

```sh
git clone https://github.com/tfausak/moxen
virtualenv moxen
cd moxen
source bin/activate
pip install -r requirements/development.txt
fab setup  # Might take a while.
fab server
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
