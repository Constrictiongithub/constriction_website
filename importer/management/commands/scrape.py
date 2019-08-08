import json
import logging

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from .scrapers import caseinpiemonte, exploresardinia, remicom, sestrierecase

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
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
        logger.warning("logging started")
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
                    except Exception as exc:
                        continue
                    if investment:
                        added_identifiers.append(investment.identifier)
        if delete and added_identifiers:
            # TODO: gestire eliminazione a seconda del type.
            identifiers = module.TYPE.objects.filter(source=module).values_list('identifier')
            identifiers_to_delete = [i for i in identifiers if i not in added_identifiers]
            if identifiers_to_delete:
                logger.warning("Deleting %s", identifiers_to_delete)
            module.TYPE.objects.filter(identifier__in=identifiers_to_delete).delete()
