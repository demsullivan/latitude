from __future__ import absolute_import
from craigslist import CraigslistJobs
from datetime import datetime
import time
import logging
import urllib2
from urlparse import urlparse
from bs4 import BeautifulSoup

from stores.models import Lead
from parsers.base import BaseParser

logger = logging.getLogger('latitude.craigslist')

class CraigslistParser(BaseParser):
    def job_to_lead_for_source(self, source):
        def job_to_lead(job):
            title = job['name']
            url = job['url']
            date_string = job['datetime']
            date_created = int(time.mktime(datetime.strptime(date_string, "%Y-%m-%d %H:%M").timetuple()))

            logger.info("Converting Craigslist job into lead for URL {}".format(url))
            return Lead(lead_url=url, date_created=date_created, source_name=source.source_name, title=title,
                        description='n/a', contact_name='n/a', contact_email='n/a',
                        website='n/a', twitter='n/a', linkedin='n/a')

        return job_to_lead

    def populate_lead(self, lead):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        lead_dict = lead._asdict()

        try:
            req = urllib2.Request(lead.lead_url, headers={ 'User-Agent': user_agent })
            response = urllib2.urlopen(req).read()
        except Exception as e:
            logger.error("Error populating craigslist lead {}: {}".format(lead.lead_url, str(e)))
            return lead

        soup = BeautifulSoup(response, 'html.parser')
        lead_dict['description'] = str(soup.find(id='postingbody'))

        parsed_url = urlparse(lead.lead_url)
        reply_url = "{}://{}/reply{}".format(parsed_url.scheme, parsed_url.netloc, parsed_url.path.replace('.html', ''))

        logger.debug("Retrieving email info from {}".format(reply_url))
        try:
            req = urllib2.Request(reply_url, headers={ 'User-Agent': user_agent })
            reply_response = urllib2.urlopen(req).read()
        except Exception as e:
            logger.error("Error retriving contact details for craigslist lead {}: {}".format(lead.lead_url, str(e)))
            return lead

        reply_soup = BeautifulSoup(reply_response, 'html.parser')
        try:
            lead_dict['contact_email'] = reply_soup.find('div', class_='anonemail').string
        except:
            pass

        return Lead(**lead_dict)


    def get_leads(self, source, site=None, category=None, filters=None):
        jobs = CraigslistJobs(site=site, category=category, filters=filters)
        return map(self.job_to_lead_for_source(source), jobs.get_results())
