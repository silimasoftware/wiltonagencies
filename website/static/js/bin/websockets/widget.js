$(function () {
    const chatSocket = new WebSocket($('#ws_chat_form').attr('ws_url'));
    chatSocket.onmessage = function (e) {
        data = JSON.parse(e.data);
        $('#chat-log').append(data.username +" : "+  data.message + '<br>')
    };

    $("#send_data").click(function (event) {
        message = $('#chat-message-input').val();
        if (message == "") {
            alert("you need to type somthing")
        }
        else {
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            $('#chat-message-input').val('')
        }
    });

    $('#chat-message-input').keyup(function (e) {
        if (e.keyCode === 13) {
            $('#send_data').click();
        }
    });

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed!');
    };

    $("#open_chat").click(function (event) {
        $("#chat_box").toggle(100)
    });

    $("#close_chat").click(function (event) {
        $("#chat_box").toggle(100)
        chatSocket.close()
    });
});
