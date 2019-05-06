from django.db import models
from django_countries.fields import CountryField

# Create your models here.

class TimeSerie(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    country = CountryField()

    def __str__(self):
        return self.title + " - " + self.country.code

    
class TimeSerieEntry(models.Model):

    class Meta:
        ordering = ['date']

    date = models.DateField()
    value = models.DecimalField(null=True, max_digits=14, decimal_places=2)
    time_serie = models.ForeignKey(TimeSerie, related_name='entries', on_delete=models.CASCADE)
