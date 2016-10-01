import config from '../config';
import leadTemplate from '../templates/lead.hbs';

function promiseClick(promiseFunction) {
  function eventHandler(ev) {
    var target = $(ev.target);
    if (!target.hasClass('spinner')) {
      target.toggleClass('spinner');
    }

    promiseFunction(ev).then(() => {
      target.toggleClass('spinner');
    }).catch(() => {
      target.toggleClass('spinner');
      target.addClass('failed');
    });
  }

  return eventHandler;
}

export default {
    didRender() {
      this.attachEventListeners();
    },

    attachEventListeners() {
      $(`#toggle-${this.id}`).click(promiseClick(this.onToggleClick.bind(this)));
      $(`#refresh-${this.id}`).click(promiseClick(this.onRefreshClick.bind(this)));
      $(`#save-${this.id}`).click(promiseClick(this.onSaveClick.bind(this)));
      $(`#remove-${this.id}`).click(promiseClick(this.onRemoveClick.bind(this)));
    },

    onToggleClick() {
      $(`#lead-${this.id}`).find('.description').toggleClass('hidden');
      $(`#toggle-${this.id}`).toggleClass('glyphicon-collapse-down').toggleClass('glyphicon-expand');
    },

    onRefreshClick(ev) {
      return new Promise((resolve, reject) => {

        $.ajax({

          method: 'POST',
          url: `${config.apiUrl}/update`,
          data: { lead_url: this.lead.lead_url, date_created: this.lead.date_created },

        }).done(data => {

          this.lead = JSON.parse(data);
          $(`#lead-${this.id}`).replaceWith(leadTemplate(this));
          this.didRender();
          resolve();

        }).fail((xhr, status, err) => {

          reject();

        });

      });
    },

    onSaveClick(ev) {
      console.log('save clicked');
    },

    onRemoveClick(ev) {
      return new Promise((resolve, reject) => {

        $.ajax({

          method: 'POST',
          url: `${config.apiUrl}/delete`,
          data: { lead_url: this.lead.lead_url, date_created: this.lead.date_created }

        }).done(() => {

          var leadEl = $(`#lead-${this.id}`);
          leadEl.addClass('transparent');
          leadEl.one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', () => {
            leadEl.remove();
          });

          resolve();

        }).fail(() => {

          reject();

        });

      });
    },

    hasAttribute(attr) {
      return this.lead[attr] !== 'n/a';
    },

    humanizedTimestamp() {
      return new Date(this.lead.date_created*1000).toString();
    },

    hasName() {
      return this.hasAttribute('contact_name');
    },

    hasEmail() {
      return this.hasAttribute('contact_email');
    },

    hasWebsite() {
      return this.hasAttribute('website');
    },

    hasTwitter() {
      return this.hasAttribute('twitter');
    },

    hasLinkedIn() {
      return this.hasAttribute('linkedin');
    }
}
