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
CATEGORY = "realestate"
SOURCE = "sestrierecase"
THOUSAND_SEP = "."
CURRENCY = "EUR"
PRICE_REGEXP = re.compile(r"([\d.]+)")
SURFACE_REGEXP = re.compile(r"([\d.]+)")
BASE_URL = "https://www.sestrierecase.it"

SELECTORS = {"title": "#left-area .property-title",
             "price": "#left-area .price",
             "description": "#left-area .wpp_the_content",
             "images": "#left-area .cycle-slideshow a@href",
             "meta": {"#property_stats li": {
                 "title": ".attribute",
                 "value": ".value",
             }},
             }


def scrape_site(noupdate):
    """ Scrapes the needed pages of the site to extract investments
    """
    count = 0
    for page in range(1, 100):
        url = "{base}/feed/?paged={page}".format(base=BASE_URL, page=page)
        xml = parse_markup_in_url(url, 'xml')
        for item in xml.find_all('item'):
            count += 1
            url = item.find("link").text
            if check_skip(noupdate, SOURCE, url):
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
    result["url"] = url
    if "price" in result:
        result["currency"] = CURRENCY
        result["price"] = normalize_number(result["price"], PRICE_REGEXP, THOUSAND_SEP)
    if "meta" in result:
        result["meta"] = normalize_meta(result["meta"])
        if "indirizzo" in result["meta"]:
            result["address"] = result["meta"]["indirizzo"]
            del(result["meta"]["indirizzo"])
        elif "comune" in result["meta"]:
            result["address"] = result["meta"]["comune"]
            del(result["meta"]["comune"])
        if "superficie mq" in result["meta"]:
            result["surface"] = normalize_number(result["meta"]["superficie mq"], SURFACE_REGEXP, THOUSAND_SEP)
            del(result["meta"]["superficie mq"])
    return result


def save_investment(item):
    return create_investment(item, CATEGORY, SOURCE, LANG)



"""
META
{  
   "bagni":"2",
   "piano":"3\u00b0 e 4\u00b0 piano",
   "vista":"Piste da sci",
   "codice":"V46 11",
   "comune":"Sestriere",
   "cucina":"Abitabile",
   "locali":"3",
   "allarme":"s\u00ec",
   "cantina":"s\u00ec",
   "taverna":"no",%
   "arredato":"no",
   "mansarda":"s\u00ec",
   "soffitta":"no",
   "terrazzo":"s\u00ec",
   "categoria":"Residenziale",
   "contratto":"Vendita",
   "panoramico":"s\u00ec",
   "posto auto":"Esterno",
   "prezzo \u20ac":"\u20ac 568400",
   "impianto tv":"s\u00ec",
   "riscaldamento":"Autonomo",
   "superficie mq":"98 sq ft",
   "numero livelli":"2",
   "stato immobile":"Nuovo-in costruzione",
   "anno costruzione":"2019",
   "fascia di prezzo":"500001 - 600000",
   "giardino/cortile":"s\u00ec",
   "classe energetica":"A",
   "impianto satellitare":"s\u00ec"
}
"""
