var myHeader = { Authorization : "Token " + readCookie('token')};

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function getProfile() {

var saveData = $.ajax({
        type: 'GET',
        url: "/api/user/1/",
        headers: myHeader,
        dataType: "json"
    }).done( function(resultData) {
                document.getElementById('name-user').innerHTML = resultData['first_name'] + " " + resultData['last_name'];
                document.getElementById('email-user').innerHTML = resultData['email'];
                document.getElementById('phone-number-user').innerHTML = resultData['phone_number'];
                document.getElementById('birth-date-user').innerHTML = resultData['birth_date'];
    });
}

function getKids() {

var saveData = $.ajax({

    type: 'GET',
    url: "/api/kid",
    headers: myHeader,
    dataType: "json"
    }).done( function(resultData) {

            for (i = 1; i <= resultData['results'].length; i++) {
                    var expanded = '';
                    if (i == 1) { expanded = 'in';}
                    document.getElementById('accordion').insertAdjacentHTML('beforeend', `
                            <div class="panel panel-default">
                            <div class="panel-heading" role="tab" id="heading">
                              <h4 class="panel-title">
                                <a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse` + i +`" aria-expanded="false" aria-controls="collapse` + i +`">
                                  ` + resultData['results'][i-1].first_name + `
                                </a>
                                  <span class="glyphicon glyphicon-trash pull-right" onclick="deleteChild(`+ resultData['results'][i-1].id +`)" style="color: red;"></span>
                                  <a href="/kids/view/`+ resultData['results'][i-1].id +`">
                                      <span class="glyphicon glyphicon-eye-open pull-right"></span>
                                  </a>
                              </h4>
                            </div>
                            <div id="collapse` + i +`" class="panel-collapse collapse `+ expanded +`" role="tabpanel" aria-labelledby="heading` + i +`">
                              <div class="panel-body">
                                  <div class="row">
                                      <div class="col-md-3"><img src="/static/global/img/baby_picture.jpeg"></div>
                                      <div class="col-md-6">
                                          <h3>` + resultData['results'][i-1].first_name + ' ' + resultData['results'][i-1].last_name +`</h3>
                                          <p><span class="glyphicon glyphicon-calendar"></span> ` + resultData['results'][i-1].birth_date + `</p>
                                          <p><span class="glyphicon glyphicon-map-marker"></span> <span id="location` + i + `">Unknown location</span></p>
                                      </div>
                                  </div>
                              </div>
                            </div>
                          </div>
                    `);
            };
            var kid_map = {}; // Highly important, used to store kid_id maped to i
            for (i = 1; i <= resultData['results'].length; i++) {
                    var kid_id = resultData['results'][i - 1].id;
                    kid_map[kid_id] = i;
                    $.ajax({
                        type: 'GET',
                        url: "/api/location",
                        headers: myHeader,
                        data: {'kid' : kid_id, 'limit' : 1},
                        dataType: "json"
                    }).done( function(resultData2) {
                                if (resultData2.count > 0 ) {
                                   googleCall(resultData2, kid_map);
                                }
                    });
            }
    })
};

function googleCall(resultData, kid_map) {
    var kid_id = resultData["results"][0].kid;
    $.ajax({
        type: 'GET',
        url: "http://maps.googleapis.com/maps/api/geocode/json",
        data: {'latlng' : resultData['results'][0].latitude + ',' + resultData['results'][0].longitude},
        dataType: "json"
    }).done(function(data) {
                var address = data['results'][0];
                if (address != null) {
                     document.getElementById('location' + kid_map[kid_id]).innerHTML = address.formatted_address;
                } else {
                     document.getElementById('location' + kid_map[kid_id]).innerHTML = "Unknown street";
                }
    });
}


function deleteChild(id) {
   var r = confirm("Are you sure you what to delete the child?");

   if (r == true) {
        var saveData = $.ajax({

        type: 'DELETE',
        url: "/api/kid/" + id,
        headers: myHeader,
        dataType: "json"
        });
    location.reload();
   }
};

function addChild() {

        var saveData = $.ajax({
        type: 'POST',
        url: "/api/kid/",
        headers: myHeader,
        data: {'first_name' : $("#id_first_name").val(), 'birth_date' : $("#id_birth_date").val() },
        dataType: "json"
        }).done(function(resultData) {
               location.reload();
        }).fail( function(resultData) {
                   document.getElementById('first_name_error').innerHTML = '';
                   document.getElementById('birth_date_error').innerHTML = ' ';
                   for (obj in resultData.responseJSON) {
                        document.getElementById(obj + '_error').innerHTML = ('*' + resultData.responseJSON[obj]);
                   }
        });
};