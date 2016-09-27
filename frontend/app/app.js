import Store from './stores/dynamodb';
import config from './config';
import leadTemplate from './templates/lead.hbs';
import leadComponent from './components/lead';

function main() {
  AWS.config.update({
      accessKeyId: config.AWS_ACCESS_KEY_ID,
      secretAccessKey: config.AWS_SECRET_ACCESS_KEY,
      region: 'us-east-1',
      endpoint: 'http://localhost:8001'
  });

  var store = new Store();
  store.getAllLeads().then(data => {
    data.forEach(item => {
      $('#application').append(leadTemplate(Object.assign({ lead: item }, leadComponent)));
    })
  });

}

main();
