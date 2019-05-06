from django.contrib import admin

from .models import TimeSerie
from .models import TimeSerieEntry


class TimeSerieEntryInline(admin.TabularInline):
    model = TimeSerieEntry

class TimeSerieAdmin(admin.ModelAdmin):
    inlines = [TimeSerieEntryInline, ]
    class Meta:
        model = TimeSerie


admin.site.register(TimeSerie, TimeSerieAdmin)
