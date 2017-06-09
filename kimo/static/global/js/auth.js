function login() {

    $.ajax({
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
$(document).ready(function() {
    $('#id_password, #id_password2').on('keyup', function () {
      if ($('#id_password').val() == $('#id_password2').val()) {
        $('#password2_error').html('Matching').css('color', '#449d44');
      } else
        $('#password2_error').html('* Not Matching').css('color', '#d75b32');
    });
});

function register() {

        $.ajax({
        type: 'POST',
        url: "/api/user/",
        data: {'username' : $("#id_username").val(), 'password' : $("#id_password").val(),
                'first_name' : $("#id_first_name").val(), 'last_name' : $("#id_last_name").val(),
                'email' : $("#id_email").val()},
        dataType: "json"
        }).done( function(resultData) {
                window.location.href = '/account/login/';
        }).fail( function(resultData) {
              document.getElementById('username_error').innerHTML = '';
              document.getElementById('password_error').innerHTML = '';
              document.getElementById('first_name_error').innerHTML = '';
              document.getElementById('last_name_error').innerHTML = '';
              document.getElementById('email_error').innerHTML = '';
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
    }).done(function (resultData) {
        window.location.href = '/account/profile';
    }).fail( function(resultData) {
        window.location.href = '/account/profile';
    });
}

function logout() {
 $.ajax({

    type: 'GET',
    url: "/api/auth/logout/",
    dataType: "json",
    error:  function (resultData) {
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