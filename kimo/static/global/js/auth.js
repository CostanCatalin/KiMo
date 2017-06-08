function login() {

var saveData = $.ajax({

    type: 'POST',
    url: "http://127.0.0.1:8000/api/token-auth/",
    headers: myHeader,
    data: {'username' : $("#id_username").val(), 'password' : $("#id_password").val(), },
    success: function(resultData) {
                alert('woooo');
    },
    error : function(resultData) {
                alert('off');
    },
    dataType: "json"
});
}