  var map;
  function initMap() {
    var myLatLng = {lat: 42.2335399, lng: -88.33784799999999};

    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 18,
      center: myLatLng
    });

    var marker = new google.maps.Marker({
      position: myLatLng,
      map: map,
      title: "Amber's Here!"
    });

    google.maps.event.addListener(map, "click", function (event) {
        var latitude = event.latLng.lat();
        var longitude = event.latLng.lng();
        console.log( latitude + ', ' + longitude );

        radius = new google.maps.Circle({map: map,
            radius: 100,
            center: event.latLng,
            fillColor: '#777',
            fillOpacity: 0.1,
            strokeColor: '#AA0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            draggable: true,    // Dragable
            editable: true      // Resizable
        });

        console.log(radius);

        // Center of map
        map.panTo(new google.maps.LatLng(latitude,longitude));

    });
  };