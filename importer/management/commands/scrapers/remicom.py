import logging
import re

from investments.models import Business

from .utils import (check_skip, create_investment, extract_data, get_id,
                    normalize_meta, normalize_number, parse_markup_in_url,
                    scrape_page)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

LANG = "fr"
COUNTRIES = ["CH", ]
TYPE = Business
SOURCE = "remicom"
THOUSAND_SEP = "'"
CURRENCY = "CHF"
PRICE_REGEXP = re.compile(r"([\d']+)")
SURFACE_REGEXP = re.compile(r"([\d]+)")
BASE_URL = "http://remicom.com"

SELECTORS = {"title": "h2.title_assets",
             "description": "#details",
             "images": "img.assets_v2_picture@src",
             "meta": {".tech_detail_asset": {
                 "title": ".tech_detail_asset_td_h",
                 "value": ".tech_detail_asset_td_c",
             }},
             }


def scrape_site(noupdate):
    """ Scrapes the needed pages of the site to extract investments
    """
    count = 0
    for page in range(1, 100):
        url = "{base}/en/our-offers?page={page}".format(base=BASE_URL, page=page)
        for url in scrape_page(url, ".prodBlock .btn-container a"):
            count += 1
            if check_skip(noupdate, SOURCE, url):
                yield None
                continue
            investment = scrape_investment(url)
            if not investment:
                logger.warning("Ended parsing %d investment on page %d" % (count, page))
                break
            logger.warning(
                "Parsing investment number %d on page %d: %s" % (count, page, url))
            yield investment
        if count:
            logger.info("Parsed %d investment on page %d" % (count, page))
        else:
            logger.warning("Stopped parsing on page %d" % page)


def scrape_investment(url):
    """ Scrapes a single investments
    """
    html = parse_markup_in_url(BASE_URL + url)
    result = extract_data(SELECTORS, html)
    if not result:
        logger.error("Empty result for %s" % url)
    result["url"] = BASE_URL + url
    result["id"] = get_id(SOURCE, url)
    result["title"] = re.sub(r"\(.*?\)$", "", result["title"])
    price = None
    if "images" in result and result["images"]:
        result["images"] = [BASE_URL + result["images"], ]
    if "meta" in result:
        metas = []
        for meta in result["meta"]:
            for title,value in dict(zip(meta["title"], meta["value"])).items():
                if title and value:
                    if title == "Price":
                        price = value
                    else:
                        metas.append({"title": title, "value": value})
        result["meta"] = normalize_meta(metas)
        if "surface" in result["meta"]:
            result["surface"] = normalize_number(result["meta"]["surface"], SURFACE_REGEXP, THOUSAND_SEP)
    # TODO: no price... What to do? Get rent price maybe?
    if price:
        result["currency"] = CURRENCY
        result["price"] = normalize_number(price, PRICE_REGEXP, THOUSAND_SEP)

    if "description" in result:
        result["description"] = "<p>" + "</p><p>".join(result["description"].split("\r\n")) + "</p>"
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
