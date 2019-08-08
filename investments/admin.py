from django.contrib import admin
from modeltranslation.admin import TabbedExternalJqueryTranslationAdmin

from .models import (Bond, Business, Commodity, Equity, HedgeFund, Investment,
                     InvestmentImage, P2PLending, PreciousObject, RealEstate)


class InvestmentImagesInline(admin.TabularInline):
    model = InvestmentImage.investments.through  # pylint: disable=no-member
    classes = ("collapse", )


class InvestmentAdmin(TabbedExternalJqueryTranslationAdmin):
    inlines = [InvestmentImagesInline, ]
    fieldsets = [
        (None, {
            'fields': ('title', 'description', 'source', 'url', 'countries',
                       'price', 'currency')}),
    ]


class RealEstateAdmin(TabbedExternalJqueryTranslationAdmin):
    inlines = [InvestmentImagesInline, ]
    fieldsets = [
        (None, {
            'fields': ('title', 'description', 'source', 'url', 'countries',
                       'address', 'surface', 'price', 'currency')}),
    ]


class P2PLendingAdmin(TabbedExternalJqueryTranslationAdmin):
    inlines = [InvestmentImagesInline, ]
    fieldsets = [
        (None, {
            'fields': ('title', 'description', 'source', 'url', 'countries',
                       'buyback', 'price', 'currency')}),
    ]


class BusinessAdmin(TabbedExternalJqueryTranslationAdmin):
    inlines = [InvestmentImagesInline, ]
    fieldsets = [
        (None, {
            'fields': ('title', 'description', 'source', 'url', 'countries',
                       'price', 'currency')}),
    ]


class EquityAdmin(TabbedExternalJqueryTranslationAdmin):
    inlines = [InvestmentImagesInline, ]
    fieldsets = [
        (None, {
            'fields': ('title', 'description', 'source', 'url', 'countries',
                       'price', 'currency')}),
    ]


class PreciousObjectAdmin(TabbedExternalJqueryTranslationAdmin):
    inlines = [InvestmentImagesInline, ]
    fieldsets = [
        (None, {
            'fields': ('title', 'description', 'source', 'url', 'countries',
                       'price', 'currency')}),
    ]
    
class HedgeFundAdmin(TabbedExternalJqueryTranslationAdmin):
    inlines = [InvestmentImagesInline, ]
    fieldsets = [
        (None, {
            'fields': ('title', 'description', 'source', 'url', 'countries',
                       'price', 'currency')}),
    ]


class BondAdmin(TabbedExternalJqueryTranslationAdmin):
    inlines = [InvestmentImagesInline, ]
    fieldsets = [
        (None, {
            'fields': ('title', 'description', 'source', 'url', 'countries',
                       'price', 'currency')}),
    ]
    

class CommodityAdmin(TabbedExternalJqueryTranslationAdmin):
    inlines = [InvestmentImagesInline, ]
    fieldsets = [
        (None, {
            'fields': ('title', 'description', 'source', 'url', 'countries',
                       'price', 'currency')}),
    ]
    

class InvestmentImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(RealEstate, RealEstateAdmin)
admin.site.register(P2PLending, P2PLendingAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(PreciousObject, PreciousObjectAdmin)
admin.site.register(HedgeFund, HedgeFundAdmin)
admin.site.register(Bond, BondAdmin)
admin.site.register(Commodity, CommodityAdmin)
# admin.site.register(InvestmentImage, InvestmentImageAdmin)
