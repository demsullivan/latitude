export default class Lead {
  get attributes() {
    return {
      lead_url: 'S',
      date_created: 'N',
      source_name: 'S',
      title: 'S',
      description: 'S',
      contact_name: 'S',
      contact_email: 'S',
      website: 'S',
      twitter: 'S',
      linkedin: 'S',
      deleted: 'BOOL'
    };
  }

  constructor(attrs) {
    Object.assign(this, attrs);
  }
}
