import logging
import re

from .utils import check_skip
from .utils import create_investment
from .utils import extract_data
from .utils import get_id
from .utils import normalize_meta
from .utils import normalize_number
from .utils import parse_markup_in_url
from .utils import scrape_page

logger = logging.getLogger("constriction.scrapers")

LANG = "it"
CATEGORY = "immobili"
SOURCE = "exploresardinia"
THOUSAND_SEP = "."
CURRENCY = "EUR"
PRICE_REGEXP = re.compile(r"([\d.]+)")
SURFACE_REGEXP = re.compile(r"([\d.]+)")
BASE_URL = "http://www.exploresardinia.it/immobili"

SELECTORS = {"title": "#center > table:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(1) > b",
             "price": "#center .prezzo",
             "description": "#center > table:nth-of-type(2) > tr:nth-of-type(1) > td:nth-of-type(1)",
             "images": "#thumbs a@href",
             "meta": {"#opzioni tr": {
                 "title": "td:nth-of-type(1)",
                 "value": "td:nth-of-type(2)",
             }},
             }


def scrape_site(noupdate):
    """ Scrapes the needed pages of the site to extract investments
    """
    count = 0
    for page in range(0, 1000, 10):
        url = "{base}/index?ricerca=1&motivazione=1&per_page={page}".format(base=BASE_URL, page=page)
        for url in scrape_page(url, "#center .dettagli a"):
            count += 1
            if check_skip(noupdate, SOURCE, url):
                yield None
                continue
            investment = scrape_investment(url)
            if not investment:
                logger.warning("Ended parsing %d investment on %d page" % (count, page))
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
    result["url"] = url
    result["title"] = re.sub(r" - .-.{3}-.$", "", result["title"])
    result["title"] = result["title"].replace("-", " ")
    if "meta" in result:
        result["meta"] = normalize_meta(result["meta"])
        if "localita'" in result["meta"]:
            result["address"] = result["meta"]["localita'"]
        if "totale m\u00b2 comm" in result["meta"]:
            result["surface"] = normalize_number(result["meta"]["totale m\u00b2 comm"], SURFACE_REGEXP, THOUSAND_SEP)
    if "price" in result:
        result["currency"] = CURRENCY
        result["price"] = normalize_number(result["price"], PRICE_REGEXP, THOUSAND_SEP)
    if "description" in result:
        result["description"] = result["description"].replace("Dettagli", "", 1)
    return result


def save_investment(item):
    return create_investment(item, CATEGORY, SOURCE, LANG)


"""
META
{  
   "vani":"10",
   "bagni":"5",
   "camere":"3",
   "localita'":"Cagliari - Quartiere del Sole/Poetto",
   "totale m\u00b2 comm":"750",
   "distanza dal mare":"0 m"
}
"""
