
// Kudos to: https://bernii.github.io/gauge.js/
    function set_gauge(opts,value, max_value) {
  var target = document.getElementById('diagnosis_gauge'); // your canvas element
  var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!
  gauge.maxValue = max_value; // set max gauge value
  gauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
  gauge.animationSpeed = 32; // set animation speed (32 is default value)
  gauge.set(value); // set actual value
}


