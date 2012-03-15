from BeautifulSoup import BeautifulSoup
from liberator.forms import GathererTextForm
from magic.forms import CardForm
from urllib2 import urlopen
import pprint
import re
import sys


def main(*args):
    for arg in args:
        liberate(arg)


def liberate(url):
    response = urlopen(url)
    dom = BeautifulSoup(response)
    kwargs = {}
    for tag in dom.find('div', 'textspoiler').findAll('tr'):
        tags = tag.findAll('td')
        if len(tags) != 1:
            key = re.sub('[^a-z]', '_', tags[0].string.strip().lower()[:-1])
            kwargs[key] = '\n'.join(
                text for text in tags[1].findAll(text=True))
        else:
            form = GathererTextForm(kwargs)
            _ = form.is_valid()
            pprint.pprint(form.cleaned_data)
            kwargs = {
                'name': form.cleaned_data['name'],
                'rules_text': '\n'.join(form.cleaned_data['rules_text']),
            }
            card = CardForm(kwargs)
            card.is_valid()
            kwargs = {}


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
