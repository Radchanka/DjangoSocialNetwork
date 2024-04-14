console.log('This is the profile page script.');

document.addEventListener('DOMContentLoaded', function() {
    const profileNameElement = document.getElementById('profileName');
    const profileBioElement = document.getElementById('profileBio');

    console.log(profileNameElement);
    console.log(profileBioElement);

    if (profileNameElement && profileBioElement) {
        profileNameElement.innerHTML = '<h2>' + profileNameElement.textContent + '</h2>';
        profileBioElement.innerHTML = '<p>' + profileBioElement.textContent + '</p>';
    } else {
        console.error('One or more profile elements not found.');
    }
});