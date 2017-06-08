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

function getNotifications() {

var saveData = $.ajax({
        type: 'GET',
        url: "http://127.0.0.1:8000/api/notification/",
        headers: myHeader,
        dataType: "json"
    }).done( function(resultData) {
           var numberOfValues = 3;
           if (resultData.count < 3) {
               numberOfValues = resultData.count;
           }
           console.log(Math.round(((new Date()).getTime() - new Date(resultData["results"][0].date_created).getTime()) / 3600000));
           document.getElementById("notification-circle").textContent = numberOfValues;

           for ( i = 0; i < numberOfValues; i++) {

                   var hours = Math.round(((new Date()).getTime() - new Date(resultData["results"][i].date_created).getTime()) / 3600000);
                   var hourText = "hour";
                   if (hours > 1) {
                       hourText = "hours";
                   } else {
                       hours = "< 1"
                   }
                   document.getElementById('notifications').insertAdjacentHTML('beforeend', `
                        <li>
                            <span><i class="glyphicon glyphicon-exclamation-sign"></i>
                                ` + resultData["results"][i].text + `<br><small>` + hours + " " + hourText + ` ago</small>
                            </span>
                        </li>`
                   );
           }
    });
}

