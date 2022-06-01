var report_table, custom_pagination_table, callrecordings_table, url, agent_mis_table,current_order_col
result = []
audio = document.getElementById("audio_div");
qc_audio = document.getElementById("qc_audio_div");
visibility_col_dic = {
	text: 'Save column visibility',
	className: 'btn-outline-dark',
	action: function ( e, dt, node, config ) {
		var col_name = []
		var report_name = $("#report_name").val()
		$(".dataTables_scrollHeadInner #column_name th").each(function(index) {
			temp_name = $(this).attr("data-field_name")
			if (temp_name) {
				col_name.push(temp_name)
			}
		});
		$.ajax({
			type: 'post',
			headers: {
				"X-CSRFToken": csrf_token
			},
			url: '/api/save-column-visibility/',
			data: {'col_name':col_name, 'report_name':report_name},
			success: function(data) {
				showInfoToast("Column Visiility Saved Successfully", 'top-center')
			},
			error: function(data) {
				console.log(data);
			}
		})
	}
}
show_hide_col_button = {
	text:'Show/Hide all columns',
	action: function ( e, dt, node, config ) {
		e.preventDefault()
		if(dt.column().visible()){
			dt.columns().visible(false)
		}else {
			dt.columns().visible(true)
		}
	}
}

function set_colums(report_table, col_list=[]) {
	$(".dataTables_scrollHeadInner #column_name th").each(function(index) {
		temp_name = $(this).attr("data-field_name")
		if ($.inArray(temp_name, col_list) == -1) {
			report_table.column(index).visible(false)   
		}
		if($(this).attr('class').includes('select-checkbox') || temp_name == 'recording_col'){
			report_table.column(index).visible(true)  
		}
	});
}

//datetimepicker initialization
function defultTime(hours,minute){
	var date = new Date()
	date.setHours(hours)
	date.setMinutes(minute)
	return date
}

// time format 
function format_time(datetime) {
	if (datetime) {
		return moment(datetime).format("YYYY-MM-DD HH:mm:ss");
	} else {
		return ''
	}
}

$(function(){
var date1 = new Date();
var munimumDate = new Date(date1.setMonth(date1.getMonth() - 3));
	$('#start-date').datetimepicker({
		icons: {
			time: 'fa fa-clock'
		},
		format: 'YYYY-MM-DD HH:mm',
		useCurrent: false,
		defaultDate:defultTime(0,0),
		maxDate:defultTime(23,59)
	})
	$('#end-date').datetimepicker({
		icons: {
			time: 'fa fa-clock'
		},
		format: 'YYYY-MM-DD HH:mm',
		useCurrent: false,
		defaultDate:moment(),
		maxDate:defultTime(23,59)
	})
	
	$("#start-date").on("change.datetimepicker", function (e) {
		if($("#end-date input").val()===''){
			$('#end-date').data("datetimepicker").date(new Date());
		}
		if($("#start-date input").val()===''){
			$('#start-date').data("datetimepicker").date(new Date());
		}
		$('#end-date').datetimepicker('minDate', e.date);
	});
	$("#end-date").on("change.datetimepicker", function (e) {
		if($("#end-date input").val()===''){
			$('#end-date').datetimepicker('setInitialDate', new Date());
		}
		if($("#start-date input").val()===''){
			$('#start-date').datetimepicker('setInitialDate', new Date());
		}
		$('#start-date').datetimepicker('maxDate', e.date);
	});
	$('#start_duration, #end_duration').datetimepicker({
		format : 'HH:mm:ss',
	})
})
report_pagination_vue = new Vue({
	el: '#report_pagination_vue',
	delimiters: ['${', '}'],
	data: {
		total_records:0,
		total_pages:0,
		page:1,
		start_index:0,
		end_index:0,
		has_next:false,
		has_prev:false,
	},
	methods:{
		changePage(value){
			$('#nextPage_number').val(value)
			customPaginationReport()
		}
	}
})
// this function for custom pagination for non queryset serverside datatable
function customPaginationReport(){
	custom_pagination_table.processing(true)
	all_users = $('#agent_activity_users option').map(function() { return $(this).val(); }).get();
	if(jQuery.isEmptyObject(all_users) == false) {
		$('#all_users').val(all_users)
	}
	all_campaigns = $('#agent_report_campaign option').map(function() { return $(this).val(); }).get();
	$('#all_campaigns').val(all_campaigns)
	$("#call_details_flag").val("")
	// $('.preloader').fadeIn('fast');
	$.ajax({
		type: 'post',
		headers: {"X-CSRFToken": csrf_token},
		url: location.pathname,
		data:$('#report_form').serialize(),
		success: function(data){
			custom_pagination_table.clear();
			custom_pagination_table.rows.add(data['table_data']); // Add new data
			custom_pagination_table.columns.adjust().draw(); // Redraw the DataTable
			report_pagination_vue.total_records = data['total_records']
			report_pagination_vue.total_pages = data['total_pages']
			report_pagination_vue.page = data['page']
			report_pagination_vue.start_index = data['start_index']
			report_pagination_vue.end_index = data['end_index']
			report_pagination_vue.has_next = data['has_next']
			report_pagination_vue.has_prev = data['has_prev']
			if (result.length > 0){
				custom_pagination_table.rows().every( function ( rowIdx, tableLoop, rowLoop ) {
					if($.inArray(this.data()['id'],result) == -1){
						this.deselect()
					} else{
						this.select()
					}
				})
			}
			// $('.preloader').fadeOut('fast');
		},
		complete: function(){
			custom_pagination_table.processing(false)
		}
	})
}

