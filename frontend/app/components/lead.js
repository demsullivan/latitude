import config from '../config';
import leadTemplate from '../templates/lead.hbs';

export default {
    didRender() {
      this.attachEventListeners();
    },

    attachEventListeners() {
      $(`#toggle-${this.id}`).click(this.onToggleClick.bind(this));
      $(`#refresh-${this.id}`).click(this.onRefreshClick.bind(this));
      $(`#save-${this.id}`).click(this.onSaveClick.bind(this));
      $(`#remove-${this.id}`).click(this.onRemoveClick.bind(this));
    },

    onToggleClick() {
      $(`#lead-${this.id}`).find('.description').toggleClass('hidden');
      $(`#toggle-${this.id}`).toggleClass('glyphicon-collapse-down').toggleClass('glyphicon-expand');
    },

    onRefreshClick(ev) {
      var target = $(ev.target);
      if (!target.hasClass('spinner')) {
        target.toggleClass('spinner');

        $.ajax({
          method: 'POST',
          url: `${config.apiUrl}/update`,
          data: { lead_url: this.lead.lead_url, date_created: this.lead.date_created },
        }).done(data => {
          this.lead = JSON.parse(data);
          $(`#lead-${this.id}`).replaceWith(leadTemplate(this));
        }).fail((xhr, status, err) => {
          debugger;
        }).always(() => {
          target.toggleClass('spinner');
        });
      }

      console.log('refresh clicked');
    },

    onSaveClick(ev) {
      console.log('save clicked');
    },

    onRemoveClick(ev) {
      console.log('remove clicked');
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
