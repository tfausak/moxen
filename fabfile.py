from fabric.api import env, local, task
import re

env.run = 'heroku run python manage.py'


@task
def bootstrap():
    addons = {
        'cloudamqp': 'lemur',
        'heroku-postgresql': 'dev',
        'memcache': '5mb',
        'sendgrid': 'starter',
    }

    configs = {
        'AWS_ACCESS_KEY_ID': 'aws_access_key_id',
        'AWS_SECRET_ACCESS_KEY': 'aws_secret_access_key',
        'AWS_STORAGE_BUCKET_NAME': 'aws_storage_bucket_name',
        'DJANGO_SETTINGS_MODULE': 'moxen.settings.production',
        'SECRET_KEY': 'secret_key',
    }

    local('heroku apps:create')
    local('heroku ps:scale web=1')
    for key, value in addons:
        local('heroku addons:add {}:{}'.format(key, value))
    for key, value in configs:
        local('heroku config:set {}={}'.format(key, value))

    output = local('heroku pg:info', capture=True)
    database = re.match('^=== ([A-Z_]+)', output).group(1)
    local('heroku pg:promote {}'.format(database))


@task
def console():
    local('python manage.py debugsqlshell')


@task
def deploy():
    local('git push heroku master')
    local('{.run} syncdb --noinput'.format(env))
    local('{.run} migrate --noinput'.format(env))
    local('{.run} collectstatic --noinput'.format(env))
    local('{.run} compress'.format(env))


@task
def server():
    local('python manage.py syncdb --noinput')
    local('python manage.py migrate --noinput')
    local('python manage.py runserver')


@task
def setup():
    local('python manage.py syncdb --all')
    local('python manage.py migrate --fake')
    local('python manage.py loaddata color manasymbol manacost supertype '
        'cardtype subtype set rarity block format ruling card printing '
        'legality')


@task
def lint():
    local('pep8 . --config=.pep8')
    local('pylint *.py --rcfile=.pylintrc')
    local('pylint moxen --rcfile=.pylintrc')


@task
def test():
    lint()
    local('python manage.py test')
