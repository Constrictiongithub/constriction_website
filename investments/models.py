from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

CATEGORY_CHOICES = (('immobili', _('Immobili')),
                    ('finanza', _('Finanza')), )
SOURCE_CHOICES = (('caseinpiemonte', _('Case in Piemonte')),
                  ('remicom', _('Remicom')),
                  ('exploresardinia', _('Explore Sardinia')),
                  ('sestrierecase', _('Sestriere case')),
                  ('manual', _('Manuale')), )


class Investment(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True, max_length=250)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    source = models.CharField(max_length=15, choices=SOURCE_CHOICES,
                              default="manual")
    country = CountryField(default="IT", multiple=True)
    address = models.CharField(blank=True, null=True, max_length=500)
    surface = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)
    price = models.DecimalField(blank=True, null=True, max_digits=14, decimal_places=2)
    currency = models.CharField(blank=True, null=True, max_length=3)
    identifier = models.CharField(unique=True, max_length=200)
    meta = JSONField(blank=True, null=True)
    tags = JSONField(blank=True, null=True)
    raw_data = JSONField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def first_image(self):
        images = self.images.all()  # pylint: disable=no-member
        try:
            return images[0].image
        except IndexError:
            return None

    @property
    def category_image_url(self):
        return "{}/images/{}.jpg".format(settings.STATIC_URL, self.category)


class InvestmentImage(models.Model):

    identifier = models.CharField(unique=True, max_length=200)
    investments = models.ManyToManyField(Investment, related_name='images')
    image = models.ImageField(upload_to="uploads/investments")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.identifier
