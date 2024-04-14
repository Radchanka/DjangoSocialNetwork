document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('login-btn').addEventListener('click', function() {

        var loginUrl = this.getAttribute('data-login-url');
        window.location.href = loginUrl;
    });


    document.getElementById('register-btn').addEventListener('click', function() {

        var registerUrl = this.getAttribute('data-register-url');
        window.location.href = registerUrl;
    });
});