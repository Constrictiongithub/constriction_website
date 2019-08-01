from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from model_utils.managers import InheritanceManager

SOURCE_CHOICES = (('caseinpiemonte', _('Case in Piemonte')),
                  ('remicom', _('Remicom')),
                  ('exploresardinia', _('Explore Sardinia')),
                  ('sestrierecase', _('Sestriere case')),
                  ('manual', _('Manuale')), )

CATEGORY_CHOICES = (('realestate', _('Real estate')),
                    ('p2plending', _('P2P lending')), )


class Investment(models.Model):
    """ Generic investment """
    objects = InheritanceManager()
    category_id = "investment"
    category = models.CharField(max_length=15,
                                choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True, max_length=250)
    source = models.CharField(max_length=15,
                              choices=SOURCE_CHOICES,
                              default="manual")
    countries = CountryField(default="IT", multiple=True)
    price = models.DecimalField(null=True, max_digits=14, decimal_places=2)
    currency = models.CharField(blank=True ,null=True, max_length=3)
    interests = models.DecimalField(blank=True, null=True, max_digits=14, decimal_places=2)

    def __str__(self):
        return self.title

    @property
    def first_image(self):
        images = self.images.all()
        try:
            return images[0].image
        except IndexError:
            return None

    @property
    def category_image_url(self):
        return "{}/images/{}.jpg".format(settings.STATIC_URL, self.category_id)

    @property
    def card_snippet_url(self):
        return "snippets/{}_card.html".format(self.category)

    def save(self, *args, **kwargs):
        self.category = self.category_id
        super().save(*args, **kwargs)


class RealEstate(Investment):
    category_id = "realestate"
    address = models.CharField(null=True, max_length=500)
    surface = models.DecimalField(null=True, max_digits=8, decimal_places=2)
    raw_data = JSONField(null=True)
    identifier = models.CharField(null=True, blank=True, unique=True,
                                  max_length=200)

    class Meta:
        verbose_name = _("Real estate investment")
        verbose_name_plural = _("Real estate investments")


class P2PLending(Investment):
    category_id = "p2plending"
    buyback = models.BooleanField()

    class Meta:
        verbose_name = _("Peer to peer lending investment")
        verbose_name_plural = _("Peer to peer lending investments")


class InvestmentImage(models.Model):
    investments = models.ManyToManyField(Investment, related_name='images')
    image = models.ImageField(upload_to="uploads/investments")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    identifier = models.CharField(null=True, blank=True, unique=True,
                                  max_length=200)

    class Meta:
        verbose_name = _("Investment image")
        verbose_name_plural = _("Investment images")

    def __str__(self):
        return self.identifier