//this function for datatable with serverside pagination
function report_datatable(table,url,col_list){
	report_table = table.DataTable({
		"scrollX": true,
		"serverSide": true,
		"processing": true,
		"searching": false,
		"language": {
			"processing": '<i class="fa fa-spinner fa-spin fa-3x fa-fw"></i><span class="sr-only">Loading...</span> '
		},
		"ajax": {
			"url": url,
			"headers": { "X-CSRFToken": csrf_token },
			"type": "POST",
			"data":function(d){
				d.format = "datatables"
				d.selected_campaign = $('#agent_report_campaign').val()
				d.selected_user = $('#agent_activity_users').val()
				d.all_users = $('#agent_activity_users option').map(function() { return $(this).val(); }).get();
				d.all_campaigns = $('#agent_report_campaign option').map(function() { return $(this).val(); }).get();
				d.selected_disposition = $('#disposition').val()
				d.start_date = $("#start-date input").val()
				d.end_date = $("#end-date input").val()
				d.numeric = $("#number").val()
				d.uniquefields = $('#uniquefields').val()
				d.unique_id = $('#unique_id').val()
			},
		},
		columnDefs: [{ 
			"targets": '_all',
			"defaultContent": " ", 
			},
			{
			"targets":'dialler_cols',
			render:function(data,type,row,meta){
				var title = report_table.column( meta.col ).header()
				var field_name = $(title).data('field_name')
				if(data == '' || data == null ){
					return row[field_name]
					}else{
						return data
					}
				}
			},
			{
			"targets":'timestamp-field',
			render : function(data){
				return format_time(data)
			},
			"targets":'comment-field',
			render: function(data){
				if (data){
					return '<div style="min-width:250px; max-width:550px; white-space: normal; overflow-wrap: break-word;">'+data+'</div>'
				} else {
					return '';
				}
			}
		}],
		dom: 'Bfrtip',
		lengthMenu: [
			[ 10, 25, 50, 100 ],
			[ '10 rows', '25 rows', '50 rows', '100 rows' ]
		],
		buttons:{
			dom:{
				button:{
					tag:'button',
					className:''
				}
			}
		},
		buttons: [
			{
				extend: 'pageLength',
				className: 'btn-outline-dark',
			},
			{
				extend: 'colvis',
				prefixButtons: [ show_hide_col_button ],
				className: 'btn-outline-dark',
			},
			visibility_col_dic
			]
	});
	if (col_list) {
		$(".dataTables_scrollHeadInner #column_name th").each(function(index) {
	        temp_name = $(this).attr("data-field_name")
	        if ($.inArray(temp_name, col_list) == -1) {
	        	// report_table.column(index).visible(true)
	        	report_table.column(index).visible(false)	
	        }
	        
	    });
		
	}
}

