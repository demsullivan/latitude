import Lead from '../models/lead';

export default class DynamoDB {
  constructor() {
    this.db = new AWS.DynamoDB();
    // this.db.endpoint = 'http://localhost:8001';
  }

  getAllLeads() {
    return new Promise((resolve, reject) => {
      this.db.scan({ TableName: 'Lead' }, function(err, data) {
        var leads = data['Items'].map(function(item) {
          for (var key in item) {
            if (item[key].S) item[key] = item[key].S;
            if (item[key].N) item[key] = new Number(item[key].N);
          }
          return new Lead(item);
        })
        resolve(leads);
      });
    });
  }
}
