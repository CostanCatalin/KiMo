  var myHeader = { Authorization : "Token " + readCookie('token'), 'X-CSRFToken': readCookie("csrftoken")};
  var kid_id = window.location.pathname.split('/')[3];
  var markers = [];
  var map;

  function initMap() {
        var myLatLng = {lat: 42.2335399, lng: -88.33784799999999};

        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 18,
          center: myLatLng
        });

        google.maps.event.addListener(map, "click", function (event) {
            var latitude = event.latLng.lat();
            var longitude = event.latLng.lng();

            document.getElementById('latitude').value = latitude;
            document.getElementById('longitude').value = longitude;

            //console.log(latitude + "  " + longitude);
            map.panTo(new google.maps.LatLng(latitude,longitude));
        });
        getRestrictions(map);
        getPosition(map);
  };


function getKidInfo() {
$.ajax({
        type: 'GET',
        url: "/api/kid/" + kid_id,
        headers: myHeader,
        dataType: "json"
    }).done( function(resultData) {
         var first_name = titleCase(resultData['first_name']) ;
         document.getElementById('kid-name').textContent = first_name + " " + titleCase(resultData['last_name']);
         document.getElementById('first-name').textContent = first_name;
         var birth_date = new Date(resultData['birth_date']);
         document.getElementById('birth-date').textContent = formatDate(birth_date);
         document.getElementById('age').textContent = getAge(birth_date);
    });
    getActivity();
}

function getRestrictions(map) {
$.ajax({
        type: 'GET',
        url: "/api/restriction/?kid=" + kid_id,
        headers: myHeader,
        dataType: "json"
    }).done( function(resultData) {
         for (i = 0; i < resultData.count; i++) {
            var restriction = resultData.results[i];
            var centerCoord = new google.maps.LatLng(restriction.latitude, restriction.longitude);


            radius = new google.maps.Circle({
                map: map,
                radius: restriction.distance,
                center: centerCoord,
                fillColor: '#777',
                fillOpacity: 0.1,
                strokeColor: '#AA0000',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                draggable: false,    // Dragable
                editable: false     // Resizable
            });

         }
    });
}

function addRestriction() {
    $.ajax({
        type: 'POST',
        url: "/api/restriction/",
        headers: myHeader,
        data : {'kid' : kid_id, 'latitude' : $("#latitude").val(),'longitude' :$("#longitude").val(), distance : $("#distance").val()},
        dataType: "json"
    }).fail( function(resultData) {

     document.getElementById('latitude_error').innerHTML = '';
     document.getElementById('longitude_error').innerHTML = '';
     document.getElementById('distance_error').innerHTML = '';

     var listData = JSON.parse(resultData.responseText);
     for (obj in listData) {
             document.getElementById(obj + '_error').innerHTML = ('*' + listData[obj]);
     }
     });
}

function getPosition(map) {
 setInterval(function() {
$.ajax({
        type: 'GET',
        url: "/api/location?kid=" + kid_id + "&limit=1",
        headers: myHeader,
        dataType: "json"
    }).done( function(resultData) {

        if (resultData.count > 0) {
            var position = resultData.results[0];
            var posCoord = new google.maps.LatLng(position.latitude, position.longitude);
            deleteMarkers();

            addMarker(posCoord);
            showMarkers();
            map.panTo(posCoord);
            setStreet("child-pos", position.latitude, position.longitude);
        } else {
            document.getElementById("child-pos").textContent = "Unknown location";
            document.getElementById("child-pos").textContent = "Unknown location";
            alert("Kid is nowhere to be found");
        }
    })
    }, 5000);

}

function getActivity() {
    $.ajax({
        type: 'GET',
        url: "/api/notification/?limit=10",
        headers: myHeader,
        dataType: "json"
    }).done( function(resultData) {
          console.log(resultData.results);
    });
}


function formatDate(date) {
    var month_names = new Array ( );
    month_names[month_names.length] = "Jan";
    month_names[month_names.length] = "Feb";
    month_names[month_names.length] = "March";
    month_names[month_names.length] = "Apr";
    month_names[month_names.length] = "May";
    month_names[month_names.length] = "June";
    month_names[month_names.length] = "July";
    month_names[month_names.length] = "Aug";
    month_names[month_names.length] = "Sept";
    month_names[month_names.length] = "Oct";
    month_names[month_names.length] = "Nov";
    month_names[month_names.length] = "Dec";

   return date.getDate() + " " + month_names[date.getMonth()] +  " " + date.getFullYear();
}

function getAge(date) {
    var age = '';
    var current_date = new Date();

    var years = current_date.getFullYear() - date.getFullYear();
    if (years > 0) {
        age += years + " year";
        if (years > 1) {
            age += "s";
        }
    }

    var months = current_date.getMonth() - date.getMonth();

    if (months > 0) {
        if (years > 0) {
            age += " and ";
        }
        age += months + " month";
        if (months > 1) {
            age += "s";
        }
    }

    return "(" + age + " old)";
}

function titleCase(string) {
 return string.charAt(0).toUpperCase() + string.slice(1);
}

function setStreet(id, latitude, longitude) {
    $.ajax({
        type: 'GET',
        url: "http://maps.googleapis.com/maps/api/geocode/json",
        data: {'latlng' : latitude + ',' + longitude},
        dataType: "json"
    }).done(function(data) {
        if(data.results.length > 0) {
            var address = data['results'][0];
            document.getElementById(id).textContent = address.formatted_address;
        } else {
            document.getElementById(id).textContent = "Unknown street";
        }
    });
}

function addMarker(location) {
   var marker = new google.maps.Marker({
       position: location,
       map: map
   });
   markers.push(marker);
}

function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
       markers[i].setMap(map);
    }
}

function clearMarkers() {
   setMapOnAll(null);
}

function showMarkers() {
   setMapOnAll(map);
}

function deleteMarkers() {
   clearMarkers();
   markers = [];
}
