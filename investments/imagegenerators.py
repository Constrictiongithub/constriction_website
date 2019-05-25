from imagekit import ImageSpec
from imagekit import register
from imagekit.processors import Thumbnail


class InvestmentCardThumbnail(ImageSpec):
    processors = [Thumbnail(400, 400)]
    format = 'JPEG'
    options = {'quality': 60}


class InvestmentDetailThumbnail(ImageSpec):
    processors = [Thumbnail(400, 999)]
    format = 'JPEG'
    options = {'quality': 60}


register.generator('constriction.investments:card', InvestmentCardThumbnail)
register.generator('constriction.investments:detail', InvestmentDetailThumbnail)
