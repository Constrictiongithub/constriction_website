from django.contrib import admin
from modeltranslation.admin import TabbedExternalJqueryTranslationAdmin

from .models import Investment
from .models import InvestmentImage


class InvestmentImagesInline(admin.TabularInline):
    model = InvestmentImage.investments.through
    classes = ("collapse", )


class InvestmentAdmin(TabbedExternalJqueryTranslationAdmin):
    inlines = [InvestmentImagesInline, ]
    fieldsets = [
        (None, {'fields': ('title', 'description', 'url', 'category', 'source', 'country', 'address', 'surface', 'price', 'currency')}),
        (u'Advanced', {'classes': ('collapse', ), 'fields': ('identifier', 'meta', 'tags', 'raw_data')}),
    ]

admin.site.register(Investment, InvestmentAdmin)
