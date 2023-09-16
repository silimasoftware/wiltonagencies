$(function () {
  $("#module_wrapper").on("submit", "form", function (e) {
    e.preventDefault();
    $(".modal").modal("hide");
    $(".modal").on("hidden.bs.modal", function () {
      $(this).removeData();
    });
    _form = new FormData(this)
    _form.append("uid", $(this).attr("uid"));
    _form.append("action", $(this).attr("tag"));
    _form.append("csrfmiddlewaretoken", $('input[name="csrfmiddlewaretoken"]').attr(
      "value"
    ));
    $.ajax({
      type: "POST",
      data: _form,
      processData: false,
      contentType: false,
      dataType: "json",
      error: function (request, error) {
        console.log(arguments);
        console.log(" Can't do because: " + error);
        alert("Oh shit, somthing went wrong:" + error);
      },
      success: function (data) {
        console.log(data);
        $("#msg_queue").html(data.msg_list);
        if (data.html) {
          $("#module_wrapper").html(data.html);
        }
      },
    });
  });
});

function load_model(action, uid, tag) {
  $.ajax({
    type: "POST",
    data: {
      action: action,
      uid: uid,
      tag: tag,
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').attr("value"),
    },
    dataType: "json",
    error: function (request, error) {
      console.log(arguments);
      console.log(" Can't do because: " + error);
      alert("Oh shit, somthing went wrong... Check the logs");
    },
    success: function (data) {
      $("#msg_queue").html(data.msg_list);
      if (data.modal) {
        $("#modal_wrapper").html(data.modal);
        $(".modal").modal("show");
      }
    },
  });
}