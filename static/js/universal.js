// Create map centered on Zurich
var map = L.map('map').setView([47.3769, 8.5417], 20); // Zurich coordinates: [latitude, longitude]

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Get latitude and longitude parameters from the URL
var urlParams = new URLSearchParams(window.location.search);
var latitude = parseFloat(urlParams.get('latitude'));
var longitude = parseFloat(urlParams.get('longitude'));

// Check if latitude and longitude are valid
if (!isNaN(latitude) && !isNaN(longitude)) {
    console.log('Latitude:', latitude);
    console.log('Longitude:', longitude);

    // Add marker for provided latitude and longitude
    L.marker([latitude, longitude]).addTo(map)
        .bindPopup("Popup content here")
        .openPopup();
} else {
    console.error('Invalid latitude or longitude provided.');
}