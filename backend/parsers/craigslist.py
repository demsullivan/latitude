from __future__ import absolute_import
from craigslist import CraigslistJobs
from datetime import datetime
import time
import logging

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

    def get_leads(self, source, site=None, category=None, filters=None):
        jobs = CraigslistJobs(site=site, category=category, filters=filters)
        return map(self.job_to_lead_for_source(source), jobs.get_results())
