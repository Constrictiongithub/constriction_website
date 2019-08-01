from modeltranslation.translator import TranslationOptions, translator

from investments.models import Investment, P2PLending, RealEstate


class InvestmentTranslationOptions(TranslationOptions):
    fields = ('title', 'slug', 'description')


class P2PLendingTranslationOptions(TranslationOptions):
    fields = ()


class RealEstateTranslationOptions(TranslationOptions):
    fields = ()


translator.register(Investment, InvestmentTranslationOptions)
translator.register(P2PLending, P2PLendingTranslationOptions)
translator.register(RealEstate, RealEstateTranslationOptions)
