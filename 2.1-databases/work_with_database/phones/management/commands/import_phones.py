import csv
from datetime import datetime as dt

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            phone_current = Phone()
            phone_current.name = phone["name"]
            phone_current.image = phone["image"]
            phone_current.price = phone["price"]
            phone_current.release_date = dt.strptime(phone["release_date"], "%Y-%m-%d").date()
            phone_current.lte_exists = phone["lte_exists"] == 'True'
            phone_current.slug = slugify(phone["name"])
            phone_current.save()
