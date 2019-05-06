import json
import logging

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import transaction
from investments.models import Investment

from .scrapers import caseinpiemonte
from .scrapers import exploresardinia
from .scrapers import remicom
from .scrapers import sestrierecase

logger = logging.getLogger("constriction.console")
AVAILABLE_SITES = ("caseinpiemonte", "remicom", "exploresardinia", "sestrierecase")


class Command(BaseCommand):
    help = 'Scrapes and imports investments data from websites'

    def add_arguments(self, parser):
        parser.add_argument('--site', "-s", type=str)
        parser.add_argument('--noupdate', "-n", action='store_true')
        parser.add_argument("--delete", "-d", action='store_true')
        parser.add_argument("--limit", "-l", type=int)
        parser.add_argument("--offset", "-o", type=int)

    def handle(self, *args, **options):
        
        limit = options["limit"]
        offset = options["offset"]
        if offset and limit:
            limit += offset
        noupdate = options["noupdate"]
        site = options["site"]
        delete = options["delete"]
        for available_site in AVAILABLE_SITES:
            if not site or site == available_site:
                self.scrape_site(available_site, limit, offset, noupdate, delete)

    def scrape_site(self, module, limit, offset, noupdate, delete):
        module = eval(module)
        added_identifiers = []
        for count, item in enumerate(module.scrape_site(noupdate)):
            if offset and count < offset:
                continue
            if limit and count >= limit:
                break
            if item:
                with transaction.atomic():
                    try:
                        investment = module.save_investment(item)
                    except:
                        import ipdb; ipdb.set_trace()
                    if investment:
                        added_identifiers.append(investment.identifier)
        if delete and added_identifiers:
            identifiers = Investment.objects.filter(source=module).values_list('identifier')
            identifiers_to_delete = [i for i in identifiers if i not in added_identifiers]
            if identifiers_to_delete:
                logger.warning("Deleting %s", identifiers_to_delete)
            Investment.objects.filter(identifier__in=identifiers_to_delete).delete()
