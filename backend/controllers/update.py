import web
import json

from utils import find_class
from stores.models import Lead, Source
from .application import ApplicationController

class UpdateLeadController(ApplicationController):
    def POST(self):
        super(UpdateLeadController, self).POST()
        params = web.input()

        lead = self.store.get_item(Lead, dict(lead_url=params.lead_url, date_created=int(params.date_created)))
        source = self.store.get_item(Source, dict(source_name=lead.source_name))

        parser = find_class(source.parser)()
        lead = parser.populate_lead(lead)

        self.store.update(lead)

        return json.dumps(lead._asdict())
