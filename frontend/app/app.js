import Store from './stores/dynamodb';
import config from './config';

import leadTemplate from './templates/lead.hbs';
import leadComponent from './components/lead';

import loginTemplate from './templates/login.hbs';
import loginComponent from './components/login';

var applicationEl = $('#application');


function templateWithComponent(template, component, context) {
  return template(Object.assign(context, component));
}

function displayLeadList() {
  var store = new Store();
  store.getAllLeads().then(data => {
    if (data.length == 0) {
      applicationEl.text("No leads found in the database.");
    } else {
      data.forEach(item => {
        applicationEl.append(templateWithComponent(leadTemplate, leadComponent, { lead: item }));
      });
    }
  });
}

function userLoggedIn(data) {
  AWS.config.update({
    accessKeyId: data.aws_access_key_id,
    secretAccessKey: data.aws_secret_access_key,
    region: 'us-east-1'
  });

  applicationEl.empty();
  displayLeadList();
}

function main() {
  var ctx = { userLoggedIn, loginUrl: config.loginUrl };
  applicationEl.append(templateWithComponent(loginTemplate, loginComponent, ctx));
  loginComponent.didRender.bind(Object.assign(ctx, loginComponent))();
}

main();
