from modeltranslation.translator import TranslationOptions, translator

from investments.models import (Bond, Business, Commodity, Equity, HedgeFund,
                                Investment, P2PLending, PreciousObject,
                                RealEstate)


class InvestmentTranslationOptions(TranslationOptions):
    fields = ('title', 'slug', 'description')


class P2PLendingTranslationOptions(TranslationOptions):
    fields = ()


class RealEstateTranslationOptions(TranslationOptions):
    fields = ()


class BusinessTranslationOptions(TranslationOptions):
    fields = ()


class PreciousObjectTranslationOptions(TranslationOptions):
    fields = ()

    
class HedgeFundTranslationOptions(TranslationOptions):
    fields = ()


class BondTranslationOptions(TranslationOptions):
    fields = ()


class CommodityTranslationOptions(TranslationOptions):
    fields = ()


class EquityTranslationOptions(TranslationOptions):
    fields = ()



translator.register(Investment, InvestmentTranslationOptions)
translator.register(P2PLending, P2PLendingTranslationOptions)
translator.register(RealEstate, RealEstateTranslationOptions)
translator.register(Business, BusinessTranslationOptions)
translator.register(PreciousObject, PreciousObjectTranslationOptions)
translator.register(HedgeFund, HedgeFundTranslationOptions)
translator.register(Bond, BondTranslationOptions)
translator.register(Commodity, CommodityTranslationOptions)
translator.register(Equity, EquityTranslationOptions)
