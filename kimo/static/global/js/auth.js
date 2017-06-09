function login() {

var saveData = $.ajax({

    type: 'POST',
    url: "/api/token-auth/",
    data: {'username' : $("#id_username").val(), 'password' : $("#id_password").val()},
    dataType: "json"
    }).done( function(resultData) {
            createCookie("token", resultData.token, 0);
            loginSession();

    }).fail( function(resultData) {
          document.getElementById('username_error').innerHTML = '';
          document.getElementById('password_error').innerHTML = '';
          document.getElementById('non_field_errors_error').innerHTML = '';
          var listData = JSON.parse(resultData.responseText);
          for (obj in listData) {
               document.getElementById(obj + '_error').innerHTML = ('*' + listData[obj]);
          }
    });

    return false;
}

function loginSession() {
 $.ajax({

    type: 'POST',
    url: "/api/auth/login/",
    data: {'username' : $("#id_username").val(), 'password' : $("#id_password").val(), 'csrfmiddlewaretoken':  $("input[name='csrfmiddlewaretoken']").val()},
    dataType: "json"
    }).fail( function(resultData) {
         console.log(resultData);
         window.location.href = '/account/profile';
    });
}

function logout() {
 $.ajax({

    type: 'GET',
    url: "/api/auth/logout/",
    dataType: "json",
    error:  function (resultData) {
         console.log(resultData);
         window.location.href = '/account/login/';
        }
    });
}


function createCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}