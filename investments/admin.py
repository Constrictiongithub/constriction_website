from django.contrib import admin
from modeltranslation.admin import TabbedExternalJqueryTranslationAdmin

from .models import InvestmentImage, P2PLending, RealEstate


class InvestmentImagesInline(admin.TabularInline):
    model = InvestmentImage.investments.through  # pylint: disable=no-member
    classes = ("collapse", )


class RealEstateAdmin(TabbedExternalJqueryTranslationAdmin):
    inlines = [InvestmentImagesInline, ]
    fieldsets = [
        (None, {
            'fields': ('title', 'description', 'source', 'url', 'countries',
                       'address', 'surface', 'price', 'currency')}),
        (u'Import', {
            'fields': ('identifier', 'raw_data'),
            'classes': ('collapse', )}),
    ]


class P2PLendingAdmin(TabbedExternalJqueryTranslationAdmin):
    inlines = [InvestmentImagesInline, ]
    fieldsets = [
        (None, {
            'fields': ('title', 'description', 'source', 'url', 'countries',
                       'buyback' 'price', 'currency')}),
    ]


class InvestmentImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(RealEstate, RealEstateAdmin)
admin.site.register(P2PLending, P2PLendingAdmin)
admin.site.register(InvestmentImage, InvestmentImageAdmin)
