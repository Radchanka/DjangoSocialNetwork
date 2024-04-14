document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('register-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '{% url 'gramm:activation_info' %}';
            } else {
                console.error('Error while registering:', response.statusText);
            }
        })
        .catch(error => {
            console.error('An error occurred:', error);
        });
    });
});