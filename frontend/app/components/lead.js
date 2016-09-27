export default {
    hasAttribute(attr) {
      return this.lead[attr] !== 'n/a';
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
