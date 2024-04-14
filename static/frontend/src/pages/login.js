document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(loginForm);

        fetch(loginForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '{% url 'gramm:profile' user.id %}';
            } else {
                console.error('Error while submitting the form:', response.statusText);
            }
        })
        .catch(error => {
               console.error('An error occurred:', error);
        });
    });
});