// custom pagination table
function customPaginationTable(table, col_list){
	var id = '#' + table.attr('id');
	ordering = false
	checkbox_classname = ''
	default_order_col = [[0,'desc']]
	if(table.attr('id') == 'callrecordings-list-table'){
		ordering = true
		current_order_col = [8,'desc']
		checkbox_classname = 'select-checkbox'
		default_order_col = [[8,'desc']]
	}
	if(table.attr('id') == 'alternate-numbers-table'){
		checkbox_classname = 'select-checkbox'
	}
	custom_pagination_table = $(table).DataTable({
		"scrollX": true,
		"bPaginate": false,
		"bInfo": false,
		"searching": false,
		"processing": true,
		"ordering": ordering,
		"order": default_order_col, //for recording table
		"processing":  true,
		"language": {
			"processing": '<i class="fa fa-spinner fa-spin fa-3x fa-fw"></i><span class="sr-only">Loading...</span> '
		},
		select: {
			style:'multi',
			selector: 'td:first-child'
		},
		columnDefs: [
			{
				orderable: false,
				className: checkbox_classname,
				targets:   0
			},
			{ 
				"targets":"talk_time_col",
				"orderable":true
			},
			{
			"targets":'timestamp-field',
			orderable:true,
			render : function(data){
				return format_time(data)
			}},
			{
			"targets": '_all',
			"defaultContent": " ",
			orderable:false
			},
			{
				"targets":'modify',
				"orderable": false,
				render : function(data, type, row) {
					return '<button type="button" class="btn btn-primary btn-sm modify-callback" data-id="'+row["callbackcontact_id"]+'">Modify</button>'
				}
			},
			{
				"targets":'modify-abandoned',
				"orderable": false,
				render : function(data, type, row) {
					return '<button type="button" class="btn btn-primary btn-sm modify-abandoned" data-id="'+row["id"]+'">Modify</button>'
				}
			},
			{
				"targets": "checkbox_col",
				"orderable": false,	
				render: function(data, type, row) {
					data = {
						"can_delete": can_delete,
					}
					if ("checked" in row) {
						data["checked"] = "checked"
					}
					var cust_template = `<div class="btn-group select-all-div"><div class="form-check"><label class="form-check-label ml-3"><input name="select_all" value="1" type="checkbox" class="form-check-input"{{#checked}}{{checked}}{{/checked}}/><i class="input-helper"></i></label></div></div>`
					var html = Mustache.to_html(cust_template, data);
					return html
				}
			},
			{
				"targets":'recording-field',
				"orderable": false,
				render: function(data,type,row,full){
					return `<button class='btn btn-inverse-success play-recording'><i class='fas fa-play-circle'></i></button><button class='btn btn-inverse-info ml-2 save-qc'><i class="far fa-comments"></i></button><a href='#' class='btn btn-inverse-info ml-2 file-download'><i class='fa fa-download'></i></a><a href='' download id="${row['session_uuid']}"></a>`
				}
			},

		],
		"fnCreatedRow": function( nRow, aData, iDataIndex ) {
			if ("callbackcontact_id" in aData) {
		    	$(nRow).attr('id', "row-"+aData["callbackcontact_id"]);
			}
			else if("id" in aData) {
				$(nRow).attr('id', "row-"+aData["id"]);	
			}
			if (aData["is_feedback"] == "true") {
				$(nRow).addClass("feedback_saved")	
			}
			else {
				$(nRow).removeClass("feedback_saved")		
			}
		},
		dom: 'Bfrtip',
		lengthMenu: [
			[ 10, 25, 50, 100 ],
			[ '10 rows', '25 rows', '50 rows', '100 rows' ]
		],
		buttons:{
			dom:{
				button:{
					tag:'button',
					className:''
				}
			}
		},
		buttons: [
			{
				extend: 'pageLength',
				className: 'btn-outline-dark',
			},
			{
				extend: 'colvis',
				prefixButtons: [ show_hide_col_button ],
				className: 'btn-outline-dark',
			},
			visibility_col_dic
			]
	})
	if (col_list) {
		set_colums(custom_pagination_table,col_list)
	}
	if(table.attr('id') == 'callrecordings-list-table'){
		custom_pagination_table
		.on( 'select', function ( e, dt, type, indexes ) {
			if (result.indexOf(custom_pagination_table.rows(indexes).data()[0]['id']) == -1){
				result.push(custom_pagination_table.rows(indexes).data()[0]['id'])
			}
			$('#selected_rows_count').text(result.length+ ' rows selected')
		})
		.on( 'deselect', function ( e, dt, type, indexes ) {
			$.each(indexes, function(index,value){
				var removed_index = result.indexOf(custom_pagination_table.rows(value).data()[0]['id'])
				if (removed_index !=-1){
					result.splice(removed_index, 1);
				}
			})
			if(result.length == 0){
				$('#selected_rows_count').text('')
			}else{
				$('#selected_rows_count').text(result.length+ ' rows selected')
			}
		});
		$(table).on( 'order.dt', function () {
			var order = custom_pagination_table.order();
			if (JSON.stringify(current_order_col) != JSON.stringify(order[0])){
				current_order_col = [...order[0]]
				$('#order_col').val($(custom_pagination_table.column(order[0][0]).header()).data('field_name'))
				$('#order_by').val(order[0][1])
				customPaginationReport()
			}
		} );
		$(id+' tbody').on('click', 'tr td:not(:first-child,:last-child)', function (e) {
			e.stopPropagation();
			$('#callrecordings-list-table tbody tr').removeClass('highlighted_row')
			$(this).parent('tr').addClass('highlighted_row')
    	});
    	$(window).click(function() {
			$('#callrecordings-list-table tbody tr').removeClass('highlighted_row')
		})
	}
	if(table.attr('id') == 'alternate-numbers-table'){
	    custom_pagination_table
        .on( 'select', function ( e, dt, type, indexes ) {
        	console.log(431)
            if (result.indexOf(custom_pagination_table.rows(indexes).data()[0]['id']) == -1){
                result.push(custom_pagination_table.rows(indexes).data()[0]['id'])
            }
            $('#selected_rows_count').text(result.length+ ' rows selected')
            $('#slected_entry').val(result);
        })
        .on( 'deselect', function ( e, dt, type, indexes ) {
            $.each(indexes, function(index,value){
                var removed_index = result.indexOf(custom_pagination_table.rows(value).data()[0]['id'])
                if (removed_index !=-1){
                    result.splice(removed_index, 1);
                }
            })
            if(result.length == 0){
                $('#selected_rows_count').text('')
            }else{
                $('#selected_rows_count').text(result.length+ ' rows selected')
            }
            $('#slected_entry').val(result);
        });
    }

}
// agent mis table
function agentmisDatatable(table){
	agent_mis_table = table.DataTable({
			"scrollX": true,
			"searching": false,
			"processing": true,
			columnDefs: [{ 
				"targets": '_all',
				"defaultContent": " ", 
				},
				{
				"targets":'timestamp-field',
				render : function(data){
					return format_time(data)
				}
			}],
			dom: 'Bfrtip',
			lengthMenu: [
				[ 10, 25, 50, 100 ],
				[ '10 rows', '25 rows', '50 rows', '100 rows' ]
			],
			buttons:{
				dom:{
					button:{
						tag:'button',
						className:''
					}
				}
			},
			buttons: [
				{
					extend: 'pageLength',
					className: 'btn-outline-dark',
				},
				{
					extend: 'colvis',
					prefixButtons: [ show_hide_col_button ],
					className: 'btn-outline-dark',
				}]
		})
}
function MISPaginationReport(url){
	all_users = $('#agent_activity_users option').map(function() { return $(this).val(); }).get();
	all_campaigns = $('#agent_report_campaign option').map(function() { return $(this).val(); }).get();
	$('#all_users').val(all_users)
	$('#all_campaigns').val(all_campaigns)
	$.ajax({
		type: 'post',
		headers: {"X-CSRFToken": csrf_token},
		url: url,
		data:$('#report_form').serialize(),
		success: function(data){
			agent_mis_table.clear().draw();
			agent_mis_table.rows.add(data['table_data']); // Add new data
			agent_mis_table.columns.adjust().draw(); // Redraw the DataTable
		}
	})
}
$('#mis-report-filter').click(function(){
	result = []
	$('#selected_rows_count').text('')
	customPaginationReport()
})

