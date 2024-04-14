$(document).ready(function () {
    $('#id_images-TOTAL_FORMS').attr('type', 'hidden');
    $('#id_images-0-image').removeAttr('required');
    $('#id_images-0-image').attr('multiple', 'true');

    $('#id_images-0-image').on('change', function () {
        var input = this;
        var previewContainer = $('#preview-container');

        previewContainer.empty();

        for (var i = 0; i < input.files.length; i++) {
            var reader = new FileReader();
            reader.onload = function (e) {
                var image = $('<img>').attr('src', e.target.result).addClass('img-thumbnail mx-2');
                previewContainer.append(image);
            };
            reader.readAsDataURL(input.files[i]);
        }
    });
});