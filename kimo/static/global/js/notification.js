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

$(document).ready(function() {
    $(document).on("click", "#notifications li a", function (event){
         event.preventDefault();

         var addressValue = $(this).attr("href");
         var kid_id = addressValue.split("/")[3];
         var notification_id = addressValue.split("/")[4];

          setSeen(notification_id, kid_id);
          window.location.href = "/kids/view/" + kid_id + "/";
         return false;
    });

var getNotifications = function() {
    $.ajax({
        type: 'GET',
        url: "/api/notification/?seen=false?limit=3",
        headers: myHeader,
        dataType: "json"
    }).done( function(resultData) {
           var numberOfValues = 3;
           if (resultData.count < 3) {
               numberOfValues = resultData.count;
           }
           document.getElementById("notification-circle").textContent = numberOfValues;
           document.getElementById("notifications").innerHTML = `<li class="notification-header"> Notifications </li>`;

           for ( i = 0; i < numberOfValues; i++) {

                   var hours = Math.round(((new Date()).getTime() - new Date(resultData["results"][i].date_created).getTime()) / 3600000);
                   var hourText = "";
                   var daysText = "";
                   var days = 0;

                   if (hours >= 24) {
                       days = Math.floor(hours / 24);
                       hours = Math.ceil(hours % 24);
                       if (days > 1) {
                           daysText += days + " days"
                       } else {
                           daysText += days + " day"
                       }

                       if (hours > 0) {
                            hourText = " and " + hours;
                            if (hours > 1) {
                             hourText += " hours";
                            } else {
                             hourText += " hour ";
                            }
                       }
                   } else {
                       if (hours > 1) {
                           hourText = hours + " hours";
                       } else {
                           hourText = "< 1 hour"
                       }
                   }
                   document.getElementById('notifications').insertAdjacentHTML('beforeend', `
                        <li>
                            <span><i class="glyphicon glyphicon-exclamation-sign"></i>
                                <a href="/account/profile/` + resultData["results"][i].kid + "/"+ resultData["results"][i].id +`"> ` + resultData["results"][i].text + `</a><br>
                                 <small>` + daysText + hourText + ` ago</small>
                            </span>

                             <p id="" hidden></p>
                        </li>`
                   );
           }
    });
    };
    getNotifications();
    setInterval(getNotifications, 5000);
});

function setSeen(notification_id, kid_id) {
    var saveData = $.ajax({
        type: 'PATCH',
        url: "/api/notification/" +  notification_id + "/",
        headers: myHeader,
        data: {"kid" : kid_id, "seen": true},
        dataType: "json"
    });
}
