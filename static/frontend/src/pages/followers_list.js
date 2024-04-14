document.addEventListener('DOMContentLoaded', function() {

    var followersList = document.querySelectorAll('.list-group-item');


    var followerCountElement = document.createElement('p');
    followerCountElement.textContent = 'Total Followers: ' + followersList.length;
    followerCountElement.classList.add('text-center');
    document.body.insertBefore(followerCountElement, document.querySelector('.container'));

});