"""Constants used in the liberation process.
"""
import re


GATHERER_URL = re.compile('^http://gatherer[.]wizards[.]com/')
GATHERER_STANDARD_URL = re.compile(r'\boutput=standard\b')
GATHERER_COMPACT_URL = re.compile(r'\boutput=compact\b')
GATHERER_CHECKLIST_URL = re.compile(r'\boutput=checklist\b')
GATHERER_VISUAL_URL = re.compile(r'\bmethod=visual\b')
GATHERER_TEXT_URL = re.compile(r'\bmethod=text\b')
GATHERER_CARD_URL = re.compile(r'\bmultiverseid=\d\+\b')
