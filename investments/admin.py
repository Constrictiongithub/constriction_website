from django.contrib import admin
from modeltranslation.admin import TabbedExternalJqueryTranslationAdmin

from .models import Investment
from .models import InvestmentImage


class InvestmentImagesInline(admin.TabularInline):
    model = InvestmentImage.investments.through  # pylint: disable=no-member
    classes = ("collapse", )


class InvestmentAdmin(TabbedExternalJqueryTranslationAdmin):
    inlines = [InvestmentImagesInline, ]
    fieldsets = [
        (None, {
            'fields': ('title', 'description', 'url', 'category', 'source',
                       'country', 'address', 'surface', 'price', 'currency')}),
        (u'Advanced', {
            'fields': ('identifier', 'meta', 'tags', 'raw_data'),
            'classes': ('collapse', )}),
    ]


class InvestmentImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Investment, InvestmentAdmin)
admin.site.register(InvestmentImage, InvestmentImageAdmin)