// recoding table datatable
function recordingDatatable(table, col_list){
	var id = '#' + table.attr('id');
	callrecordings_table = table.DataTable({
		"scrollX": true,
		"serverSide": true,
		"processing": true,
		"searching": false,
		"ajax": {
			"url": url,
			"headers": { "X-CSRFToken": csrf_token },
			"type": "POST",
			"data":function(d){
				d.format = "datatables"
				d.customer_cid = $('#destination_extension').val()
				d.selected_campaign = $('#agent_report_campaign').val()
				d.all_campaigns = $('#agent_report_campaign option').map(function() { return $(this).val(); }).get();
				d.selected_user = $('#agent_activity_users').val()
				d.all_users = $('#agent_activity_users option:not(.d-none)').map(function() { return $(this).val(); }).get();
				d.start_date = $("#start-date input").val()
				d.end_date = $("#end-date input").val()
				d.unique_id = $("#unique_id").val()
			},
		},
		columnDefs: [{ 
				"targets": '_all',
				"defaultContent": " ", 
			},
			{
				"targets":'timestamp-field',
				render : function(data){
					return format_time(data)
				},
			},
			{
            targets: "checkbox_col",
            render: function(data, type, row) {
                data = {
                    "can_delete": can_delete,
                }
                if ("checked" in row) {
                    data["checked"] = "checked"
                }
                var cust_template = `<div class="btn-group select-all-div"><div class="form-check"><label class="form-check-label ml-3"><input name="select_all" value="1" type="checkbox" class="form-check-input"{{#checked}}{{checked}}{{/checked}}/><i class="input-helper"></i></label></div></div>`
                var html = Mustache.to_html(cust_template, data);
                return html
            }

        },
			{
				targets:[-2],
				render: function(data,type,row,full){
					if(can_qc_update) {
						return `<button class='btn btn-inverse-success play-recording'><i class='fas fa-play-circle'></i></button><button class='btn btn-inverse-info ml-2 save-qc'><i class="far fa-comments"></i></button><a href='#' class='btn btn-inverse-info ml-2 file-download'><i class='fa fa-download'></i></a><a href='' download id="${row['session_uuid']}"></a>`
					}
					else {
						return `<button class='btn btn-inverse-success play-recording'><i class='fas fa-play-circle'></i></button><a href='#' class='btn btn-inverse-info ml-2 file-download'><i class='fa fa-download'></i></a><a href='' download id="${row['session_uuid']}"></a>`
					}
				}
			},
			 {
                "targets": [ -3 ],
                "visible": false
            },
             {
                "targets": [ -1 ],
                "visible": true
            },
		],
		"fnCreatedRow": function(nRow, aData, iDataIndex) {
            key_name = Object.keys(aData)[0]
            $(nRow).attr('id', aData[key_name]);
        },
		dom: 'Bfrtip',
		lengthMenu: [
			[ 10, 25, 50, -1 ],
			[ '10 rows', '25 rows', '50 rows', 'Show all' ]
		],
		buttons:{
			dom:{
				button:{
					tag:'button',
					className:''
				}
			}
		},
		buttons: [
			{
				extend: 'pageLength',
				className: 'btn-outline-dark',
			},
			{
				extend: 'colvis',
				prefixButtons: [ show_hide_col_button ],
				className: 'btn-outline-dark',
			},
			visibility_col_dic
			]
	});
	if(col_list) {
		set_colums(callrecordings_table,col_list)
	}
	$(document).on('change', id + ' tbody input[type="checkbox"]', function(e) {
        var $row = $(this).closest('tr');
        if (this.checked) {
            result.push($row.attr("id"))
            $row.addClass('selected');
        } else {
            result = jQuery.grep(result, function(value) {
                return value != $row.attr("id");
            });
            $row.removeClass('selected');
        }
        // Prevent click event from propagating to parent
        e.stopPropagation()
    });
    // Handle click on "Select all" control
    $(document).on('change', '#example-select-all', function(e) {
        if (this.checked) {
            $(id + ' tbody input[type="checkbox"]:not(:checked)').trigger('click');
            // delete_highp = true
            result = query_set_list
            select_all_checked = true
        } else {
            $(id + ' tbody input[type="checkbox"]:checked').trigger('click');
            select_all_checked = false
            result = []
        }
        // Prevent click event from propagating to parent
        e.stopPropagation();
    });
    $(document).on('init.dt', id, function(e) {
        var flexyAvatar = new Vue({
            el: '.table',
            components: {
                avatar: VueAvatar.Avatar
            },
        });

        if (result) {
            $.each(result, function(index, value) {
                $(".card").find(id + " tbody tr[id=" + value + "] input[type='checkbox']").prop('checked', true);
                var $row = $(".card").find(id + " tbody tr[id=" + value + "]")
                $row.addClass("selected")
                    // $(".card "+id+ " tbody tr[id="+value+"] input[type='checkbox']").trigger("change")
                    // $(".card "+id+" tbody tr[id="+value+"] input[type='checkbox']").click()
            });
        } else {
            $(".card " + id + " tbody input[type='checkbox']:checked").trigger('click');
        }
    });
}

