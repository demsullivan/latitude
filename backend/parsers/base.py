import time
from datetime import datetime

class BaseParser(object):
    time_range_seconds = 43200 # 12 hours

    def __init__(self):
        self.now = time.mktime(datetime.now().timetuple())

    def lead_filter(self, lead):
        return lead is not None and (self.now - lead.date_created) < self.time_range_seconds

    def get_lead_list(self, source, params={}):
        return filter(self.lead_filter, self.get_leads(source, **params))
