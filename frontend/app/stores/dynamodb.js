import Lead from '../models/lead';
import config from '../config';

export default class DynamoDB {
  constructor() {
    this.db = new AWS.DynamoDB();
    if (config.dbEndpoint !== null) this.db.endpoint = config.dbEndpoint;
  }

  deserializeModel(item) {
    for (var key in item) {
      if (item[key].S) item[key] = item[key].S;
      if (item[key].N) item[key] = new Number(item[key].N);
      if (item[key].BOOL) item[key] = item[key].BOOL;
    }
    return item;
  }

  getAllLeads() {
    return new Promise((resolve, reject) => {
      this.db.scan({ TableName: 'Lead' }, (err, data) => {
        var leads = data['Items']
          .map(item => { return new Lead(this.deserializeModel(item)); })
          .filter(lead => { return !lead.deleted; });

        resolve(leads);
      });
    });
  }
}
