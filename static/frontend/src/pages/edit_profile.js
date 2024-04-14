$(document).ready(function () {
    $('#id_avatar').on('change', function () {
        var input = this;
        var previewContainer = $('#avatar-preview');

        previewContainer.empty();

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                var image = $('<img>').attr('src', e.target.result).addClass('img-thumbnail');
                previewContainer.append(image);
            };

            reader.readAsDataURL(input.files[0]);
        }
    });
});