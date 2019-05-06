from investments.models import Investment
from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import translator


class InvestmentTranslationOptions(TranslationOptions):
    fields = ('title', 'slug', 'description', 'meta', 'tags')


translator.register(Investment, InvestmentTranslationOptions)
