$(function () {
  $("form").submit(function (event) {
    event.preventDefault();
    event.preventDefault();
    _name = $('#name').val();
    email = $('#email').val();
    subject = $('#subject').val();
    message = $('#message').val();
    if (_name == "" || email == "" || subject == "" || message == "") {
      alert("Please fill out all the fields");
    } else {
      var r = confirm("I confirm all the information provided is correct!");
      if (r == true) {
        console.log("Checked")
        $(".form-after").hide();
        $("#form-result").show();
        $("#form-result-text").html("Working on it...");
        $("#form-msg").show();
        // pretent to look busy incase email takes a sec...
        val = 0
        var loading_stuff = setInterval(function () {
          val += 1
          $(".progress-bar").css("width", val + "%").attr("aria-valuenow", val);
          if (val > 110) {
            val = 0
          }
        }, 10);
        $.ajax({
          type: "POST",
          data: {
            name: _name,
            email: email,
            subject: subject,
            message: message,
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
            if ('success' in data) {
              clearInterval(loading_stuff);
              $("#form-result-text").html("Success!");
              $("#form-result").html("<h1>Sent Successfully!</h1><br>We will get back to you as soon as possable.");
              $(".login-now").html("");
            } else {
              $("#msg_queue").append(data.msg_list);
              $("#form-result").hide();
              $(".form-after").show();
            }
          },
        });
      } else {
        alert("Please enter your email again!");
      }
    }
  });
});