import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from . import crawler
from .countries import country_list
from ..job import Job


@crawler.route('/stackoverflow', methods=['GET'])
def crawl_stackoverflow():
    """Crawls for jobs at stackoverflow."""
    get_items()
    return 'Done'


def get_document(url, payload):
    """
    Load content from url and return a query enabled document. A dictionary
    of get parameters can be set in payload.
    """
    request = requests.get(url, params=payload)
    return BeautifulSoup(request.text, 'xml')


def get_items():
    for country in country_list:
        print 'Scraping country ' + country

        document = get_document(base_url(), {'l': country})
        selection = document.select('rss > channel item')

        for element in selection:
            link = item_link(element)
            job = Job.query.filter_by(link=link).first()

            if job:
                Job.update(
                    job, job.etag, '1', item_updated(element),
                    item_created(element), item_provider(), item_link(element),
                    item_author(element), item_location(element),
                    item_title(element), item_description(element))
            else:
                Job.create(
                    None, '1', item_updated(element), item_created(element),
                    item_provider(), item_link(element), item_author(element),
                    item_location(element), item_title(element),
                    item_description(element))


def base_url():
    return 'https://stackoverflow.com/jobs/feed'


def item_updated(element):
    raw_updated = re.search(
        '<a10:updated>(.*)</a10:updated>', element.prettify(),
        re.DOTALL).group(1).strip()
    updated = datetime.strptime(raw_updated, '%Y-%m-%dT%H:%M:%SZ')
    return updated


def item_created(element):
    raw_created = element.find('pubDate').string.strip()
    created = datetime.strptime(raw_created, '%a, %d %b %Y %H:%M:%S Z')
    return created


def item_provider():
    return 'stackoverflow'


def item_link(element):
    return element.find('link').string.strip()


def item_author(element):
    author = ''

    try:
        author = re.search(
            '<a10:author>.*<a10:name>(.*)</a10:name>.*</a10:author>',
            element.prettify(), re.DOTALL).group(1).strip()
    except Exception as e:
        pass

    return author


def item_location(element):
    return element.find('location').string.strip()


def item_title(element):
    return element.find('title').string.strip()


def item_description(element):
    return element.find('description').string.strip()
