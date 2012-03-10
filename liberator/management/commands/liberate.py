"""Convenience command to liberate from the command line.
"""
from django.core.management.base import BaseCommand
from liberator.shortcuts import liberate


class Command(BaseCommand):
    args = 'url ...'
    help = 'Liberate the given URLs.'

    def handle(self, *args, **options):
        for url in args:
            liberate(url)
