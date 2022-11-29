var totalCallback_table, call_history_table;
history_audio = document.getElementById("history_audio_div");
// time format 
function format_time(datetime) {
	if (datetime) {
		return moment(datetime).format("YYYY-MM-DD HH:mm:ss");
	} else {
		return ''
	}
}
totalCallback_table = $('#callback-list').DataTable({
	scrollX:true,
	"destroy":true,
	"bPaginate":false,
	"searching":false,
	"processing":true,
	"info":false,
	columns:[{
		"title": "Number",
		"data" : "numeric",
	},
	{
		"title": "Agent",
		"data": "user"
	},
	{
		"title": "Campaign",
		"data": "campaign",
	},
	{
		"title": "Type",
		"data": "callback_type",
	},
	{
		"title": "Callback Time",
		"data": "schedule_time",
		render : function(data){
			return format_time(data)
		}
	},
	{
		"title": "Disposition",
		"data": "disposition",
	},
	{
		"title":"Comment",
		"data": "comment",
		render: function(data){
			if (data){
				return '<div style="min-width:250px; max-width:550px; white-space: normal; overflow-wrap: break-word;">'+data+'</div>'
			} else {
				return '';
			}
		}
	},
	{
		"title": "Status",
		"data": "status",
	},
	{
		"title": "Action",
		render : function(){
			if (sip_login == true) {
				return "<button class='btn btn-sm btn-inverse-success py-1 px-2 cb-call-btn' title='Call'>"+
				"<i class='fa fa-phone fa-rotate-90'></i></button>"
			}
			else {
				return "<button class='btn btn-sm btn-inverse-success py-1 px-2 cb-call-btn restrict_action' title='Call'>"+
				"<i class='fa fa-phone fa-rotate-90'></i></button>"
			}
		}
	}],
	createdRow: function(row, data){
		$(row).attr('data-tableName','totalCallback_table')
	}
});

activeCallback_table = $('#active-callback-list').DataTable({
	scrollX:true,
	overflowX:'auto',
	columns:[
	{
		"title": "Phone Number",
		"data" : "numeric",
	},
	{
		"title": "Agent",
		"data": "user"
	},
	{
		"title": "Campaign",
		"data": "campaign",
	},
	{
		"title": "Type",
		"data": "callback_type",
	},
	{
		"title": "Callback Time",
		"data": "schedule_time",
		render : function(data){
			return format_time(data)
		}
	},
	{
		"title": "Disposition",
		"data": "disposition"
	},
	{
		"title":"Comment",
		"data": "comment",
		render: function(data){
			if (data){
				return '<div style="min-width:250px; max-width:550px; white-space: normal; overflow-wrap: break-word;">'+data+'</div>'
			} else {
				return '';
			}
		}
	},
	{
		"title":"CallMode",
		"data": "callmode"
	},
	{
		"title": "Action",
		render : function(){
			return "<button class='btn btn-sm btn-inverse-success py-1 px-2 cb-call-btn' title='Call'>"+
			"<i class='fa fa-phone fa-rotate-90'></i></button>"+
			"<button class='btn btn-sm btn-inverse-info py-1 px-2 ml-1 snooze-btn' title='Snooze'>"+
			"<i class='fas fa-bell'></i></button>"+
			"<button class='btn btn-sm btn-inverse-primary py-1 px-2 ml-1 d-none' title='View'>"+
			"<i class='fas fa-info'></i></button>"
		}
	},
	],
	createdRow: function(row, data){
		$(row).attr('data-tableName','activeCallback_table')
	}
})
campaignCallbacks_table = $("#campaign-callback-list").DataTable({
	scrollX:true,
	overflowX:'auto',
	columns:[
	{
		"title": "Phone Number",
		"data" : "numeric",
	},
	{
		"title": "Name",
		"data": "first_name",
	},
	{
		"title": "Agent",
		"data": "user"
	},
	{
		"title": "Type",
		"data": "callback_type",
	},
	{
		"title": "Callback Time",
		"data": "schedule_time",
		render : function(data){
			return format_time(data)
		}
	},
	{
		"title": "Disposition",
		"data": "disposition"
	},
	{
		"title":"Comment",
		"data": "comment",
		render: function(data){
			if (data){
				return '<div style="min-width:250px; max-width:550px; white-space: normal; overflow-wrap: break-word;">'+data+'</div>'
			} else {
				return '';
			}
		}
	},
	{
		"title": "Status",
		"data": "status",
	},
	{
		"title": "CallMode",
		"data": "callmode",
	},
	{
		"title": "Action",
		render : function(){
			return "<button class='btn btn-sm btn-inverse-success py-1 px-2 cb-call-btn' title='Call'>"+
			"<i class='fa fa-phone fa-rotate-90'></i></button>"
		}
	},
	],
	createdRow: function(row, data){
		$(row).attr('data-tableName','campaignCallbacks_table')
	}
})

