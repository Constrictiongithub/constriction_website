from imagekit import ImageSpec
from imagekit import register
from imagekit.processors import Thumbnail
from pilkit.processors import Anchor


class InvestmentCardThumbnail(ImageSpec):
    processors = [Thumbnail(999, 400, crop=False, upscale=True)]
    format = 'JPEG'
    options = {'quality': 75}


class InvestmentDetailThumbnail(ImageSpec):
    processors = [Thumbnail(400, 999, crop=False, upscale=False)]
    format = 'JPEG'
    options = {'quality': 75}


register.generator('constriction.investments:card', InvestmentCardThumbnail)
register.generator('constriction.investments:detail', InvestmentDetailThumbnail)
