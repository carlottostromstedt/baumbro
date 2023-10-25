document.addEventListener("DOMContentLoaded", function(){
    let locationButton = document.querySelector("#locationButton")
    let locationDisplay = document.querySelector("#locationDisplay")

    function getLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
      } else { 
        locationDisplay.innerHTML = "Geolocation is not supported by this browser.";
      }
    }
    
    function showPosition(position) {
      locationDisplay.innerHTML = "Latitude: " + position.coords.latitude + 
      "<br>Longitude: " + position.coords.longitude;
    }

    locationButton.addEventListener("click", function(){
        getLocation();
    })
});


document.addEventListener("DOMContentLoaded", function(){
  let sendCoordinatesButton = document.querySelector("#send_coordinates");
  let userLatInput = document.querySelector("#user_lat");
  let userLonInput = document.querySelector("#user_lon");

  function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    } else { 
      userLatInput.value = "Geolocation is not supported by this browser.";
      userLonInput.value = "Geolocation is not supported by this browser.";
    }
  }
  
  function showPosition(position) {
    userLatInput.value = position.coords.latitude;
    userLonInput.value = position.coords.longitude;
  }

  sendCoordinatesButton.addEventListener("click", function(){
      getLocation();
  })
});
