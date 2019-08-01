
from contextlib import closing
import html
from io import BytesIO
import json
import logging
import re

from bs4 import BeautifulSoup
from cache_memoize import cache_memoize
from django.conf import settings
from django.utils.text import slugify
from google.cloud import translate
from google.oauth2 import service_account
from investments.models import RealEstate
from investments.models import InvestmentImage
import requests

LANGUAGES = [lang[0] for lang in settings.LANGUAGES]
CLEAN_META = re.compile('[(){}<>.:;\n\t\r]')
logger = logging.getLogger("constriction.scrapers")
translator = translate.Client(credentials=settings.GS_CREDENTIALS)

def get_url(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    if url == "#":
        return
    if url.startswith("//"):
        url = "https:" + url
    try:
        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}
        with closing(requests.get(url, stream=True, headers=headers)) as resp:
            if is_good_markup(resp):
                return resp.content
            else:
                return None

    except requests.exceptions.RequestException as e:
        logger.error('Requests to {0} : {1} failed'.format(url, str(e)))
        return None

def get_picture(url):
    """ Downloads a picture and returns the content
    """
    if url.startswith("//"):
        url = "https:" + url
    try:
        with closing(requests.get(url, stream=True)) as resp:
            if is_good_image(resp):
                output = BytesIO()
                output.write(resp.content)
                return output
            else:
                return None
    except requests.exceptions.RequestException as e:
        logger.error('Requests to {0} : {1} failed'.format(url, str(e)))
        return None


def is_good_image(resp):
    """
    Returns True if the response seems to be an image, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('image') > -1)


def is_good_markup(resp):
    """
    Returns True if the response seems to be HTML or XML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and (content_type.find('html') > -1 or content_type.find('xml') > -1))



def parse_markup_in_url(url, parser='html.parser'):
    """ Gets an url, fetches it and returns a bs4 parsed object
    """
    raw_markup = get_url(url)
    if not raw_markup:
        return None
    markup = BeautifulSoup(raw_markup, parser)
    return markup


def scrape_page(url, selector):
    """ Scrapes an url yelding as output each link url matching selector
    """
    html = parse_markup_in_url(url)
    if not html:
        logger.warning("Empty html for: %s" % url)
        return []
    investment_links = html.select(selector)
    if not investment_links:
        logger.warning("No links for: %s" % url)
        return []
    for investment_link in investment_links:
        if not investment_link:
            logger.warning("Empty investment links in page %s" % url)
            continue
        investment_url = investment_link.get("href", "")
        if not investment_url:
            logger.warning("Empty investment link")
            continue
        yield investment_url


def _extract_dict(parent, value):
    """ get the interesting selector and calls again _extract_data on children
    """
    results = []
    for selector, selectors_dict in value.items():
        elements = parent.select(selector)
        for element in elements:
            if not element:
                continue
            results.append(extract_data(selectors_dict, element))
    return results

def _get_value(element, attr):
    """ get the interesting value. Can be an attr, text or outer html
    """
    if attr:
        if attr == "html":
            return str(element).strip()
        return element.get(attr)
    return element.text.strip()

def _extract_elements(html, selector):
    """ Extracts elements by selector. Can return string o list
    """
    attr = ""
    if "@" in selector:
        selector, attr = selector.split("@")
    elements = html.select(selector)
    if type(elements) is list:
        if len(elements) > 1:
            logger.info("List result: %s", selector,)
            return [_get_value(e, attr) for e in elements]
        elif len(elements) == 1:
            logger.info("Single result: %s", selector,)
            return _get_value(elements[0], attr)
    logger.info("Failed to extract: %s", selector,)
    return ""

def extract_data(selectors_dict, html):
    """ Extracts the selectors structure dict data into a dict
    """
    result = {}
    if not html:
        logger.warning("No html to extract")
        return result
    for name, selector in selectors_dict.items():
        if type(selector) is dict:
            logger.info("Extracting dict: %s", name,)
            result[name] = _extract_dict(html, selector)
        else:
            logger.info("Extracting selector: %s", name,)
            result[name] = _extract_elements(html, selector)
    return result


