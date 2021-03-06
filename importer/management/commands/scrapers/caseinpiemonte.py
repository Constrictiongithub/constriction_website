import logging
import re

from investments.models import RealEstate

from .utils import (check_skip, create_investment, extract_data, get_id,
                    get_interest_range, normalize_meta, normalize_number,
                    parse_markup_in_url, price_range, scrape_page)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

LANG = "en"
COUNTRIES = ["IT", ]
TYPE = RealEstate
SOURCE = "caseinpiemonte"
THOUSAND_SEP = "."
CURRENCY = "EUR"
PRICE_REGEXP = re.compile(r"([\d.]+)")
SURFACE_REGEXP = re.compile(r"([\d.]+)")
BASE_URL = "https://caseinpiemonte.com/properties"

SELECTORS = {"title": ".rh_page__head .rh_page__title",
             "address": ".rh_page__head .rh_page__property_address",
             "price": ".rh_page__head .price",
             "efficency": ".energy-efficency",
             "description": ".rh_content p@html",
             "images": ".flexslider .slides li a@href",
             "tags": ".rh_property__features_wrap .rh_property__feature",
             "meta": {".rh_property__meta_wrap .rh_property__meta": {
                 "title": "h4",
                 "value": ".figure",
                 "label": ".label",
             }},
             }


def scrape_site(noupdate):
    """ Scrapes the needed pages of the site to extract investments
    """
    count = 0
    for page in range(1, 100):
        url = "{base}/page/{page}".format(base=BASE_URL, page=page)
        for url in scrape_page(url, "article.rh_list_card .rh_overlay__contents a"):
            count += 1
            if check_skip(noupdate, TYPE, SOURCE, url):
                yield None
                continue
            investment = scrape_investment(url)
            if not investment:
                logger.warning("Ended parsing %d investment on page %d" % (count, page))
                break
            logger.warning("Parsing investment number %d on page %d: %s" % (count, page, url))
            yield investment
        if count:
            logger.info("Parsed %d investment on page %d" % (count, page))
        else:
            logger.warning("Stopped parsing on page %d" %  page)


def scrape_investment(url):
    """ Scrapes a single investments
    """
    html = parse_markup_in_url(url)
    result = extract_data(SELECTORS, html)
    if not result:
        logger.error("Empty result for %s" % url)
        return
    result["id"] = get_id(SOURCE, url)
    result["url"] = "https:" + url
    if "meta" in result:
        if "efficency" in result:
            result["meta"].append({"title": "efficency", "value": result["efficency"]})
        result["meta"] = normalize_meta(result["meta"])
        if "area" in result["meta"]:
            result["surface"] = normalize_number(result["meta"]["area"], SURFACE_REGEXP, THOUSAND_SEP)
    if "price" in result:
        result["currency"] = CURRENCY
        result["price"] = normalize_number(
            result["price"], PRICE_REGEXP, THOUSAND_SEP)
        result["price"] = price_range(result["price"])
    result["interest"] = get_interest_range(COUNTRIES)
    if "description" in result:
        result["description"] = " ".join(result["description"])
    return result


def save_investment(item):
    return create_investment(item, TYPE, COUNTRIES, SOURCE, LANG)


"""
META
{  
   "superficie":"190m2",
   "prezzo di affitto":"Prezzo di affitto CHF 5'500 - Approssimativamente EUR 5'060-"
}
"""
