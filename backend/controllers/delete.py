import web
from .application import ApplicationController
from stores.models import Lead

class DeleteLeadController(ApplicationController):
    def POST(self):
        super(DeleteLeadController, self).POST()
        params = web.input()
        self.store.delete_by_key(Lead, lead_url=params.lead_url, date_created=int(params.date_created))
        # lead = self.store.get_item(Lead, dict(lead_url=params.lead_url, date_created=params.date_created))
        # lead = lead._asdict()
        # lead['deleted'] = True
        # self.store.update(Lead(lead))

        return web.ok()
