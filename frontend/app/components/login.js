export default {
  didRender() {
    this.attachEventListeners();
  },

  attachEventListeners() {
    $('#login').click(this.onLoginClick.bind(this));
  },

  onLoginClick() {
    $('#error-msg').addClass('hidden');
    this.authenticate(this.getUsername(), this.getPassword()).then(data => {
      this.userLoggedIn(data);
    }).catch(reason => {
      $('#error-msg').text(reason).removeClass('hidden');
    });
  },

  authenticate(username, password) {
    return new Promise((resolve, reject) => {
      $.ajax({
        method: "POST",
        data: { username, password },
        url: this.loginUrl,
        dataType: 'json'
      }).done((data, status, xhr) => {
        resolve(data);
      }).fail((xhr, status, err) => {
        var reason;
        if (xhr.status == 500) {
          reason = "Unknown server error.";
        } else if (xhr.status == 401) {
          reason = "Invalid username or password.";
        } else {
          reason = "Unknown error.";
        }

        reject(reason);
      });
    });
  },

  getUsername() {
    return $('#username').val();
  },

  getPassword() {
    return $('#password').val();
  }
};
