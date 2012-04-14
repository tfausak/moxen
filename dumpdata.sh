#!/usr/bin/sh

for model
do
    echo $model
    python manage.py dumpdata magic.$model | \
    python -m json.tool | \
    sed 's/ *$//' > \
    magic/fixtures/$(echo $model | tr '[:upper:]' '[:lower:]').json
done
