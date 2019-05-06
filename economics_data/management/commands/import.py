
import csv
from datetime import date
import json
import logging
import os

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import transaction
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django_countries import countries as available_countries
from economics_data.models import TimeSerie
from economics_data.models import TimeSerieEntry

logger = logging.getLogger("constriction.console")


class Command(BaseCommand):
    help = 'Scrapes and imports economic data from files'
    charts = [{"id": "gdp", "filter": "B1GQ,SCA,MIO_EUR_SCA", "title": _("Prodotto interno lordo"), "file": "teina010.tsv"},
              {"id": "housing", "filter": "TOTAL,I15_NSA", "title": _("Prezzo delle case"), "file": "teicp270.tsv"},
    ]

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        countries = []
        for country in available_countries:
            if country.code == "EU":
                countries.append("EU28")
            else:
                countries.append(country.code)
        countries = tuple(countries)
        for chart in self.charts:
            series = {}
            title = chart["title"]
            base_path = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(base_path, "data", chart["file"])
            for country in available_countries:
                series[country.code], res = TimeSerie.objects.get_or_create(title=title, slug=chart["id"], country=country)
                TimeSerieEntry.objects.filter(time_serie=series[country.code]).delete()
            with open(path) as tsvfile:
                quarters = []
                rows = csv.reader(tsvfile, delimiter='\t')
                first_row = next(rows)
                for header in first_row[1:]:
                    year, quarter = header.split("Q")
                    quarters.append(date(int(year), 3 * int(quarter) - 1, 15))
                for row in rows:
                    first_column = row[0]
                    if not first_column.endswith(countries) or not first_column.startswith(chart["filter"]):
                        continue
                    country_code = first_column.replace("EU28", "EU")[-2:]
                    for index, value in enumerate(row[1:]):
                        value = float(value.strip("p").strip())
                        entry = TimeSerieEntry(date=quarters[index], value=value, time_serie=series[country_code])
                        entry.save()