function setAudioTag(url, row_data){
	audio.src = url
	audio.load()
	$('#recordingPlay_modal').find('#rp_cust_number').text(row_data["customer_cid"])
	$('#recordingPlay_modal').find('#rp_agent').text(row_data["user"])
	$('#recordingPlay_modal').find('#rp_campaign').text(row_data["campaign_name"])
	$('#recordingPlay_modal').modal('show')
}

// play the audio file
$(document).on('click', '.play-recording', function(){
	$(this).parent('tr').addClass('highlighted_row')
	var url = ''
	var row_data = custom_pagination_table.row(row).data()
	var parent_path = `${location.protocol}//${row_data['ip_address']}/recordings`
	var row = $(this).parents('tr')
	var date = new Date(row_data['ring_time']);
	var file_date = `${("0" + date.getDate()).slice(-2)}-${("0" + (date.getMonth() + 1)).slice(-2)}-${date.getFullYear()}`
	var file_time = `${("0" + date.getHours()).slice(-2)}-${("0" + date.getMinutes()).slice(-2)}`
	if (date.setHours(0,0,0,0) != new Date().setHours(0,0,0,0)){
		parent_path = `${parent_path}/${file_date}`
	}
	$.ajax({
		url:`${parent_path}/${file_date}-${file_time}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`,
		type:'HEAD',
		error: function()
		{
			date = new Date(row_data['connect_time']);
			file_time = `${("0" + date.getHours()).slice(-2)}-${("0" + date.getMinutes()).slice(-2)}`
			$.ajax({
				url:`${parent_path}/${file_date}-${file_time}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`,
				type:'HEAD',
				error: function()
				{
					filenotfoundAlert()
				},
				success: function(){
					setAudioTag(`${parent_path}/${file_date}-${file_time}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`,row_data)
				}
			})
		},
		success: function()
		{
			setAudioTag(`${parent_path}/${file_date}-${file_time}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`,row_data)
		}
	});
});
// hide record play modal
$('#recordingPlay_modal').on('hide.bs.modal', function(){
	audio.pause()
	audio.src = ''
	audio.load()
	$('#recordingPlay_modal').find('#rp_cust_number, #rp_agent, #rp_campaign, #rp_init_time').text('')
})

