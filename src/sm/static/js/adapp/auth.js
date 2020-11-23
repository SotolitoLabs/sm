
// Our auth token
var token = Cookies.get("token");
alert("AUTH.JS TOKEN: " + token);

function login(username, password) {
  get_token(username, password);
}


function set_auth_info(token) {
  Cookies.set('token', token);
}


function get_token(user, password) {
  console.log("Getting Token");
  $.post(api_host + "/token-auth/",
  {
      username: user, 
      password: password
  })
  .fail(function(jqxhr, text, error) {
    console.log("Login failed: " + jqxhr.responseText);
    alert("Login failed: " + jqxhr.responseText + " User:" + user + " pass: " + password);
  })
  .done(function(data) {
    console.log("DATA: " + JSON.stringify(data));
    set_auth_info(data.token);
    location.href = "/mental_test.html";
  });
}


//https://www.django-rest-framework.org/topics/ajax-csrf-cors/