def get_id(base, url, extension=False):
    name = [u for u in url.strip("/").split("/") if u][-1]
    name = name[-50:]
    if extension and "." in name[-5:]:
        name,extension = name.rsplit(".", 1)
        extension = "." + extension
    else:
        extension = ""
    return slugify(base + "_" + name) + extension


def normalize_number(number, regexp, thousand_sep):
    number = regexp.search(number)
    if not number:
        return None
    number = number.group(1)
    number = number.replace(thousand_sep, "").strip()
    return int(number)


def create_investment(item, category, source, lang):
    """ Replaces adds and deletes investments in Django models
    """
    try:
        investment = RealEstate.objects.get(identifier=item["id"])
        logger.info("Updating object %s" % item["id"])
    except RealEstate.MultipleObjectsReturned:
        logger.error("There should be max 1 investment with idetifier %s" % item["id"])
        return
    except RealEstate.DoesNotExist:
        logger.info("Creating object %s" % item["id"])
        investment = RealEstate(identifier=item["id"])
    title = item.get("title", "No title")
#    meta = [i for k, v in item.get("meta", {}).items() for i in [k, v]]
#    tags = item.get("tags", [])
    desc = item.get("description", None)
    for dst_lang in LANGUAGES:
        trans_title = translation(lang, dst_lang, title)
        trans_title = html.unescape(trans_title)
        trans_slug = slugify(trans_title)
        trans_desc = translation(lang, dst_lang, desc)
#        trans_metas = translation(lang, dst_lang, meta)
#        if trans_metas:
#            trans_metas = [html.unescape(t) for t in trans_metas]
#            trans_metas = dict(zip(trans_metas[::2], trans_metas[1::2]))
#        trans_tags = translation(lang, dst_lang, tags)
        setattr(investment, "title_" + dst_lang, trans_title)
        setattr(investment, "slug_" + dst_lang, trans_slug)
        setattr(investment, "description_" + dst_lang, trans_desc)
#        setattr(investment, "meta_" + dst_lang, trans_metas)
#        setattr(investment, "tags_" + dst_lang, trans_tags)
    investment.address = item.get("address", None)
    investment.url = item.get("url", None)
    investment.price = item.get("price", None)
    investment.currency = item.get("currency", None)
    investment.surface = item.get("surface", None)
    investment.category = category
    investment.source = source
    investment.raw_data = json.dumps(item)
    investment.save()
    if not investment.images.count():
        # I only save the first image
        images = item.get("images", [])
        if images:
            image = create_image(images[0], source)
            if image and not image.investments.filter(identifier=investment.identifier).exists():
                image.investments.add(investment)
    return investment

def create_image(image_url, source):
    identifier = get_id(source, image_url, extension=True)
    try:
        image_obj = InvestmentImage.objects.get(identifier=identifier)
    except InvestmentImage.MultipleObjectsReturned:
        logger.error("There should be max 1 image with idetifier %s" % identifier)
        return
    except InvestmentImage.DoesNotExist:
        image = get_picture(image_url)
        if not image:
            return
        logger.warning("Creating image %s" % identifier)
        image_obj = InvestmentImage(identifier=identifier)
        image_obj.image.save(identifier, image, save=True)
        image_obj.save()
    return image_obj


def normalize_meta(metas):
    results = {}
    for meta in metas:
        label = ""
        title = meta["title"].strip()
        value = meta["value"].strip()
        if "label" in meta:
            label = meta["label"].strip()
            value += label
        title = CLEAN_META.sub('', title).lower()
        value = CLEAN_META.sub('', value)
        value = re.sub(r' +', ' ', value)
        if title and value:
            results[title] = value
    return results


def check_skip(noupdate, source, url):
    identifier = get_id(source, url)
    if noupdate and RealEstate.objects.filter(identifier=identifier).count():
        logger.warning("Skipping investment %s" %(identifier))
        return True
    return False


def translation(from_lang, to_lang, content):
    if from_lang == to_lang or not content:
        return content
    trans = translator.translate(content, source_language=from_lang, target_language=to_lang)
    if type(trans) is list:
        return [t["translatedText"] for t in trans]
    if "translatedText" in trans:
        return trans["translatedText"]
    if "data" in trans and "translations" in trans["data"]:
        return [t["translatedText"] for t in trans["data"]["translations"]]