// show record play modal
$('#recordingPlay_modal').on('shown.bs.modal', function(){
	audio.play()
})

// to download audio file
$(document).on('click','.file-download', function(e){
	e.preventDefault;
	$(this).parent('tr').addClass('highlighted_row')
	downlod_btn = $(this)
	var parent_path = `${location.protocol}//${row_data['ip_address']}/recordings`
	var row = $(this).parents('tr')
	var row_data = custom_pagination_table.row(row).data()
	var date = new Date(row_data['ring_time']);
	var file_date = `${("0" + date.getDate()).slice(-2)}-${("0" + (date.getMonth() + 1)).slice(-2)}-${date.getFullYear()}`
	var file_time = `${("0" + date.getHours()).slice(-2)}-${("0" + date.getMinutes()).slice(-2)}`
	if (date.setHours(0,0,0,0) != new Date().setHours(0,0,0,0)){
		parent_path = `${parent_path}/${file_date}`
	}
	$.ajax({
		url:`${parent_path}/${file_date}-${file_time}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`,
		type:'HEAD',
		error: function()
		{
			date = new Date(row_data['connect_time']);
			file_time = `${("0" + date.getHours()).slice(-2)}-${("0" + date.getMinutes()).slice(-2)}`
			$.ajax({
				url:`${parent_path}/${file_date}-${file_time}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`,
				type:'HEAD',
				error: function(){
					filenotfoundAlert()
				},
				success: function(){
					$('#'+row_data['session_uuid']).attr('href',`${parent_path}/${file_date}-${file_time}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`)
					$('#'+row_data['session_uuid']).attr('download',`${file_date}-${file_time}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`)
					$('#'+row_data['session_uuid'])[0].click()
				}
			})
		},
		success: function()
		{
			$('#'+row_data['session_uuid']).attr('href',`${parent_path}/${file_date}-${file_time}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`)
			$('#'+row_data['session_uuid']).attr('download',`${file_date}-${file_time}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`)
			$('#'+row_data['session_uuid'])[0].click()
		}
	});
})

