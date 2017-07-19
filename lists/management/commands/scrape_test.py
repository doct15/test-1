################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define RadHR Test Scrape.                                           ##
################################################################################


################################################################################
## Import Required Libraries.                                                 ##
################################################################################
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

################################################################################
## Import Third Party Models.                                                 ##
################################################################################
import time
import datetime

################################################################################
## Import Defined Models.                                                     ##
################################################################################
# from simple_history.utils import update_change_reason
from posts.utils import create_slug
from lists.models import Watchlist

################################################################################
## Define the Command Function.                                               ##
################################################################################
class Command(BaseCommand):

    args = ''
    help = 'Grabs things we need for Test and stores them in the DB'

    ############################################################################
    ## Define The Create Notes Function.                                      ##
    ############################################################################
    def _create_notes(self):
        notes = Watchlist(notes='test')
        notes.save()

    ############################################################################
    ## Define the Handle Function.                                            ##
    ############################################################################
    def handle(self, *args, **options):
        self._create_notes()
        self.stdout.write(self.style.SUCCESS('A **NEW** Note has just been saved on behalf of %s' % (user)))
