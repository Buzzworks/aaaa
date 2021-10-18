function humanaize(time) {

}
var noti_interval;
var csrf_token = $("input[name='csrfmiddlewaretoken']").val()
var callnotifiaction_vue = new Vue({
    // this vue is related to call_notififcations
    el: '#call_notification',
    delimiters: ['${', '}'],
    data: {
        notification_data: [],
        selected_noti: {}
    },
    methods: {
        showNotification(key) {
            let noti_id, noti_type, noti_campaign, noti_user, numeric, contact_id;
            let noti_data = this.notification_data[key];
            noti_id = noti_data['id'];
            noti_type = noti_data['title'];
            noti_campaign = noti_data['campaign']
            noti_user = noti_data['user']
            if (noti_user == undefined) {
                noti_user = null
            }
            if (noti_campaign == undefined) {
                noti_campaign = null
            }
            numeric = noti_data['numeric']
            contact_id = noti_data['contact_id']
            $.ajax({
                type: 'POST',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/api/update-notification/',
                data: {
                    "noti_type": noti_type,
                    'noti_campaign': noti_campaign,
                    'noti_user': noti_user,
                    'numeric': numeric,
                    "noti_id": noti_id,
                    'contact_id': contact_id
                },
                success: function(data) {
                    noti_modal.selected_noti_data = data['selected_noti_detail']
                    noti_modal.selected_noti_type = noti_data['title'];
                    $('#notification_modal').modal('show')
                }
            })

        },

    },
    filters: {
        format_date: function(date) {
            return moment().from(date, true);
        }
    },
    watch: {

    },
})

var noti_modal = new Vue({
    el: '#notification_modal',
    delimiters: ['${', '}'],
    data: {
        selected_noti_type: '',
        selected_noti_data: {},
        snooze_show: false,
        call_error: ''
    },
    methods: {
        makeCbcall() {
            if (this.selected_noti_data.campaign != '') {
                if (this.selected_noti_data.campaign == campaign_name) {
                    var numeric = this.selected_noti_data.numeric
                    var cb_campaign = this.selected_noti_data.campaign
                    var cb_user = this.selected_noti_data.user
                    var contact_id = this.selected_noti_data.contact_id
                    if (this.selected_noti_type == 'callback') {
                        makeCallbackcall(numeric, cb_campaign, cb_user, contact_id)
                    } else if (this.selected_noti_type == 'Abandonedcall') {
                        var caller_id = this.selected_noti_data.caller_id
                        makeAbandonedcall_Call(numeric, caller_id)
                    }
                } else {
                    this.call_error = "Please Login to " + this.selected_noti_data.campaign + " to make call";
                    setTimeout(() => this.call_error = '', 2000);
                }
            } else {
                this.call_error = "Please Login to Any campaign to make call";
                setTimeout(() => this.call_error = '', 2000);
            }
        },
        snooze_submit() {
            var snoozed_time = $('#snooze_time input').val()
            var snooze_numeric = this.selected_noti_data.numeric
            var snooze_campaign = this.selected_noti_data.campaign
            var snooze_cbtype = this.selected_noti_data.callback_type
            var contact_id = this.selected_noti_data.contact_id
            var snooze_noti_type = this.selected_noti_type
            if (snooze_time != '') {
                $.ajax({
                    type: 'POST',
                    headers: {
                        "X-CSRFToken": csrf_token
                    },
                    url: '/api/snooze-callback/',
                    data: {
                        'snoozed_time': snoozed_time,
                        'numeric': snooze_numeric,
                        'campaign': snooze_campaign,
                        'callback_type': snooze_cbtype,
                        'notification_type': snooze_noti_type,
                        'contact_id': contact_id
                    },
                    success: function(data) {
                        $('#notification_modal').modal('hide')
                        $('.circle').addClass('d-none')
                        if (data['success']) {
                            // $('#heartbit').addClass('d-none')
                            showSuccessToast(data['success'], "top-center")
                        }
                    }
                })
            } else {
                $('.circle').removeClass('d-none')
                this.call_error = "Please select snooze time";
                setTimeout(() => this.call_error = '', 2000);
            }
        }
    }
})

$('#notification_modal').on('hidden.bs.modal', function(e) {
        // do something...
        noti_modal.snooze_show = false;
    })
    // this function to get notification from notification table
function getNotification() {
    $.ajax({
        type: 'GET',
        url: '/api/get-notifications/',
        cache: false,
        timeout: 5000,
        success: function(data) {
            callnotifiaction_vue.notification_data = data['notification_data']
        }
    })
}


// to get notifications on click of notification dropdown
$("#call_notificationDropdown").click(function(event) {
    if ($.inArray(agent_info_vue.state, ['Feedback', 'InCall']) == -1) {
        clearInterval(noti_interval)
        getNotification()
            // noti_interval = setInterval(getNotification, 1000)
    } else {
        event.stopPropagation()
    }
})
$("#admin_call_notificationDropdown").click(function(event) {
    clearInterval(noti_interval)
    getNotification()
        // noti_interval = setInterval(getNotification, 1000)
})
$('#call_notification').on('hide.bs.dropdown', function() {
    clearInterval(noti_interval)
});

function get_latest_notification() {

    $.ajax({
        type: 'get',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/get_latest_notification/',
        data: {},
        success: function(data) {
            $("#dashboard-noti-count").text(data["noti_count"])
            $("#dashboard-download-count").text(data["down_count"])
        },
        error: function(data) {
            if (data['status'] == 403) {
                sessionTerminatedAlert()
            }
        }
    })

}
if(location.pathname.indexOf("agent") == -1 && location.pathname.indexOf("dashboard") ==-1){
    console.log(193);
    setInterval(get_latest_notification, 10000);
}
