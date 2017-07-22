import json
import requests
from datetime import datetime
from . import crawler
from ..job import Job


@crawler.route('/github', methods=['GET'])
def crawl_github():
    """Crawls for jobs at github."""
    get_items()
    return 'Done'


def get_document(url, payload):
    """
    Load content from url and return a query enabled document. A dictionary
    of get parameters can be set in payload.
    """
    request = requests.get(url, params=payload)
    return json.loads(request.text)


def get_items():
    page = 0

    while True:
        document = get_document(base_url(), {'page': page})

        if not len(document):
            break

        print 'Scraping page ' + str(page)

        for element in document:
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
    return 'https://jobs.github.com/positions.json'


def item_updated(element):
    return item_created(element)


def item_created(element):
    return datetime.strptime(element['created_at'], '%a %b %d %H:%M:%S %Z %Y')


def item_provider():
    return 'github'


def item_link(element):
    return element['url']


def item_author(element):
    return element['company']


def item_location(element):
    return element['location']


def item_title(element):
    return element['title']


def item_description(element):
    return element['description']