campaignAbandonedcalls_table = $('#campaign-abandonedcall-list').DataTable({
	scrollX:true,
	"destroy": true,
	"bPaginate": false,
	"ordering":true,"order":[[5,'desc']],
	"searching": false,
	"processing": true,
	"info": false,
	columns:[
	{
		"title": "Phone Number",
		"data" : "numeric",
	},
	{
		"title": "Caller ID",
		"data": "caller_id",
	},
	{
		"title": "Agent",
		"data": "username"
	},
	{
		"title": "Campaign",
		"data": "campaign",
	},
	{
		"title": "Status",
		"data": "status"
	},
	{
		"title": "Time",
		"data": "created_date",
		render : function(data){
			return format_time(data)
		}
	},
	{
		"title": "Action",
		render : function(){
			return "<button class='btn btn-sm btn-inverse-success py-1 px-2 mc-call-btn' title='Call'>"+
				"<i class='fa fa-phone fa-rotate-90'></i></button>"
		}
	},
	],
	createdRow: function(row, data){
		$(row).attr('data-tableName','campaignAbandonedcalls_table')
	}
})

totalAbandonedCalls_table = $('#abandonedcall-list').DataTable({
	scrollX:true,
	"destroy": true,
	"bPaginate": false,
	"searching": false,
	"processing": true,
	"info": false,
	"ordering":true,
	"order":[[5,'desc']],
	columns:[
	{
		"title": "Phone Number",
		"data" : "numeric",
	},
	{
		"title": "Caller ID",
		"data": "caller_id",
	},
	{
		"title": "Agent",
		"data": "username"
	},
	{
		"title": "Campaign",
		"data": "campaign",
	},
	{
		"title": "Status",
		"data": "status"
	},
	{
		"title": "Time",
		"data": "created_date",
		render : function(data){
			return format_time(data)
		}
	},
	{
		"title": "Action",
		render : function(data, type, row, meta){
			if (campaign_name && campaign_name == row["campaign"]) {
				return "<button class='btn btn-sm btn-inverse-success py-1 px-2 mc-call-btn' title='Call'>"+
				"<i class='fa fa-phone fa-rotate-90'></i></button>"
				
			}
			else {
				return "<button class='btn btn-sm btn-inverse-success py-1 px-2 mc-call-btn' title='Call' disabled>"+
				"<i class='fa fa-phone fa-rotate-90'></i></button>"
			}
		}
	},
	],
	createdRow: function(row, data){
		$(row).attr('data-tableName','totalAbandonedCalls_table')
	}
})

totalCallPerDay_table = $('#agent-totalcallsperday-list').DataTable({
	"destroy": true,
	"bPaginate": false,
	"searching": false,
	"processing": true,
	"info": false,
	columns:[
	{
		"title": "PhoneNumber",
		"data" : "customer_cid",
		render:function(data){
			return "<a class='td-call-number '>"+data+"</a>"
		}
	},
	{
		"title":"Campaign",
		"data" : "campaign_name"
	},
	{
		"title": "PhoneBook",
		"data": "phonebook"
	},
	{
		"title": "Call Length",
		"data": "call_length",
	},
	{
		"title": "Disposition",
		"data": "cdrfeedback.primary_dispo",
	},
	{
		"title": "CallMode",
		"data": "callmode"
	},
	{
		"title": "Time",
		"data": "created",
		render : function(data){
			return format_time(data)
		}
	},
	],
	createdRow: function(row, data){
		$(row).attr('data-tableName','totalCallPerDay_table')
	}
})

