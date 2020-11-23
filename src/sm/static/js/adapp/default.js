
// location of our API
//var api_host = document.location.protocol + "//" + document.location.host + "/api";

// Initialize
var api_host = document.location.protocol + "//" + document.location.host + "/api";
var data;
var questions = "";
var indicators = "";
var progress_bar_content = "";
var current_question = 0;
var total_questions = 0;
var mental_test_list = "";
var current_user = "";
var mental_test_id = get_url_vars()["id"];

if (typeof mental_test_id === 'undefined') {
  alert("Using default mental test");
  mental_test_id = 1;
}
 

// Initialize REST API Client
var client = new $.RestClient('/api/', { stringifyData: true }, headers: {"Authorization": localStorage.getItem('token')});
client.add('mental_test_results'); // tests with results
client.add('mental_test'); // test list

 
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
  console.log("LOADING MENTAL TEST: " + m.name);
  var active_class = "";
  if (m.id == mental_test_id)
    active_class = "is-active";
  progress_bar_content += `<li class=${active_class}" data-step="${index}">
  <a href=/static/mental_test.html?id=${m.id}>${m.name}</a>
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
  data = "";
  for(i = 1; i <= total_questions; i++) {
    qs = document.getElementById("question_range-" + i);
    data += 
    `{
      "user": "${current_user}",
      "test": "${mental_test_id}",
      "test_field": "${qs.name}",
      "value": "${qs.value}",
     },`;
  }
  //post_data = post_data.replace(/,$/, "");

  post_data = `[
    ${data}
  ]`;
  return post_data;
}
  
  
function send_mental_test(f) {
  post_data = serialize_question();
  csrf = Cookies.get("csrftoken");
  $.ajaxSetup({
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-CSRFToken': csrf
    }
  });
  $.post(api_host + "/mental_test_results/", post_data)
  .fail(function(jqxhr, text, error) {
    console.log("Mental test failed: " + jqxhr.responseText);
    alert("Mental test failed: " + jqxhr.responseText);
  })
  .done(function(data) {
    alert(data.success);
  });
}

