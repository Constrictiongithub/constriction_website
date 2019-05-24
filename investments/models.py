from autoslug import AutoSlugField
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from sorl.thumbnail import ImageField as SorlThumbnailImageField

CATEGORY_CHOICES = (('immobili', _('Immobili')),
                    ('finanza', _('Finanza')),
)
SOURCE_CHOICES = (('caseinpiemonte', _('Case in Piemonte')),
                  ('remicom', _('Remicom')),
                  ('exploresardinia', _('Explore Sardinia')),
                  ('sestrierecase', _('Sestriere case')),
                  ('manual', _('Manuale')),
)

class Investment(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True)
    url = models.URLField(null=True, max_length=250)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    source = models.CharField(max_length=15, choices=SOURCE_CHOICES, default="manual")
    country = CountryField(default="IT")
    address = models.CharField(null=True, max_length=500)
    surface = models.DecimalField(null=True, max_digits=8, decimal_places=2)
    price = models.DecimalField(null=True, max_digits=14, decimal_places=2)
    currency = models.CharField(null=True, max_length=3)
    identifier = models.CharField(unique=True, max_length=200)
    meta = JSONField(null=True)
    tags = JSONField(null=True)
    raw_data = JSONField(null=True)

    def __str__(self):
        return self.title

    @property
    def first_image(self):
        images = self.images.all()
        try:
            return images[0]
        except IndexError:
            return None


class InvestmentImage(models.Model):
    identifier = models.CharField(unique=True, max_length=200)
    investments = models.ManyToManyField(Investment, related_name='images')
    image = SorlThumbnailImageField(upload_to='images')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.identifier