lead_bucket_table = $('#lead_bucket_list').DataTable({
	"destroy": true,
	"bPaginate": false,
	"searching": false,
	"processing": true,
	"info": false,
	aoColumnDefs: [
		{
			"aTargets": 'contactList_action',
			"mData": "",
			width: "1%",
			orderable: false,
			"mRender": function (data, type,row,full) {
				 return  `<button type='button' class='btn btn-link p-1 view-detail' id='${row['contact']['id']}' phone_number='${row['contact']['numeric']}' campaign="${row['contact']['campaign']}" title='View'> <i class='fas fa-eye'></i> </button> <button type='button' class='btn btn-inverse-info p-1 view-lead-call-history' data-id='${row['contact']['id']}' phone_number='${row['contact']['numeric']}' title='Call History'> <i class='fas fa-history'></i> </button> <button type='button' class='btn btn-inverse-success p-1 contact-make-call' contact_id='${row['contact']['id']}' phone_number='${row['contact']['numeric']}' campaign="${row['contact']['campaign']}" title='Call'> <i class='fa fa-phone fa-rotate-90'></i> </button>`;
			}
		}
	],
})
$(document).on('click','.snooze-btn', function(){
	var snooze_row_data;
	if ($(this).parents('tr').attr('data-tableName') == 'totalCallback_table'){
		snooze_row_data = totalCallback_table.row( $(this).parents('tr') ).data();
	}
	else if ($(this).parents('tr').attr('data-tableName') == 'activeCallback_table'){
		snooze_row_data = activeCallback_table.row( $(this).parents('tr') ).data();
	}
	else if ($(this).parents('tr').attr('data-tableName') == 'campaignCallbacks_table'){
		snooze_row_data = campaignCallbacks_table.row( $(this).parents('tr') ).data();
	}
	noti_modal.selected_noti_data = snooze_row_data
	noti_modal.selected_noti_type = 'callback'
	$('#notification_modal').modal('show')
	console.log(snooze_row_data)
})

$(document).on('click','.cb-call-btn',function(){
	var cb_row_data;
	if ($(this).parents('tr').attr('data-tableName') == 'totalCallback_table'){
		cb_row_data = totalCallback_table.row( $(this).parents('tr') ).data();
	}
	else if ($(this).parents('tr').attr('data-tableName') == 'activeCallback_table'){
		cb_row_data = activeCallback_table.row( $(this).parents('tr') ).data();
	}
	else if ($(this).parents('tr').attr('data-tableName') == 'campaignCallbacks_table'){
		cb_row_data = campaignCallbacks_table.row( $(this).parents('tr') ).data();
	}
	if(agent_info_vue.camp_name === cb_row_data['campaign']){
		if (extension in session_details && Object.keys(session_details[extension]).length > 0){
			makeCallbackcall(cb_row_data['numeric'],cb_row_data['campaign'],cb_row_data['user'], cb_row_data["contact_id"])
		} else {
			showWarningToast('Session details not avaliabe, Re-Login to dialler', 'top-center')
			$('#btnLogMeOut').click()
		}
	}else{
		showWarningToast(`Login to <b>${cb_row_data['campaign']}</b> campaign to make call`, 'top-right')
	}
})

$(document).on('click','.mc-call-btn', function(){
	var mcc_row_data;
	if($(this).parents('tr').attr('data-tableName')=='totalAbandonedCalls_table'){
		mcc_row_data = totalAbandonedCalls_table.row($(this).parents('tr')).data();
	}
	else if($(this).parents('tr').attr('data-tableName')=='campaignAbandonedcalls_table'){
		mcc_row_data = campaignAbandonedcalls_table.row($(this).parents('tr')).data();
	}
	if (extension in session_details && Object.keys(session_details[extension]).length > 0){
		makeAbandonedcall_Call(mcc_row_data['numeric'],mcc_row_data['caller_id'])
	} else {
		showWarningToast('Session details not avaliabe, Re-Login to dialler', 'top-center')
		$('#btnLogMeOut').click()
	}
})

