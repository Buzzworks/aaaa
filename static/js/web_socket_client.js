//////////////// Get Data from Script ///////////////////////
// var host = document.getElementById("web_socket_client").getAttribute("data-name");
// var socket = io.connect(host + ':4656', {
//     'reconnection': true,
//     'reconnectionDelay': 1000,
//     'reconnectionDelayMax': 5000,
//     'reconnectionAttempts': 10,
//     'maxListeners': 1000,
// });
// socket.on('connect', function() {
//     console.log("connect");
// });

// socket.on('message', function(message) {
//     var message = JSON.parse(message);
//     if (message.is_progress) {
//         $('#' + message.id + '').empty();
//         $('#' + message.id + '').append("<div class='progress progress-lg mt-2'><div class='progress-bar bg-success' role='progressbar' style=\"width:" + message.live_count + "%\" aria-valuenow=" + message.live_count + "% aria-valuemin=\"0\" aria-valuemax=\"100\" >" + message.live_count + "%</div>");
//     } else if (message.is_live_count) {
//         // console.log(194);
//         $('#' + message.id + '').text(message.value);

//     } else if (message.is_update) {
//         get_updates();
//         if(message.value=='agent' && $('#table_div').data('selected')==='agent'){
//             live_data.getAgentData()
//         }
//         if(message.value=='on_call' && $('#table_div').data('selected')==='on_call'){
//             live_data.getOnCallAgentData()
//         }
//         if(message.value=='campaign' && $('#table_div').data('selected')==='campaign'){
//             live_data.getCampaignData()
//         }

//     } else {
//         get_pagination_data(pagination_vue.page)
//     }

// });

