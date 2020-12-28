
// location of our API
//var api_host = document.location.protocol + "//" + document.location.host + "/api";

// Initialize
var api_host = document.location.protocol + "//" + document.location.host + "/api";
var data;
var questions = "";
var indicators = "";
var progress_bar_content = "";
var progress_bar_content_diagnosis = "";
var current_question = 0;
var total_questions = 0;
var mental_test_list = "";
var current_user = "";
var current_test_name = "NO CURRENT TEST AVAILABLE";
var mental_test_id = get_url_vars()["id"];
var DEFAULT_MENTAL_TEST_ID = 2;

if (typeof mental_test_id === 'undefined') {
  mental_test_id = DEFAULT_MENTAL_TEST_ID; //TODO get this from a service
}
 
//https://github.com/jpillora/jquery.rest/blob/gh-pages/dist/jquery.rest.js
// Initialize REST API Client
//var client = new $.RestClient('/api/', { stringifyData: true },  headers: { "Authorization": localStorage.getItem('token') });
var client = new $.RestClient('/api/', { stringifyData: true });
//client.opts.ajax.Authorization=localStorage.getItem('token');
//client.opts.ajax.ajaxOpts.headers['Authorization']=localStorage.getItem('TEST');

client.add('mental_test_results'); // tests with results
client.add('mental_test'); // test list
client.add('mental_test_diagnose'); // test diagnostics
client.add('mental_test_diagnose_result'); // ALL test diagnostics

 
function set_bubbles() { 
  const allRanges = document.querySelectorAll(".sm-range-wrap");
  allRanges.forEach(wrap => {
    const range = wrap.querySelector(".sm-range");
    const bubble = wrap.querySelector(".sm-bubble");
  
    range.addEventListener("input", () => {
      setBubble(range, bubble);
    });
    setBubble(range, bubble);
  });
}
  
  
function setBubble(range, bubble) {
  const val = range.value;
  const min = range.min ? range.min : 0;
  const max = range.max ? range.max : 100;
  const newVal = Number(((val - min) * 100) / (max - min));
  bubble.innerHTML = val;
  
  // Sorta magic numbers based on size of the native UI thumb
  bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.10}px))`;
}
  
  
// Read a page's GET URL variables and return them as an associative array.
// https://stackoverflow.com/questions/4656843/get-querystring-from-url-using-jquery
function get_url_vars() {
  var vars = [], hash;
  var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
  for(var i = 0; i < hashes.length; i++) {
    hash = hashes[i].split('=');
    vars.push(hash[0]);
    vars[hash[0]] = hash[1];
  }
  return vars;
}
 

function add_question(tf, tf_value, index) {
  if( tf_value <= 0 ) {
    tf_value = Math.round(tf.field_type.final_range / 2);
  }
  questions += `<div class="carousel-item sm-range-wrap" id="question-${index}">
    <h4 style="padding-bottom: 6%">${index}.&nbsp;${tf.name}</h4>
    <div class="row">
      <div class="sm-bubble"><output id="output-${tf.id}">${tf_value}</output></div>
    <div class="col-sm-3">${tf.field_type.initial_label}</div>
    <div class="col-sm-6"><input type="range" min="${tf.field_type.initial_range}" 
      max="${tf.field_type.final_range}" value="${tf_value}" class="sm-slider sm-range" 
      id="question_range-${index}" name="${tf.id}" onMouseDown="set_question(this)"> </div>
    <div class="col-sm-3">${tf.field_type.final_label}</div>
      </div>
    </div>`;

    indicators += `<li data-target="#carouselExampleIndicators"
      data-slide-to="${(index-1)}" class="sm-carousel-indicator active"></li>`
}


function add_mental_test(m, index) {
  index += DEFAULT_MENTAL_TEST_ID;

  var active_class = "";
  if (m.id == mental_test_id) {
    current_test_name = m.name;
    active_class = "is-active";
  }
  progress_bar_content += `<li class="${active_class}" data-step="${index}">
  <a href=/static/mental_test.html?id=${m.id}>${m.name}</a>
  </li>`;
}
 

function add_mental_test_diagnosis(m, index) {
  index += DEFAULT_MENTAL_TEST_ID;
  console.log("DEBUG::LOADING MENTAL TEST " + m.id + ": " + m.name);

  var active_class = "";
  if (m.id == mental_test_id) {
    current_test_name = m.name;
    active_class = "is-active";
  }
  progress_bar_content_diagnosis += `<li class="${active_class}" data-step="${index}">
  <a href=/static/mental_test_diagnosis.html?id=${m.id}>${m.name}</a>
  </li>`;
}
 

  
function set_question(slider) {
  output = document.getElementById("output-" + slider.name);
  output.innerHTML = slider.value;
  slider.oninput = function() {
    output.innerHTML = this.value;
  }
}
 

function show_previous_question() {
  if (current_question > 1) {
    $("#question-" + current_question).removeClass('active');
    current_question = current_question - 1;
    $("#question-" + current_question).addClass('active');
  }
}
  
  
function show_next_question() {
  if (current_question < total_questions ) {
    $("#question-" + current_question).removeClass('active');
    current_question = current_question + 1;
    $("#question-" + current_question).addClass('active');
  }
}
  
  
function serialize_question() {
  data = [];
  for(i = 1; i <= total_questions; i++) {
    qs = document.getElementById("question_range-" + i);
    data.push(
      {
        "user":       current_user,
        "test":       mental_test_id,
        "test_field": qs.name,
        "value":      qs.value,
       }
     );
  }
  return data;
}
  
  
function send_mental_test(f) {
  post_data = serialize_question();
  //TODO: csrf = Cookies.get("csrftoken");
  $.ajaxSetup({
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'Token ' + token
      //'X-CSRFToken': csrf
    }
  });
  $.post(api_host + "/mental_test_results/", JSON.stringify(post_data))
  .fail(function(jqxhr, text, error) {
    console.log("Mental test failed: " + jqxhr.responseText);
    alert("Mental test failed: " + jqxhr.responseText);
  })
  .done(function(data) {
    alert(data.success);
  });
}

function diagnose_test(f) {
  //Update test
  send_mental_test(f);
  //var diagnose_data = {};
  // Get mental tests diagnosis
  console.log("Starting diagnose procedure...");
  d = {
        "test": mental_test_id,
      };
 
  client.mental_test_diagnose_result.create(d)
  .fail(function(jqxhr, text, error) {
    console.log("Mental test diagnosis failed: " + jqxhr.responseText);
    alert("Mental test diagnosis failed: " + jqxhr.responseText);
  })
  .done(function( data ) {
    alert(data);
    //window.location.href="/mental_test_diagnosis.html?id=" + mental_test_id;
  });

  console.log("DIAGNOSE DATA: " + JSON.stringify(diagnose_data));
  return(diagnose_data);
}
