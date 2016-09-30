import logging
import xml.etree.ElementTree as ET
import urllib2
from datetime import datetime
import time

from stores.models import Lead
from parsers.base import BaseParser

logger = logging.getLogger('latitude.rss')

def child_attr(el, selector, attr, ns=None):
    child_el = el.find(selector, ns)
    if child_el is not None:
        return child_el.get(attr)
    else:
        return None

class RSSParser(BaseParser):
    def __init__(self):
        self.ns = {'atom': 'http://www.w3.org/2005/Atom'}
        self.date_formats = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"]
        super(RSSParser, self).__init__()

    def entry_to_lead_for_source(self, source):
        def entry_to_lead(entry):
            url = child_attr(entry, 'atom:link', 'href', self.ns)
            title = entry.find('atom:title', self.ns).text
            description = entry.find('atom:content', self.ns).text

            date_string = entry.find('atom:updated', self.ns).text
            if date_string.endswith('+00:00'):
                date_string = date_string[:-6]

            for fmt in self.date_formats:
                try:
                    date_created = int(time.mktime(datetime.strptime(date_string, fmt).timetuple()))
                except ValueError:
                    pass
                else:
                    break


            if url and title:
                logger.info("Converting RSS entry to lead for URL {}".format(url))
                return Lead(lead_url=url, date_created=date_created, source_name=source.source_name, title=title,
                            description=description, contact_name='n/a', contact_email='n/a',
                            website='n/a', twitter='n/a', linkedin='n/a')
            else:
                return None

        return entry_to_lead

    def get_leads(self, source, title_filter=None, content_filter=None):
        logger.info('Grabbing RSS from {}'.format(source.source_url))

        try:
            response = urllib2.urlopen(source.source_url)
        except Exception, e:
            logger.error("Error in request for RSS feed: {}".format(str(e)))
            return []

        tree = ET.parse(response)
        root = tree.getroot()

        return map(self.entry_to_lead_for_source(source), root.findall('atom:entry', self.ns))
