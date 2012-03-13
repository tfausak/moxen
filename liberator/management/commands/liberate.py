from django.core.management.base import BaseCommand
from liberator.shortcuts import liberate


class Command(BaseCommand):
    """Convenience command to liberate pages from the command line.
    """
    args = 'url ...'
    help = 'Liberate the given URLs.'

    def handle(self, *args, **options):
        for url in args:
            liberate(url)