// custom filter for recording report
$('#recording-report-filter').click(function(){
	callrecordings_table.draw()
})

// custom filter for report table
$('#custom-report-filter').click(function(){
	report_table.draw()
})
$('#report-filter').click(function(){
	customPaginationReport()
})

$(document).on('click', '.modify-callback', function(e){ 
	var callback_id = $(this).attr("data-id")
	var campaign = $("#row-"+callback_id+" td:eq(0)").text()
	var phonebook = $("#row-"+callback_id+" td:eq(1)").text()
	var user = $("#row-"+callback_id+" td:eq(2)").text().trim()
	var numeric = $("#row-"+callback_id+" td:eq(3)").text()
	var schedule_time = $("#row-"+callback_id+" td:eq(7)").text()
	var disposition = $("#row-"+callback_id+" td:eq(8)").text()
	var comment = $("#row-"+callback_id+" td:eq(9)").text()
	$("#callback-modal").find("#campaign").val(campaign)
	$("#callback-modal").find("#phonebook").val(phonebook)
	$("#callback-modal").find("#user").val(user).trigger('change');
	$("#callback-modal").find("#numeric").val(numeric)
	$("#callback-modal").find("#schedule_time").val(schedule_time)
	$("#callback-modal").find("#disposition").val(disposition)
	$("#callback-modal").find("#comment").val(comment)
	$("#callback-modal").find("#instance_id").val(callback_id)
	$("#callback-modal").modal("show")

})

$("#callback-modal, #abandoned-modal").on("hidden.bs.modal", function(){
	$("#pending-call-form").trigger("reset");
});

$(document).on('click', '.modify-abandoned', function(e){ 
	td_call_data = custom_pagination_table.row($(this).parents('tr')).data();
	$("#abandoned-modal").find("#campaign").val(td_call_data['campaign'])
	$("#abandoned-modal").find("#user").val(td_call_data['user']).trigger('change');
	$("#abandoned-modal").find("#full_name").val(td_call_data['full_name'])
	$("#abandoned-modal").find("#numeric").val(td_call_data['numeric'])
	$("#abandoned-modal").find("#status").val(td_call_data['status'])
	$("#abandoned-modal").find("#created_date").val(td_call_data['created_date'])
	$("#abandoned-modal").find("#instance_id").val(td_call_data['id'])
	$("#abandoned-modal").modal("show")
})

$("#schedule-report-btn").click(function() {
	mails = {}
	mails['from'] = $('#from_mails').val()
	mails['password'] = $('#password').val()
	mails['to'] = $('#to_mails').val().split(',')
	form = $('#report-scheduler-form')
	formdata = {'reports':JSON.stringify($('#reports').val()),
			'schedule_time':$('#schedule-timepicker_val').val(),
			'status':$('#status').val(),
			'emails':JSON.stringify(mails)}
	if(form.isValid()) {
		$.ajax({
			type: 'post',
			headers: {"X-CSRFToken": csrf_token},
			url: '/Modules/report-scheduler/',
			data:formdata,
			 beforeSend: function() {
                $('.preloader').fadeIn('fast');
            },
			success: function (data) {
                $('.preloader').fadeOut('fast');
				showSwal('success-message', 'Scheduler Successfully Created', '/dashboard/')
			},
		})
	}
})