var mont_call_data;
$(document).on('click','.td-call-number',function(){
	var td_call_data;
	if($(this).parents('tr').attr('data-tableName') == 'totalCallPerDay_table'){
		td_call_data = totalCallPerDay_table.row($(this).parents('tr')).data();
		if(td_call_data['campaign_name'] === agent_info_vue.camp_name) {
			if(td_call_data['customer_cid'] != ''){
				if (extension in session_details && Object.keys(session_details[extension]).length > 0){
					swal({
						text: 'Preparing to make call',
						closeOnClickOutside: false,
						button: false,
						icon: 'info'
					})
					setTimeout( function(){
						callmode = 'manual'
						dial_number = td_call_data['customer_cid']
						contact_id = td_call_data['contact_id']
						if(call_type!="2"){
								do_manual_call(dial_number,contact_id)
						}else{
								WebPSTNAgentCallDial()
						}
						swal.close();
						$('#crm-home').click()
					},3000)
				} else {
					showWarningToast('Session details not avaliabe, Re-Login to dialler', 'top-center')
					$('#btnLogMeOut').click()
				}
			}
		} else {
			showWarningToast(`Login to <b>${td_call_data['campaign_name']}</b> campaign to make call`, 'top-right')
		}
	}
	var mont_call_data;
	if($(this).parents('tr').attr('data-tableName') == 'totalCallsPerMonth_table'){
		mont_call_data = $('#agent-monthly-calls').DataTable().row($(this).parents('tr')).data();
		if(mont_call_data['campaign_name'] === agent_info_vue.camp_name) {
			if(mont_call_data['customer_cid'] != ''){
				if (extension in session_details && Object.keys(session_details[extension]).length > 0) {
					 swal({
						text: 'Preparing to make call',
						closeOnClickOutside: false,
						button: false,
						icon: 'info'
					})
					setTimeout(
					function(){
						callmode = 'manual'
						dial_number = mont_call_data.customer_cid
						contact_id = mont_call_data.cdrfeedback.contact_id
						if(call_type!="2"){
								do_manual_call(dial_number,contact_id)
						}else{
								WebPSTNAgentCallDial()
						}
						swal.close();
						$('#crm-home').click()
					},3000)
				} else {
					showWarningToast('Session details not avaliabe, Re-Login to dialler', 'top-center')
					$('#btnLogMeOut').click()
				}
			}
		} else {
			showWarningToast(`Login to <b>${mont_call_data['campaign_name']}</b> campaign to make call`, 'top-right')
		}
	}
	var mont_uniquecall_data;
	if($(this).parents('tr').attr('data-tableName') == 'totaluniqueCallsPerMonth_table'){
		mont_uniquecall_data = $('#agent-monthly-uniquecalls').DataTable().row($(this).parents('tr')).data();
		if(mont_uniquecall_data['campaign'] === agent_info_vue.camp_name) {
			if(mont_uniquecall_data['numeric'] != ''){
				if (extension in session_details && Object.keys(session_details[extension]).length > 0) {
					 swal({
						text: 'Preparing to make call',
						closeOnClickOutside: false,
						button: false,
						icon: 'info'
					})
					setTimeout(
					function(){
						callmode = 'manual'
						dial_number = mont_uniquecall_data.numeric
						contact_id = mont_uniquecall_data.contact_id
						if(call_type!="2"){
								do_manual_call(dial_number,contact_id)
						}else{
								WebPSTNAgentCallDial()
						}
						swal.close();
						$('#crm-home').click()
					},3000)
				} else {
					showWarningToast('Session details not avaliabe, Re-Login to dialler', 'top-center')
					$('#btnLogMeOut').click()
				}
			}
		} else {
			showWarningToast(`Login to <b>${mont_uniquecall_data['campaign']}</b> campaign to make call`, 'top-right')
		}
	}
})

