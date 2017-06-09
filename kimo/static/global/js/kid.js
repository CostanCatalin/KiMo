  var myHeader = { Authorization : "Token " + readCookie('token'), 'X-CSRFToken': readCookie("csrftoken")};
  var kid_id = window.location.pathname.split('/')[3];
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

        // Center of map
        map.panTo(new google.maps.LatLng(latitude,longitude));
    });
            getRestrictions();
  };

function getKidInfo() {
$.ajax({
        type: 'GET',
        url: "/api/kid/" + kid_id,
        headers: myHeader,
        dataType: "json"
    }).done( function(resultData) {
         document.getElementById('kid-name').textContent = titleCase(resultData['first_name']) + " " + titleCase(resultData['last_name']);
         document.getElementById('first-name').textContent = resultData['first_name'];
         var birth_date = new Date(resultData['birth_date']);
         document.getElementById('birth-date').textContent = formatDate(birth_date);
          document.getElementById('age').textContent = getAge(birth_date);
    });
}

function getRestrictions() {
$.ajax({
        type: 'GET',
        url: "/api/restriction/",
        headers: myHeader,
        dataType: "json"
    }).done( function(resultData) {
         for (i = 0; i < resultData.count; i++) {
            var restriction = resultData.results[i];
            console.log(restriction);
            if (restriction.kid = kid_id) {
                radius = new google.maps.Circle({map: map,
                    radius: restriction.distance,
                    center: event.latLng,
                    fillColor: '#777',
                    fillOpacity: 0.1,
                    strokeColor: '#AA0000',
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    draggable: false,    // Dragable
                    editable: false     // Resizable
                });
            }
         }
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