function setQcAudioTag(row_data, dialler_event_data){
	var parent_path = `${location.protocol}//${location.hostname}/recordings`
	var date = new Date(row_data['ring_time']);
	var file_date = `${("0" + date.getDate()).slice(-2)}-${("0" + (date.getMonth() + 1)).slice(-2)}-${date.getFullYear()}`
	var file_time = `${("0" + date.getHours()).slice(-2)}-${("0" + date.getMinutes()).slice(-2)}`
	if (date.setHours(0,0,0,0) != new Date().setHours(0,0,0,0)){
		parent_path = `${parent_path}/${file_date}`
	}
	$.ajax({
		url:`${parent_path}/${file_date}-${file_time}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`,
		type:'HEAD',
		error: function()
		{
			date = new Date(row_data['connect_time']);
			file_time = `${("0" + date.getHours()).slice(-2)}-${("0" + date.getMinutes()).slice(-2)}`
			$.ajax({
				url:`${parent_path}/${file_date}-${file_time}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`,
				type:'HEAD',
				error: function(){
					$('#audio_file_error').removeClass('d-none')
				},
				success: function(){
					qc_audio.src = `${parent_path}/${file_date}-${file_time}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`
					qc_audio.load()
					$('#audio_file_error').addClass('d-none')
				}
			})
		},
		success: function()
		{
			qc_audio.src = `${parent_path}/${file_date}-${file_time}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`
			qc_audio.load()
			$('#audio_file_error').addClass('d-none')
		}
	});
	$('#recordingFeedback_modal').find('#customer_cid').text(dialler_event_data["customer_cid"])
	$('#recordingFeedback_modal').find('#call_duration').text(dialler_event_data["call_duration"])
	$('#recordingFeedback_modal').find('#comment').text(dialler_event_data["comment"])
	$('#recordingFeedback_modal').find('#customer_name').text(dialler_event_data["user__username"])
	$('#recordingFeedback_modal').find('#sub_disposition').text(dialler_event_data["feedback"])
	$('#recordingFeedback_modal').find('#supervisor').text(dialler_event_data["supervisor"])
	$('#recordingFeedback_modal').find('#primary_dispo').text(dialler_event_data['primary_dispo'])
	$('#recordingFeedback_modal').find('#username').text(dialler_event_data['user__username'])
	$('#recordingFeedback_modal').find('#feedback').val(dialler_event_data['prev_feedback'])
	$('#recordingFeedback_modal').modal('show')
}

// save the qc
recording_id=""
call_recording_session_uuid = ""
$(document).on('click', '.save-qc', function(){
	$(this).parent('tr').addClass('highlighted_row')
	var row = $(this).parents('tr')
	var row_data = custom_pagination_table.row(row).data()
	var date = new Date(row_data['ring_time']);
	var url = `${location.protocol}//${row_data['ip_address']}/recordings/${("0" + date.getDate()).slice(-2)}-${("0" + (date.getMonth() + 1)).slice(-2)}-${date.getFullYear()}-${("0" + date.getHours()).slice(-2)}-${("0" + date.getMinutes()).slice(-2)}_${row_data['customer_cid']}_${row_data['session_uuid']}.mp3`
	recording_id = row_data["id"]
	call_recording_session_uuid = row_data["session_uuid"]
	$.ajax({
		url:'/CallReports/CallRecordingsDetail/'+row_data["id"]+'/',
		type:'get',
		error: function()
		{
		},
		success: function(data)
		{
			setQcAudioTag(row_data, data.dialler_event_data);
		}
	});
});

// hide record play modal
$('#recordingFeedback_modal').on('hide.bs.modal', function(){
	qc_audio.pause()
	qc_audio.src = ''
	qc_audio.load()
	$("#recording-form .reset-label").text("")
	$("#feedback").val("")
	$('#audio_file_error').addClass('d-none')
	// $('#recordingPlay_modal').find('#rp_cust_number, #rp_agent, #rp_campaign, #rp_init_time').text('')
})

$("#cancel_recording").click(function(){
	$("#feedback").val("")
	$("#recordingFeedback_modal").modal("hide")
})

$(document).on('click', '#submit-recording-feedback', function(){
	$.ajax({
		url:'/CallReports/CallRecordingsDetail/'+recording_id+'/',
		type:'post',
		headers: {
                "X-CSRFToken": csrf_token
            },
		data:{"feedback":$("#feedback").val(), "session_uuid":call_recording_session_uuid},
		error: function()
		{
		},
		success: function(data)
		{
			$(".recording_feedback_msg").removeClass("d-none")
			setTimeout(function(){
            $('.recording_feedback_msg').addClass('d-none');
            $("#recordingFeedback_modal").modal("hide")
            $("#row"+recording_id).addClass("feedback_saved")
        },3000)         
		}
	});

})
$('#alternate-number-delete').click(function(){
	if(result.length>0){
		confirmDelete('warning-message-and-cancel', 'Ok','delete')
	}else{
		$('#upload-alternate-delete-contact').modal('show');
	}
})