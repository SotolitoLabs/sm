
function get_token(user, password) {
  console.log("Getting Token");
  $.post(api_host + "/token-auth/",
  {
      username: user, 
      password: password
  })
  .fail(function(jqxhr, text, error) {
    console.log("Login failed: " + jqxhr.responseText);
    alert("Login failed: " + jqxhr.responseText);
  })
  .done(function(data) {
    alert(data.token);
  });
}

//https://www.django-rest-framework.org/topics/ajax-csrf-cors/
