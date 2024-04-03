// Create map centered on Zurich
var urlParams = new URLSearchParams(window.location.search);
var latitude = parseFloat(urlParams.get('latitude'));
var longitude = parseFloat(urlParams.get('longitude'));

var map = L.map('map').setView([latitude, longitude], 20); // Zurich coordinates: [latitude, longitude]

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Get latitude and longitude parameters from the URL


// Check if latitude and longitude are valid
if (!isNaN(latitude) && !isNaN(longitude)) {
    console.log('Latitude:', latitude);
    console.log('Longitude:', longitude);

    // Add marker for provided latitude and longitude
    L.marker([latitude, longitude]).addTo(map)
        .bindPopup("You are here")
        .openPopup()
        ._icon.classList.add("huechange");
} else {
    console.error('Invalid latitude or longitude provided.');
}