list_of_assigned_contacts_table = $('#show_assigned_contact_list').DataTable({
	"searching": false,
	"processing":true,
	"deferRender": true,	
	"paging": false,
	"info": false,
	aoColumnDefs: [
		{
			"aTargets": 'contactList_action',
			"mData": "",
			width: "1%",
			orderable: false,
			"mRender": function (data, type,row,full) {
				 return  `<button type='button' class='btn btn-link p-1 view-detail' id='${row['id']}' phone_number='${row['numeric']}' campaign="${row['campaign']}" title='View'> <i class='fas fa-eye'></i> </button> <button type='button' class='btn btn-inverse-success p-1 contact-make-call' contact_id='${row['id']}' phone_number='${row['numeric']}' campaign="${row['campaign']}" title='Call'> <i class='fa fa-phone fa-rotate-90'></i> </button>`;
			}
		}
	],
})

function callHistoryTable(table) {
	var table_instance = table.DataTable({
		"scrollX": true,
		"columnDefs": [
		{
			"targets":"action-field",
			"orderable":false,
			render:function(data,type,row,full){
				if(row['dialed_status']=='Connected'){
					return `<button type='button' class='btn btn-inverse-success p-1 play-recording' title='Play Recording'> <i class='fas fa-play-circle'></i> </button>`
				} else {
					return `<button type='button' class='btn btn-inverse-success p-1 play-recording' title='Play Recording' disabled> <i class='fas fa-play-circle'></i> </button>`
				}
			}
		},
		{
			"targets":"comment-field",
			render:function(data){
				return '<div style="max-width:550px; white-space: normal; overflow-wrap: break-word;">'+data+'</div>'
			}
		}
		],
	})
	return table_instance
}
call_history_table = callHistoryTable($('#call-history-table'))
lead_call_history_table = callHistoryTable($('#lead-call-history-table'))

$(document).on('click','.view-lead-call-history', function(){
	var lead_contact_id = $(this).data('id')
	if (lead_contact_id != "") {
		$.ajax({
			type: 'post',
			headers: { "X-CSRFToken": csrf_token },
			url: '/api/get-call-history/',
			data: { "contact_id": lead_contact_id},
			success: function(data) {
				lead_call_history_table.clear().draw();
				lead_call_history_table.rows.add(data).draw();
				$('#lead_call_history_modal').modal('show')
			}
		})
	}
})

function setAudioTag(url, row_data){
	history_audio.src = url
	history_audio.load()
	$('#recordingPlay_modal').find('#rp_cust_number').text(row_data["customer_cid"])
	$('#recordingPlay_modal').find('#rp_agent').text(row_data["user"])
	$('#recordingPlay_modal').find('#rp_campaign').text(row_data["campaign_name"])
	$('#recordingPlay_modal').modal('show')
}

$(document).on('click', '.play-recording', function(){
	var row = $(this).parents('tr')
	var row_data = lead_call_history_table.row(row).data()
	var date = new Date(row_data['diallereventlog']['ring_time']);
	var url = `${location.protocol}//${location.hostname}/recordings/${("0" + date.getDate()).slice(-2)}-${("0" + (date.getMonth() + 1)).slice(-2)}-${date.getFullYear()}-${("0" + date.getHours()).slice(-2)}-${("0" + date.getMinutes()).slice(-2)}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`
	$.ajax({
		url:url,
		type:'HEAD',
		error: function()
		{
			var connect_date = new Date(row_data['connect_time']);
			var connect_url = `${location.protocol}//${location.hostname}/recordings/${("0" + connect_date.getDate()).slice(-2)}-${("0" + (connect_date.getMonth() + 1)).slice(-2)}-${connect_date.getFullYear()}-${("0" + connect_date.getHours()).slice(-2)}-${("0" + connect_date.getMinutes()).slice(-2)}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`
			$.ajax({
				url:connect_url,
				type:'HEAD',
				error: function()
				{
					filenotfoundAlert()
				},
				success: function(){
					setAudioTag(connect_url,row_data)
				}
			})
		},
		success: function()
		{
			setAudioTag(url,row_data)
		}
	});
});

// hide record play modal
$('#recordingPlay_modal').on('hide.bs.modal', function(){
	history_audio.pause()
	history_audio.src = ''
	history_audio.load()
	$('#recordingPlay_modal').find('#rp_cust_number, #rp_agent, #rp_campaign, #rp_init_time').text('')
})

// show record play modal
$('#recordingPlay_modal').on('shown.bs.modal', function(){
	history_audio.play()
})