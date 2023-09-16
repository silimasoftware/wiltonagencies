$(function () {
  var minlength = 1;
  var req = null;
  $("#client_search").keyup(function () {
    clearInterval(itimer);
    t = 200
    i = 200
    e = 1
    start = performance.now();
    var timer
    var itimer = setInterval(function () {
      timer = Math.floor((t - (performance.now() - start)) / i) + e
      console.log(timer)
    }, i);
    setTimeout(function () {
      clearInterval(itimer);
      value = $("#client_search").val();
      if (value.length >= minlength && timer <= 0) {
        if (req != null) req.abort();
        req = $.ajax({
          type: "POST",
          data: {
            action: "search_for",
            search_value: value,
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').attr(
              "value"
            ),
          },
          dataType: "json",
          error: function (request, error) {
            console.log(arguments);
            console.log(" Can't do because: " + error);
          },
          success: function (data) {
            console.log(value)
            $("#client_search_wrapper").html(data.html);
          },
        });
      }
    }, t + 1);
  });
});