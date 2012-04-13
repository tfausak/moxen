find . -name '*.py' | xargs pep8 && \
find . -name '*.py' | xargs pylint --rcfile=./.pylintrc && \
python manage.py test magic users
