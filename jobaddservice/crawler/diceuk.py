import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from . import crawler
from ..job import Job


@crawler.route('/diceuk', methods=['GET'])
def crawl_diceuk():
    """Crawls for jobs at dice uk."""
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
    page = 1

    while True:
        document = get_document(base_url(), {'Page': page})
        document_link = document.select('rss > channel > link')[0].string

        if page > 1 and 'Page=' + str(page) not in document_link:
            break

        print 'Scraping page ' + str(page)

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

        page += 1


def base_url():
    return 'http://uk.dice.com/rss/all-jobs/all-locations/en/jobs-feed.xml'


def item_updated(element):
    return item_created(element)


def item_created(element):
    created = datetime.utcnow()

    try:
        raw_created = element.find('pubDate').string.strip().rsplit(' ', 1)[0]
        created = datetime.datetime.strptime(
            raw_created, '%a, %d %b %Y %H:%M:%S')
    except Exception as e:
        pass

    return created


def item_provider():
    return 'diceuk'


def item_link(element):
    return element.find('link').string.strip()


def item_author(element):
    author = ''
    description = item_description(element)

    try:
        author = re.search(
            'Advertiser : (.*)<br/>.*Location : (.*)<br/>', description,
            re.DOTALL).group(1).strip()
    except Exception as e:
        pass

    return author


def item_location(element):
    location = ''
    description = item_description(element)

    try:
        location = re.search(
            'Advertiser : (.*)<br/>.*Location : (.*)<br/>', description,
            re.DOTALL).group(2).strip()
    except Exception as e:
        pass

    return location


def item_title(element):
    return element.find('title').string.strip()


def item_description(element):
    description = ''

    try:
        description = element.find('description').string.strip()
    except Exception as e:
        pass

    return description
