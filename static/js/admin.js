//jquery to check restrict sidebar menu by permissions
// jquery for datatables with select option
result = []
is_download = false
delete_highp = false
crmfield_page = false
leadlistpriority_page = false
select_all_checked = false
var dateNow = new Date("October 13, 2014 02:00:00");
is_refresh_lead_list = false
var current_selectd={trc:false,tap:false,tapd:false,period:''};

$(".form-control").attr('autocomplete', 'off');
$('.form-control').on('input', function() {
    var c = this.selectionStart,
       r = /[^a-z./@#_%$*:;()+-0123456789+ ]/gi,
       v = $(this).val();
    if(r.test(v)) {
      $(this).val(v.replace(r, ''));
      c--;
    }
    if(c){
        this.setSelectionRange(c, c);
    }
});
function format_datetime_forlistingpages(datetime) {
    if (datetime) {
        return moment(datetime).format("YYYY-MM-DD");
    } else {
        return ''
    }
}


function selective_datatable(table) {
    var id = '#' + table.attr('id');
    custom_pagination_table = $(table).DataTable({
        "aaSorting": [],
        "bPaginate": false,
        "bInfo": false,
        "searching": false,
        "processing": true,
        "language": {
            processing: '<i class="fa fa-spinner fa-spin fa-3x fa-fw"></i><span class="sr-only">Loading...</span> '
        },
        responsive: {
            details: {
                display: $.fn.dataTable.Responsive.display.modal({
                    header: function(row) {
                        var data = row.data();
                        key = Object.keys(data)[0];
                        return 'Details for ' + data[key];
                    }
                }),
                renderer: $.fn.dataTable.Responsive.renderer.tableAll({
                    tableClass: 'table'
                })
            }
        },
        columnDefs: [{
            responsivePriority: 1, targets: 0
        }, {
            responsivePriority: 2, targets: 1
        }, {
            responsivePriority: 3, targets: -1
        }, {
            responsivePriority: 4, targets: -2
        },{
            targets: [0, -2],
            orderable: false,
            width: "1%"
        }, {
            targets: [-1],
            orderable: false,
            width: "16%"
        }, {
            targets: "download_data",
            render: function(data, type, row) {
                if (!row['0']) {
                    if (data.indexOf("div") != -1) {
                        return data
                    } else {
                        if (row["downloaded_file_name"] != '') {
                            return '<div class="text-right"><a target="_blank" class="btn btn-link text-info ml-2 file-download p-0" href="/api/download/'+row['id']+'/'+row['downloaded_file_name']+'/" download id="file-' + row['id'] + '" id="'+row['id']+'"><i class="fa fa-download sch-download"></i></a></div>'
                            // return '<div class="text-right"><a class="btn btn-link text-info ml-2 file-download p-0" href="'+row['downloaded_file_path']+'" download id="file-' + row['id'] + '" id="'+row['id']+'"><i class="fa fa-download sch-download"></i></a></div>'
                        }
                    }
                    return ''
                } else {
                    return data
                }
            }
        },{
            targets: "improper_data",
            render: function(data, type, row) {
                if (!row['0']) {
                    if (data.indexOf("div") != -1) {
                        return data
                    } else {
                        if (row["improper_file_name"] != '') {
                            // return '<a href="/media/upload/' + row["improper_file_name"] + '" download id="file-' + row['id'] + '">' + row['improper_file_name'] + '</a>'
                            return '<a href="' + row["improper_file_name"] + '" download id="file-' + row['id'] + '">' + row['improper_file_name'] + '</a>'
                        }
                    }
                    return ''
                } else {
                    return data
                }
            }
        }, {
            targets: "percentage",
            render: function(data, type, row) {
                if (!row['0']) {
                    if(data=='File not created / Data not available' || data=='In Progress'){
                        return '<p class="text-success" id="success-' + row['id'] + '"> '+data+' </p>'
                    }
                    if (data == 0) {
                        return '<p id="success-' + row['id'] + '"></p>'
                    }
                    if (data == '' || data != 100) {
                        return '<p id="success-' + row['id'] + '"></p>'
                    } else {
                        return '<p class="text-success" id="success-' + row['id'] + '">Completed</p>'
                    }
                } else {
                    return '<p id="success-' + row['id'] + '"></p>'
                }
            }
        }, {
            targets: "avatar",
            render: function(data, type, row) {
                key_name = Object.keys(row)[0]
                return '<div class="circle2">' + row[key_name].charAt(0).toUpperCase() + '</div>'
            }
        }, {
            targets: "name",
            render: function(data, type, row) {
                return '<a href=' + edit_url.replace("123", row["id"]) + ' class="name-el">' + data + '</a>'
            }
        }, {
            targets: "modal_name",
            render: function(data, type, row) {
                new_url = modal_url.replace("***", row['id']).replace("link_name", data)
                return new_url
            }
        }, {
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
        }, {
            targets: "action",
            render: function(data, type, row) {
                if (!row["0"]) {
                    data = {
                        "can_update": can_update,
                        "can_delete": can_delete,
                        "inst_id": row["id"],
                        "isUser": false,
                        "username": '',
                        "isPhonebook": false,
                        "username":"",
                        "role":"",
                        "destination_role_name":"",
                        "addCss":""
                    }
                    if(crmfield_page || leadlistpriority_page) {
                        data["addCss"] = "d-none"
                    }
                    if (location.pathname.indexOf("Users") != -1) {
                        data["isUser"] = true
                        if ('extension' in row) {
                            data['extension'] = row['extension']
                        }
                        if('role_name' in row) {
                            data['destination_role_name'] = row['role_name']
                        }
                        data['username'] = user_name
                        data["role"] = user_role
                    }
                    if (location.pathname.indexOf("phonebook") != -1) {
                        data["isPhonebook"] = true
                    }
                    if (edit_url) {
                        data["edit_url"] = edit_url.replace("123", row["id"])
                    } else {
                        new_url = option_url.replace("***", row['id'])
                        data["modal_url"] = new_url
                    }
                    if(row["status"] == "Active"){
                        data["active_action"] = "Make InActive"
                    }
                    else{
                        data["active_action"] = "Make Active"
                    }
                    var cust_template = `<div class='dropdown show'>
                            <button class='btn btn-secondary dropdown-toggle table-dropdown' role='button' id='dropdownMenuLink' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>
                                Choose Action</button>
                            {{#can_update }}
                            <div class='dropdown-menu' aria-labelledby='dropdownMenuLink'>
                            {{#edit_url}}
                            <a class='dropdown-item' href='{{edit_url}}'>Modify</a>
                            {{/edit_url}}
                            {{#modal_url}}
                                modal_url
                            {{/modal_url}}
                            {{#isUser}}
                            <a class='dropdown-item reset-agentPassword' href='' data-toggle='modal' data-target='#reste_user_password_modal' data-id='{{inst_id}}'>Reset Password</a>
                            <a class='dropdown-item reset-agent_wfh_Password' href='' data-toggle='modal' data-target='#reset_wfh_password_modal' data-id='{{inst_id}}'>Reset WFH Password</a>
                            <a class='dropdown-item' onclick='confirmEmergencyLogout("{{extension}}", "{{username}}", "{{role}}", "{{destination_role_name}}")'>Emergency Logout</a>
                            {{/isUser}}
                            {{#isPhonebook}}
                            <a class='dropdown-item' onclick='lead_list_churn({{inst_id}})' >List Churn</a>
                            <a class='dropdown-item' onclick="phonebook_download('download',{{inst_id}})">Download</a>
                            {{/isPhonebook}}
                            <div class='dropdown-divider {{addCss}}'></div>
                            <a class='dropdown-item {{addCss}}' onclick="confirmActiveStatus('delete_one', 'Ok','particular_entry-{{ inst_id}}-{{active_action}}')">{{active_action}}</a>
                            {{/can_update}}
                            {{#can_delete }}
                            <div class='dropdown-divider'></div>
                            <a class='dropdown-item' onclick="confirmDelete('delete_one', 'Ok','particular_entry-{{ inst_id}}')">Delete</a>
                            {{/can_delete}}
                            </div>
                            </div>`
                    var html = Mustache.to_html(cust_template, data);
                    html = html.replace("modal_url", data["modal_url"])
                    return html
                }
                return data
            }
        },
        {
            targets: "download_action",
            render: function(data, type, row) {
                if (!row["0"]) {
                    data = {
                        "can_update": can_update,
                        "can_delete": can_delete,
                        "inst_id": row["id"],
                        "isUser": false,
                        "username": '',
                        "isPhonebook": false,
                        "username":"",
                        "role":"",
                        "destination_role_name":""
                    }
                    
                    new_url = option_url.replace("***", row['id'])
                    data["modal_url"] = new_url
                    
                    var cust_template = '<div>'
                    if(row['download_actions']['start']){
                        cust_template += `<button class='btn btn-link text-primary p-1' onclick="confirmAction('action', 'Ok', 'Start','{{ inst_id}}')" title="Re-Download"><i class="fas fa-undo-alt"></i></button>`
                    }
                    if(row['download_actions']['stop']){
                        cust_template += `<button class="btn btn-link text-primary p-1" onclick="confirmAction('action', 'Ok', 'Stop' ,'{{ inst_id}}')" title="Stop"><i class="fas fa-stop"></i></button>`
                    }
                    if(row['download_actions']['delete']){
                        cust_template += `<button class="btn btn-link text-danger p-1" onclick="confirmDelete('delete_one', 'Ok','particular_entry-{{ inst_id}}')" title="Delete"><i class="fas fa-trash"></i></button>`
                    }
                    cust_template += `</div>`
                    var html = Mustache.to_html(cust_template, data);
                    html = html.replace("modal_url", data["modal_url"])
                    return html
                }
                return data
            }
        },
        {
            "targets": "demon_service_action",
            render: function(data, type, row) {
                if (row['status'] == 'active'){
                    render_sting = `<button class="btn btn-link text-danger p-1" title="Stop" onclick="daemon_action('${data}','stop')"><i class="fas fa-stop"></i></button>`
                }  else {
                    render_sting = `<button class="btn btn-link text-success p-1" title="Start" onclick="daemon_action('${data}','start')"><i class="fas fa-play"></i></button>`
                }
                render_sting += `<button class="btn btn-link text-primary p-1" title="Restart" onclick="daemon_action('${data}','restart')"><i class="fas fa-undo-alt"></i></button>`
                return render_sting
            }
        },
        {
        "targets": "list_date",  
        render: function(data, type, row) {
            return format_datetime_forlistingpages(data)
            }  
        },
        {
            "targets": "state_col",
            "orderable": false,
            render: function(data) {
                if(data == "active"){
                    return `<span class='state-dot' style='background-color: #04B76B;'></span>`
                } else {
                    return `<span class='state-dot' style='background-color: #FF5E6D;'></span>`
                }
            }
        }

        ],
        "fnCreatedRow": function(nRow, aData, iDataIndex) {
            key_name = Object.keys(aData)[1]
            $(nRow).attr('id', aData[key_name]);
        }
    });

    // Handle click on checkbox
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
function contactInfoTable(table, column_data, col_list=[]) {
    // var id = '#'+ table.attr('id');
    var table_instance = table.DataTable({
        "scrollX": true,
        "serverSide": true,
        "processing": true,
        "searching": false,
        "language": {
            processing: '<i class="fa fa-spinner fa-spin fa-3x fa-fw"></i><span class="sr-only">Loading...</span> '
        },
        "ajax": {
            "url": '/CRM/ContactInfo/',
            "headers": {
                "X-CSRFToken": csrf_token
            },
            "type": "POST",
            "data": function(d) {
                d.format = "datatables"
                d.campaign = $('#contact_campaign_select').val()
                d.phonebook = $('#contact_phonebook_select').val()
                d.user = $('#contact_agent_select').val()
                d.numeric = $('#destination_extension').val()
                d.disposition = $('#disposition').val()
                d.start_date = $('#start-date input').val()
                d.end_date = $('#end-date input').val()
                d.uniqueid = $('#uniqueid').val()
            },
        },
        "columns": column_data,
        columnDefs: [{
            "targets": '_all',
            "defaultContent": " ",
        }, {
            targets: [0],
            render: function(data, type, row) {
                return '<a class="name-el contact-info" href="#">' + data + '</a>'
            }

        }, {
            targets: [-1],
            orderable: false,
            data: 'id',
            render: function(data) {
                return `<div class="dropdown show">
                    <button class="btn btn-secondary dropdown-toggle table-dropdown" role="button" id="dropdownMenuLink"'
                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Choose Action</button>
                    <div class="dropdown-menu" aria-labelledby="dropdownMenuLink">
                    <a class="dropdown-item contact-info" href="#">Modify</a></div></div>`
                }
            },
        ],
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
            prefixButtons: [{
                text:'Show/Hide all columns',
                action: function ( e, dt, node, config ) {
                    e.preventDefault()
                    if(dt.column().visible()){
                        dt.columns().visible(false)
                    }else {
                        dt.columns().visible(true)
                    }
                }
            }],
            className: 'btn-outline-dark',
        },
        {
        text: 'Save column visibility',
        className: 'btn-outline-dark',
        action: function ( e, dt, node, config ) {
            var col_name = []
            var report_name = $("#report_name").val()
            $(".dataTables_scrollHeadInner th").each(function(index) {
                temp_name = $(this).attr("class").split(" ")
                if (temp_name) {
                    col_name.push(temp_name[0])
                }
            });
            console.log(col_name,"col nameeee")
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
        ]
        // pageLength: 2
    });
    if(col_list.length>0) {
        $(".dataTables_scrollHeadInner th").each(function(index) {
            temp_name = $(this).attr("class").split(" ")
            if (temp_name) {
                temp_name = temp_name[0]
                if ($.inArray(temp_name, col_list) == -1) {
                    // report_table.column(index).visible(true)
                    table_instance.column(index).visible(false)   
                }

            }
            
        });

    }
    return table_instance
}

$("#user_access_level").change(function() {
    if ($("#user_access_level option:selected").text() == "admin" && $("#superuser_div").hasClass("d-none")) {
        $("#superuser_div").removeClass("d-none")
    } else {
        $("#superuser_div").addClass("d-none")
        $("#superuser_chkbox").prop("checked", false)
    }
})
var validationForm = $("#user-form");
var csrf_token = $("input[name='csrfmiddlewaretoken']").val()
move = false
ajaxOptions = {
    type: 'post',
    headers: {
        "X-CSRFToken": csrf_token
    },
    url: '/UserManagement/check-user/',
    async: false,
    success: function(response_data) {
        if ($.isEmptyObject(response_data) == false) {
            if ("username" in response_data) {
                $("#username-msg").addClass("has-error")
                $("#username-msg").html("<span class='help-block form-error'>" + response_data["username"] + "</span>")
            }
            if ("extension" in response_data) {
                $("#extension-msg").addClass("has-error")
                $("#extension-msg").html("<span class='help-block form-error'>" + response_data["extension"] + "</span>")
            }
            if ("email" in response_data) {
                $("#email-msg").addClass("has-error")
                $("#email-msg").html("<span class='help-block form-error'>" + response_data["email"] + "</span>")
            }
            move = false
            return false
        } else {
            move = true
            $("#extension-msg").html("")
            $("#email-msg").html("")
            $("#username-msg").html("")
        }
    },
    error: function(data) {

        // setTimeout(function(){ $("#login-error-msg").addClass("d-none") }, 3000);
    }
}
$("#create-user-btn").click(function() {
    var form = $("#user-create-form")
    if ($("#caller_id").val() != "") {
        $("#caller_id").attr("data-validation", "length")
    }
    if ($("#email").val() != "") {
        $("#email").attr("data-validation", "email")
    }
    var existing_user = $("#existing_user_data").val()

    if (existing_user != "") {
        $("#existing_user").val(existing_user)
    }
    if(form.isValid() && strong) {
        $.ajax({
            type: 'post',
            headers: {"X-CSRFToken": csrf_token},
            url: '/UserManagement/Users/create/',
            data: form.serialize(),
            beforeSend: function() {
                $('.preloader').fadeIn('fast');
            },
            success: function (data) {
                $('.preloader').fadeOut('fast');
                showSwal('success-message', 'User Successfully Created', '/UserManagement/Users/')
            },
            error: function (data) {
                $('.preloader').fadeOut('fast');
		if (data["responseJSON"]["errors"]&& 'employee_id' in data["responseJSON"]["errors"]) {
                    $("#employee_id-error").html(`<span class="help-block form-error">${data["responseJSON"]["errors"]["employee_id"]}</span>`).addClass('has-error')
                    $("#employee_id").removeClass("valid").addClass("error")
                }
                if (data["responseJSON"]["errors"] && !('employee_id' in data["responseJSON"]["errors"]) ) {
                    $(".user-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
                    setTimeout(function(){ $(".user-err-msg").addClass("d-none") }, 3000);
                }
                if (data["responseJSON"]["email_id"]){
                    $("#email-error").html(`<span class="help-block form-error">${data["responseJSON"]["email_id"]}</span>`).addClass("has-error")
                    $("#email").removeClass("valid").addClass("error")                  
                }
                if (data["responseJSON"]["caller_id"]){
                    $("#callerid-error").html(`<span class="help-block form-error">${data["responseJSON"]["caller_id"]}</span>`).addClass("has-error")
                    $("#caller_id").removeClass("valid").addClass("error")
                }
                if (data["responseJSON"]["extension"]){
                    $("#extension-error").html(`<span class="help-block form-error">${data["responseJSON"]["extension"]}</span>`).addClass("has-error")
                    $("#extension").removeClass("valid").addClass("error")
                }
                if (data["responseJSON"]["username"]) {
                    $("#user-name-error").html(`<span class="help-block form-error">${data["responseJSON"]["username"]}</span>`).addClass('has-error')
                    $("#username").removeClass("valid").addClass("error")
                }
                if (data["responseJSON"]["wfh_numeric"]) {
                    $("#wfh_numeric-error").html(`<span class="help-block form-error">${data["responseJSON"]["wfh_numeric"]}</span>`).addClass('has-error')
                    $("#wfh_numeric").removeClass("valid").addClass("error")
                }
            }
        }); 
    }
    if(strong == false){
         $("#strong_password").text("Please enter a strong Password").removeClass("d-none")
        setTimeout(function(){
            $('#strong_password').addClass('d-none')
        },3000)
    }
})
$(document).on('change', '#show_all_fields', function() {
    $("#basic_info, #group-div").toggleClass("d-none")
})
$(document).on('change', '#existing_user_data', function() {
        var user_id = $(this).val()
        $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/api/fetch-existing-data/',
            data: {
                "instance_id": user_id,
                "app_label": "callcenter",
                "model_name": "User",
                "serializer": "UserSerializer"
            },
            success: function(data) {
                var user_data = data["instance_info"]
                $("#group").val(user_data["group"])
                $("#group").change()
                $("#user_timezone").val(user_data["user_timezone"])
                $("#is_active").val(user_data["is_active"])
                $("#user_role").val(user_data["user_role"])
                $("input[name=call_type][value=" + user_data['call_type'] + "]").prop('checked', true);
                if (user_data["user_role"]) {
                    $("#user_role").change()
                    if (user_data["reporting_to"]) {
                        $("#user_access_level").val(user_data["reporting_to"])
                    }
                } else {
                    $("#reporting-row").addClass("d-none")
                }
            },
            error: function(data) {
                if (data["responseJSON"]["errors"]) {
                    $(".user-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
                    setTimeout(function() {
                        $(".user-err-msg").addClass("d-none")
                    }, 3000);
                }
            }
        });
    })
    // $('#user-form  #datepicker-popup, #user-edit-form #datepicker-popup').datepicker({
    //  endDate: '+0d',
    //      enableOnReadonly: true,
    //      todayHighlight: true,
    //      format: 'yyyy-mm-dd',
    // });

// $('body').on('focus',".start-date, .end-date", function(){
//     $(this).datepicker({
//      enableOnReadonly: true,
//      todayHighlight: true,
//      format: 'yyyy-mm-dd',
//      orientation: 'bottom auto',
//  autoclose: true,
//  })
// })

$("#user_role").change(function() {
    var current_val = $('option:selected', this).attr('data-level');
    if (current_val != "Admin") {
        var access_level = manager_access = ""
        if (current_val == "Manager") {
            access_level = "Admin"
        } else if (current_val == "Supervisor") {
            access_level = "Admin"
            manager_access = "Manager"
        }
        $("#reporting-row").removeClass("d-none")
        $("#user_access_level").val("")
        $('#user_access_level option').attr('selected', false);
        $("#reporting-row option[value='']").attr("selected", "selected").removeClass("d-none")
        var ext_user = $("#ext_reporting_to").val()
        if (access_level) {
            $('#user_access_level option[data-access="' + access_level + '"]').removeClass("d-none")
            $('#user_access_level option[data-access!="' + access_level + '"]').addClass("d-none")
            if (manager_access) {
                $('#user_access_level option[data-access="' + manager_access + '"]').removeClass("d-none")
                    // $('#user_access_level option[data-access!="'+manager_access+'"]').addClass("d-none")
            }

        } else {
            $('#user_access_level option').removeClass("d-none")
        }
        if (ext_user != "") {
            $("#user_access_level").val(ext_user)
            ext_user = ""
        }
    } else {
        $("#reporting-row").addClass("d-none")
    }
})

$('#user_trunk').change(function(){
    $('#user_caller_id option').remove()
    $('#user_caller_id').append(`<option value=''>Select Caller ID</option>`)
    if($(this).val()){
        let dids = $(this).find(':selected').data('did_range')
        let did_range = dids.split(",")
        let start_end = did_range[0]
        if (did_range[1] == undefined) {
            end_node = start_end
        }
        else {
            end_node = did_range[1]
        }
        let is_leading_zero = false
        let start_end_length = start_end.length
        if (start_end.match(/^0+/)) {
            is_leading_zero = true
        }
        let is_leading_plus = false
        if(start_end.startsWith("+")){
            is_leading_plus = true
        }
        for (i = start_end; i <= end_node; i++) {

            let did_value = (is_leading_zero) ? i.toString().padStart(start_end_length,"0") : i.toString()
            did_value = (is_leading_plus) ? did_value.toString().padStart(start_end_length,"+") : did_value.toString()
            if(used_did_list){
                if(used_did_list.indexOf(did_value.toString()) === -1){
                    $("#user_caller_id").append(`<option value='${did_value}'>${did_value}</option>`)
                }else{
                     $("#user_caller_id").append(`<option value='${did_value}' disabled>${did_value}</option>`)
                }    
            }else{
                $("#user_caller_id").append(`<option value='${did_value}'>${did_value}</option>`)
            }
        }
    }
})
// hide and show user form according to selected template

// $(document).on('change', '#template_type', function() {
//  if ()
// })

$(document).on('click', '.reset-agent_wfh_Password', function() {
    var agentId = $(this).attr('data-id');
    $("#reset_wfh_password_form #wfh_rp_agentId").val(agentId);
})
var resetPasswordform = $("#reset_wfh_password_form ");
resetPasswordform.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        var form = $("#reset_wfh_password_form")
        if (form.isValid()) {
            $.ajax({
                type: 'post',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/api/wfh_reset_password/',
                data: form.serialize(),
                success: function(data) {
                    showSwal('success-message', data['msg'], '/UserManagement/Users/')
                },
                error: function(data) {
                    if (data["responseJSON"]["error"]) {
                        $("#old-password-msg").append('<span class="help-block form-error">' + data["responseJSON"]["error"] + '<span>')
                            .removeClass("d-none").addClass('has-error').parent().find('input').addClass('error')
                    }
                }
            })
        }
    }
});



//reset password reset form on modal hide
$('#reste_user_password_modal').on('hidden.bs.modal', function() {
    $('#reset_user_password_form')[0].reset()
});

$(document).on('click', '.reset-agentPassword', function() {
    var agentId = $(this).attr('data-id');
    $("#reset_user_password_form #rp_agentId").val(agentId);
})
var resetPasswordform = $("#reset_user_password_form");
resetPasswordform.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        var form = $("#reset_user_password_form")
        if (form.isValid()) {
            var psw = Base64.encode($("#psw").val());
            var confirm_password = Base64.encode($("#confirm_password").val());
            $("#psw").val(psw)
            $("#confirm_password").val(confirm_password)
            var form = $("#reset_user_password_form")
            $.ajax({
                type: 'post',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/api/reset_password/',
                data: form.serialize(),
                success: function(data) {
                    showSwal('success-message', data['msg'], '/UserManagement/Users/')
                },
                error: function(data) {
                    var psw = Base64.decode($("#psw").val());
                    var confirm_password = Base64.decode($("#confirm_password").val());
                    $("#psw").val(psw)
                    $("#confirm_password").val(confirm_password)
                    if (data["responseJSON"]["error"]) {
                        $("#old-password-msg").append('<span class="help-block form-error">' + data["responseJSON"]["error"] + '<span>')
                            .removeClass("d-none").addClass('has-error').parent().find('input').addClass('error')
                    }
                }
            })
        }
    }
});

$(document).on('click', '.reload, #refresh-page', function() {
    if(is_download==false){
        location.reload();
    }
    is_download = false
});

/*this function is related to the department form validation and submission */
$(document).on('click', '.group-modify', function() {
    $(".dtr-bs-modal").modal('hide');
    var pk = parseInt($(this).attr("data-groupid"));
    $.ajax({
        type: 'post',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/UserManagement/get-group/' + pk + '/',
        success: function(data) {
            selected_user = []
            $('#update_group_name').val(data.querysets['name'])
            $('#update-group-color').val(data.querysets['color_code'])
            $.each(data.queryset, function(index, value) {
                selected_user.push(value['id'])
                $('#update_user_in_group').append($("<option selected></option>").attr("value", value['id']).text(value['username']));
            })
            $.each(data.allusers, function(index, value) {
                $('#update_user_in_group').append($("<option ></option>").attr("value", value['id']).text(value['username']));
            })

            $('.asColorPicker-trigger').find('span').css("background-color", data.querysets['color_code'])
            $('form').find('#update_group_status').val(data.querysets['status'])
            if (data.querysets['is_edit'] == "false"){
                $('form').find('#update_group_status').css("pointer-events", "none");
                $("#module_status").removeClass("d-none")
            }
            else {
                $('form').find('#update_group_status').css("pointer-events", "");
                $("#module_status").addClass("d-none")
            }
            $('#group_pk').val(pk)
            $('#user_add_list').val(selected_user)
            $('#modal_update_group').modal('show');
        },
        error: function(data) {}
    });
});

var group_update_form = $("#update-group-form");
group_update_form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        var pk = $('#group_pk').val()
        if (group_update_form.isValid() == true) {
            console.log(740, '------')
            $.ajax({
                type: 'PUT',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/UserManagement/get-group/' + pk + '/',
                data: group_update_form.serialize(),
                success: function(data) {
                    showSwal('success-message', 'Group Successfully Updated')
                },
                error: function(data) {
                    if ("name" in data["responseJSON"]) {
                        $("#group-msg").addClass("has-error").html(
                            '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass("d-none")
                        setTimeout(function() {
                            $("#group-msg").addClass("d-none")
                        }, 3000);
                    }
                }
            });
        };
    }
});

var group_validation_form = $("#group-form");
group_validation_form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        if (group_validation_form.isValid() == true) {
            $.ajax({
                type: 'post',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/UserManagement/Groups/',
                data: group_validation_form.serialize(),
                success: function(data) {
                    showSwal('success-message', 'Group Successfully Created')
                },
                error: function(data) {
                    if ("name" in data["responseJSON"]) {
                        $("#group-name-msg").addClass("has-error").html(
                            '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass("d-none")
                        setTimeout(function() {
                            $("#group-name-msg").addClass("d-none")
                        }, 3000);
                    }
                }
            });
        };
    }
});

var pending_call_form = $("#pending-call-form");
pending_call_form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/api/pending-call-update-user/',
            data: pending_call_form.serialize(),
            success: function(data) {
                showSwal('success-message', 'Pending Call Successfully Updated')
            },
            error: function(data) {}
        });
    }
});

var pending_abandoned_form = $("#pending-abandoned-form");
pending_abandoned_form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/api/update-abandoned-call-user/',
            data: pending_abandoned_form.serialize(),
            success: function(data) {
                showSwal('success-message', 'Pending Call Successfully Updated')
            },
            error: function(data) {}
        });
    }
});


/* department form validation function ends here */

/* this functions is used to validate the duplicates of selected users in other groups */
$('#close_group_update').click(function() {
    $('#update_user_in_group').html('')
})
$('#modal_update_group').on('hidden.bs.modal', function(e) {
        $('#update_user_in_group').html('')
    })
    /* end of the duplicates validation here */

/*this function is related to the Switch form validation and submission */
$(document).on('click', '#switch-modify, .switch-modify', function() {
    var pk = parseInt($(this).attr("data-switchid"));
    $.ajax({
        type: 'post',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/CampaignManagement/get-switch/' + pk + '/',
        success: function(data) {
            $('#modal_title').text('Update Switch')
            $('#header_id').text('Update Switch')
            $('#subheader_id').text('Change ')
            $('#switch_name').val(data.querysets['name'])
            $('#ip_address').val(data.querysets['ip_address'])
            $('#status').val(data.querysets['status'])
            $('#sip_udp_port').val(data.querysets['sip_udp_port'])
            $('#rpc_port').val(data.querysets['rpc_port'])
            $('#wss_port').val(data.querysets['wss_port'])
            $('#event_socket_port').val(data.querysets['event_socket_port'])
            if (data.querysets['is_edit'] == "false"){
                $('#status').css("pointer-events", "none");
                $("#module_status").removeClass("d-none")
            }
            else {
                $('#status').css("pointer-events", "");
                $("#module_status").addClass("d-none")
            }
            $('#update_switch_pk').val(pk)
            $('#modal_add_switch').modal('show');
            //showSwal('success-message', 'User Group Successfully Created')
        },
        error: function(data) {

        }
    });
});
var switch_validation_form = $("#switch-form");
switch_validation_form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        if (switch_validation_form.isValid() == true) {
            var url = '/CampaignManagement/Switch/'
            var switch_id = $("#update_switch_pk").val()
            if (switch_id){
                var url = '/CampaignManagement/get-switch/' + switch_id + '/'
            }
            $.ajax({
                type: 'put',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: url,
                data: switch_validation_form.serialize(),
                success: function(data) {
                    if(switch_id) {
                        showSwal('success-message', 'Switch Successfully Updated')
                    }
                    else {
                        showSwal('success-message', 'Switch Successfully Created')
                    }
                },
                error: function(data) {
                    if ("name" in data["responseJSON"]) {
                        $("#switch_name").removeClass('valid').addClass('error');
                        $("#switch_name_msg").addClass("has-error").html(
                            '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass("d-none")
                        setTimeout(function() {
                            $("#switch_name_msg").addClass("d-none")
                        }, 3000);
                    }
                    if ("ip_address" in data["responseJSON"]) {
                        $("#ip_address").removeClass('valid').addClass('error');
                        $("#switch_ip_address_msg").addClass("has-error").html(
                            '<span class="help-block form-error">' + data["responseJSON"]["ip_address"] + '</span>').removeClass("d-none")
                        setTimeout(function() {
                            $("#switch_ip_address_msg").addClass("d-none")
                        }, 3000);
                    }
                }
            });
        };
    }
});
/* server form validation function ends here */

// create the trunk country code

$(document).on('change','#trunk_type',function(){
    var trunk_type = $('#trunk_type:checked').val()
    var prefix_check = $('#prefix').prop('checked')
    $('#prefix').prop('checked',false)
    $('.country_code_radio:radio').prop('checked',false)
    $('#country_code_select').val('').change()
    $('#selected_county_code').val('')
    $('#domestic_code, #county_code_div').addClass('d-none')
})

$(document).on('change','#prefix',function(){
    var prefix_check = $('#prefix').prop('checked')
    var trunk_type = $('#trunk_type:checked').val()
    if(trunk_type != ''){
        if(prefix_check){
            if(trunk_type =='international'){
                $('#county_code_div').removeClass('d-none')
                $('#domestic_code').addClass('d-none')
            }else{
                $('#domestic_code').removeClass('d-none')
                $('#county_code_div').addClass('d-none')
            }
        }else{
            $('#selected_county_code').val('')
            $('.country_code_radio:radio').prop('checked',false)
            $('#country_code_select').val('').change()
            $('#domestic_code, #county_code_div').addClass('d-none')
        }
    }else{
        $('#domestic_code, #county_code_div').removeClass('d-none')
        $('#prefix').prop('checked',false)
        $('.country_code_radio:radio').prop('checked',false)
        $('#selected_county_code').val('')
        $('#country_code_select').val('').change()
    }

})

$(document).on('change','.country_code_radio',function(){
    var radio_check = $('.country_code_radio:checked').val()
    if(radio_check){
        $('#create_county_code').val(radio_check)
    }else{
        $('#create_county_code').val('')
    }
})
$(document).on('change','#country_code_select', function(){
    var code_select = $(this).val()
    if(code_select){
        $('#selected_county_code').val(code_select)
        $('#create_county_code').val(code_select)
    }else{
        $('#create_county_code').val('')
    }
})
/****************update trunk **********************/

$(document).on('change','#update_trunk_type',function(){
    var trunk_type = $('#update_trunk_type:checked').val()
    var prefix_check = $('#update_prefix').prop('checked')
    $('#update_prefix').prop('checked',false)
    $('.update_country_code_radio:radio').prop('checked',false)
    $('#update_trunk_prefix').removeClass('d-none')
    $('#update_country_code_select').val('').change()
    $('#updated_selected_county_code').val('')
    $('#update_domestic_code, #update_country_code_div').addClass('d-none')
})

$(document).on('change','#update_prefix',function(){
    var prefix_check = $('#update_prefix').prop('checked')
    var trunk_type = $('#update_trunk_type:checked').val()
    if(trunk_type != ''){
        if(prefix_check){
            if(trunk_type =='international'){
                $('#update_country_code_div').removeClass('d-none')
                $('#update_domestic_code').addClass('d-none')
            }else{
                $('#update_domestic_code').removeClass('d-none')
                $('#update_country_code_div').addClass('d-none')
            }
        }else{
            $('#updated_selected_county_code').val('')
            $('.update_country_code_radio:radio').prop('checked',false)
            $('#update_country_code_select').val('').change()
            $('#update_domestic_code, #update_country_code_div').addClass('d-none')
        }
    }else{
        $('#update_domestic_code, #update_country_code_div').removeClass('d-none')
        $('#update_prefix').prop('checked',false)
        $('.update_country_code_radio:radio').prop('checked',false)
        $('#updated_selected_county_code').val('')
        $('#update_country_code_select').val('').change()
    }

})

$(document).on('change','.update_country_code_radio',function(){
    var radio_check = $('.update_country_code_radio:checked').val()
    if(radio_check){
        $('#update_county_code').val(radio_check)
    }else{
        $('#update_county_code').val('')
    }
})
$(document).on('change','#update_country_code_select', function(){
    var code_select = $(this).val()
    if(code_select){
        $('#updated_selected_county_code').val(code_select)
        $('#update_county_code').val(code_select)
    }else{
        $('#update_county_code').val('')
    }
})

/*this function is related to the Dial Trunk form validation and submission */
$(document).on('click', '.trunk-modify', function() {
    $(".dtr-bs-modal").modal('hide');
    var pk = $(this).attr("data-trunk")
    $.ajax({
        type: 'post',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/CampaignManagement/get-dialtrunk/' + pk + '/',
        success: function(data) {
            $('#update_trunk_name').val(data.querysets['name'])
            $('#update_dial_string').val(data.querysets['dial_string'])
            if(data.querysets['did_range']) {
                var did_range = data.querysets['did_range'].split(",")
                $('#update_start_did').val(did_range[0])
                $('#update_end_did').val(did_range[1])
            }
            $('#update_channel_count').val(data.querysets['channel_count'])
            $("#update_trunk_type[value='"+data.querysets['trunk_type']+"']").prop('checked', true);
            $('#update_trunk_switch').val(data.querysets['switch']).change();
            $('#update_trunk_status').val(data.querysets['status']).change();
            $('#update_prefix').prop('checked',data.querysets['prefix'])
            if(data.querysets['prefix']){
                if(data.querysets['trunk_type'] == 'international'){
                    $('#update_country_code_div ,#update_trunk_prefix').removeClass('d-none')
                    $('#update_country_code_select').val(data.querysets['country_code']).change()
                    $('#updated_selected_county_code').val(data.querysets['country_code'])
                }
                if(data.querysets['trunk_type'] == 'domestic'){
                  $('#update_domestic_code, #update_trunk_prefix').removeClass('d-none')  
                  if(data.querysets['country_code'] == '0'){
                        $(".update_country_code_radio[value='0']").prop('checked',true)
                    }else if (data.querysets['country_code'] == '91'){
                        $(".update_country_code_radio[value='91']").prop('checked',true)
                    }else{
                       $('.update_country_code_radio:radio').prop('checked',false) 
                    }
                }

            }
            $('#update_county_code').val(data.querysets['country_code'])
            if (data.querysets['is_edit'] == "false"){
                $('#update_trunk_status').css("pointer-events", "none");
                $("#module_status").removeClass("d-none")
            }
            else {
                $('#update_trunk_status').css("pointer-events", "");
                $("#module_status").addClass("d-none")
            }
            $('#update_trunk_pk').val(pk)
            $('#modal_update_trunk').modal('show');
            //showSwal('success-message', 'User Group Successfully Created')
        },
        error: function(data) {

        }
    });
});

var dialtrunk_update_form = $("#update-trunk-form");
dialtrunk_update_form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        var pk = $('#update_trunk_pk').val()
        var pk = $('#update_trunk_pk').val()
        var start=$("#update_start_did").val()
        var end=$("#update_end_did").val()
        var did_range =start+","+end
        valid_dids= true
        did_list =[]
        valid_dids= check_valid_dids(start,end)
        $("#update_hidden_did_range").val(did_range)
        if (dialtrunk_update_form.isValid() == true && parseInt(start) <= parseInt(end) && valid_dids == true) {
            console.log(dialtrunk_update_form.serialize())
            $.ajax({
                type: 'put',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/CampaignManagement/get-dialtrunk/' + pk + '/',
                data: dialtrunk_update_form.serialize(),
                success: function(data) {
                    showSwal('success-message', 'Dial Trunk Successfully Updated')
                },
                error: function(data) {
                    if ("name" in data["responseJSON"]) {
                        $("#update_trunk_name_msg").addClass("has-error").html(
                            '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass("d-none")
                        setTimeout(function() {
                            $("#update_trunk_name_msg").addClass("d-none")
                        }, 3000);
                    }
                }
            });
        }
        else {
        $(".trunk_range_msg").removeClass("d-none")
        setTimeout(function() {
                        $(".trunk_range_msg").addClass("d-none")
                    }, 3000);
        }
    }
});

function check_valid_dids(start,end){
    return (parseInt(end)-parseInt(start)<=2000)?true:false
}

var dialtrunk_validation_form = $("#trunk-form");
dialtrunk_validation_form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        var pk = $('#trunk_pk').val()
        var start=$("#start_did").val()
        var end=$("#end_did").val()
        var did_range =start+","+end
        valid_dids= check_valid_dids(start,end)

        $("#hidden_did_range").val(did_range)
        if (dialtrunk_validation_form.isValid() == true && parseInt(start) <= parseInt(end) && valid_dids == true) {
            $.ajax({
                type: 'post',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/CampaignManagement/DialTrunk/',
                data: dialtrunk_validation_form.serialize(),
                success: function(data) {
                    showSwal('success-message', 'Dial Trunk Successfully Created')
                },
                error: function(data) {
                    if ("name" in data["responseJSON"]) {
                        $("#trunk_name_msg").addClass("has-error").html(
                            '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass("d-none")
                        setTimeout(function() {
                            $("#trunk_name_msg").addClass("d-none")
                        }, 3000);
                    }
                }
            });
        }
         else {
            $(".trunk_range_msg").removeClass("d-none")
            setTimeout(function() {
                            $(".trunk_range_msg").addClass("d-none")
                        }, 3000);
        }
    }
});
/* Dial trunk form validation function ends here */

$("#modal_update_disposition").on('hidden.bs.modal', function() {
    $("#update-disposition-form")[0].reset();
    $('.dispo-tags').next('.tagsinput').remove();
    $('.dispo-tags').val('');
    $('.dispo-tags').removeAttr('data-tagsinput-init');
    $('.dispo-tags').attr('id', 'update_dispo_tag')
        // $('.dispo-tags').show();
});
/*this function is related to the disposition form validation and submission */
var dispo_update_form = $("#update-disposition-form");
dispo_update_form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        var pk = $('#update_dispo_pk').val()
        if (dispo_update_form.isValid() == true) {
            $.ajax({
                type: 'put',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/CampaignManagement/get-disposition/' + pk + '/',
                data: dispo_update_form.serialize(),
                success: function(data) {
                    showSwal('success-message', 'Department Successfully Created')
                },
                error: function(data) {
                    if ("name" in data["responseJSON"]) {
                        $("#dispo-name-msg").addClass("has-error").html(
                            '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass(
                            "d-none")
                        setTimeout(function() {
                            $("#dispo-name-msg").addClass("d-none")
                        }, 3000);
                    }
                }
            });
        };
    }
});

var dispo_validation_form = $("#disposition-form");
dispo_validation_form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        if ($("#tags").val() != "") {
            tags = true
        } else {
            tags = false
            $("#subdispo-msg").addClass("has-error").html(
                '<span class="help-block form-error">This is a required field</span>')
            setTimeout(function() {
                $("#primarydispo-msg").addClass("d-none")
            }, 3000);
        }
        if (dispo_validation_form.isValid() == true && tags == true) {
            $.ajax({
                type: 'post',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/CampaignManagement/Dispositions/',
                data: dispo_validation_form.serialize(),
                success: function(data) {
                    showSwal('success-message', 'Dispositions Successfully Created')
                },
                error: function(data) {
                    if ("name" in data["responseJSON"]) {
                        $("#primarydispo-msg").addClass("has-error").html(
                            '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass(
                            "d-none")
                        setTimeout(function() {
                            $("#primarydispo-msg").addClass("d-none")
                        }, 3000);
                    }
                }
            });
        };
    }
});
/* disposition form validation function ends here */

/*this function is related to the pausebreaks form validation and submission */
$(document).on('click', '#pausebreak-modify, .pausebreak-modify', function() {
    var pk = parseInt($(this).attr("data-pbid"));
    $.ajax({
        type: 'post',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/CampaignManagement/get-pausebreak/' + pk + '/',
        success: function(data) {
            $('#update_pausebreak_name').val(data.querysets['name'])
            $('#update-break-pick-color').val(data.querysets['break_color_code'])
            $('.asColorPicker-trigger').find('span').css('background-color', data.querysets['break_color_code'])
            $('#update_status').val(data.querysets['status'])
            if (data.querysets['is_edit'] == "false"){
                $('#update_status').css("pointer-events", "none");
                $("#module_status").removeClass("d-none")
            }
            else {
                $('#update_status').css("pointer-events", "");
                $("#module_status").addClass("d-none")
            }
            $('#update_pausebreak_pk').val(pk)
            $('#update_inactive_on_exceed').prop('checked',data.querysets['inactive_on_exceed'])
             if($('#update_inactive_on_exceed').prop('checked')){
                    $('#update_pausebreak-time-input').prop('readonly',false)
                  }else{
                    $('#update_pausebreak-time-input').prop('readonly',true)
                  }
            $("#update_pausebreak-time input").val(data.querysets['break_time'])
            $("#update_pausebreak-time").datetimepicker({
                format: 'HH:mm',
                UseCurrent: 'day',
                pickerPosition: 'top-right'
            });
            $('#modal_update_pausebreak').modal('show');
        },
        error: function(data) {
            if ("name" in data["responseJSON"]) {
                $("#primarydispo-msg").addClass("has-error").html(
                    '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass(
                    "d-none")
                setTimeout(function() {
                    $("#primarydispo-msg").addClass("d-none")
                }, 3000);
            }
        }
    });
});
// pause break update model hide
$("#modal_update_pausebreak, #modal_add_pausebreak").on('hidden.bs.modal', function() {
    $("#update-pausebreak-form, #pausebreak-form")[0].reset();
    $("#pausebreak-time-input").val("02:00");
    // $('.pb-tags').next('.tagsinput').remove();
    // $('.pb-tags').val('');
    // $('.pb-tags').removeAttr('data-tagsinput-init');
    // $('.pb-tags').attr('id','update_pausebreak_tags')
    //    // $('.dispo-tags').show();
});
var pausebreak_update_form = $("#update-pausebreak-form");
pausebreak_update_form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        var pk = $('#update_pausebreak_pk').val()
        var ajax_call = true
        var break_time = $('#update_pausebreak-time-input').val()
        if (break_time == '00:00') {
            var ajax_call = false
            $("#up_err_msg").removeClass('d-none')
            setTimeout(function() {
                $("#up_err_msg").addClass("d-none")
            }, 3000);
        }
        if (pausebreak_update_form.isValid() == true && ajax_call == true) {
            $.ajax({
                type: 'put',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/CampaignManagement/get-pausebreak/' + pk + '/',
                data: pausebreak_update_form.serialize(),
                success: function(data) {
                    showSwal('success-message', 'Pausebreak Successfully Updated')
                },
                error: function(data) {
                    if ("name" in data["responseJSON"]) {
                        $("#update_pausebreak_name").removeClass('valid').addClass('error');
                        $("#pausebreak-msg").addClass("has-error").html(
                            '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass(
                            "d-none")
                        setTimeout(function() {
                            $("#pausebreak-msg").addClass("d-none")
                        }, 3000);
                    }
                }
            });
        };
    }
});

var pausebreak_validation_form = $("#pausebreak-form");
pausebreak_validation_form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        var ajax_call = true
        var break_time = $('#pausebreak-time-input').val()
        if (break_time == '00:00') {
            var ajax_call = false
            $("#err_msg").removeClass('d-none')
            setTimeout(function() {
                $("#err_msg").addClass("d-none")
            }, 3000);
        }
        if (pausebreak_validation_form.isValid() == true && ajax_call == true) {
            $.ajax({
                type: 'post',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/CampaignManagement/Pausebreaks/',
                data: pausebreak_validation_form.serialize(),
                success: function(data) {
                    showSwal('success-message', 'Pausebreaks Successfully Created')
                },
                error: function(data) {
                    if ("name" in data["responseJSON"]) {
                        $("#pausebreak_name").removeClass('valid').addClass('error');
                        $("#pausebreak-name-msg").addClass("has-error").html(
                            '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass(
                            "d-none")
                        setTimeout(function() {
                            $("#pausebreak-name-msg").addClass("d-none")
                        }, 3000);
                    }

                }
            });
        };
    }
});

/* pausebreaks form validation function ends here */

/*this function is related to the user groups form validation and submission */
// var usergroup_validation_form = $("#user_group_form");

// usergroup_validation_form.children("div").steps({
//  headerTag: "h3",
//  bodyTag: "section",
//  transitionEffect: "slideLeft",
//  onFinished: function(event, currentIndex) {
//      if (usergroup_validation_form.isValid()==true){
//          $.ajax({
//              type: 'post',
//              headers: {"X-CSRFToken": csrf_token},
//              url: '/UserManagement/UserRoles/',
//              data: usergroup_validation_form.serialize(),
//              success: function (data) {
//                  showSwal('success-message', 'User Group Successfully Created')
//              },
//              error: function (data) {
//              }
//          });
//      };
//  }
// });

$('#create-role-btn').click(function() {
    var permissions = {}
    if ($('#ur_create_form').isValid() == true) {
        $.each($('.permission_check'), function() {
            var curr_element = $(this).attr("data-id");
            var access_array = new Array();
            var checked_input = $('#' + curr_element + '_module input:checked')
            $.each(checked_input, function() {
                access_array.push(($(this).attr("id")));
            });
            permissions[curr_element] = access_array
        });
        permissions = JSON.stringify(permissions)
        $('#permissions_input').val(permissions);
        $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            data: $('#ur_create_form').serialize(),
            success: function(data) {
                showSwal('success-message', 'User Role Successfully Created', '/UserManagement/UserRoles/')
            },
            error: function(data) {
                if ("name" in data["responseJSON"]) {
                    $('#role_name').removeClass('valid').addClass('error');
                    $("#name-msg").addClass("has-error").html(
                        '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass(
                        "d-none")
                    setTimeout(function() {
                        $("#name-msg").html("").removeClass('has-error')
                    }, 3000);
                }
            }
        });
    }
})

$(document).on('click', '#update-role-btn', function() {
    var update_permissions = {}
    if ($('#ur_update_form').isValid() == true) {
        $.each($('.permission_check'), function() {
            var curr_element = $(this).attr("data-id");
            var access_array = new Array();
            var checked_input = $('#' + curr_element + '_module input:checked')
            $.each(checked_input, function() {
                access_array.push(($(this).attr("id")));
            });
            update_permissions[curr_element] = access_array
        });
        update_permissions = JSON.stringify(update_permissions)
        $('#permissions_input').val(update_permissions);
        $.ajax({
            type: 'put',
            headers: {
                "X-CSRFToken": csrf_token
            },
            data: $('#ur_update_form').serialize(),
            success: function(data) {
                showSwal('success-message', 'User Role Successfully Updated', '/UserManagement/UserRoles/')
            },
            error: function(data) {
                if ("name" in data["responseJSON"]) {
                    $('#role_name').removeClass('valid').addClass('error');
                    $("#name-msg").addClass("has-error").html(
                        '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass(
                        "d-none")
                    setTimeout(function() {
                        $("#name-msg").html("").removeClass("has-error")
                    }, 3000);
                }
            }
        });
    }
})

$(document).on('change', '#global_dnc', function() {
    if (this.checked) {
        $('#dnc_campaign').val(null).trigger('change');
        $('#dnc_campaign').prop('disabled', true)
    } else {
        $('#dnc_campaign').prop('disabled', false)
    }
})
var create_edit_dnc_form = $("#create_edit_dnc_form");
create_edit_dnc_form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        if (create_edit_dnc_form.isValid() == true) {
            var type = 'post'
            var pk = $('#dnc_number_pk').val()
            if (pk) {
                type = 'put'
            }
            $.ajax({
                type: type,
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/Administration/dnc/create_edit/',
                data: create_edit_dnc_form.serialize(),
                success: function(data) {
                    showSwal('success-message', data['success'])
                },
                error: function(data) {
                    if ("name" in data["responseJSON"]) {
                        $("#trunk_name_msg").addClass("has-error").html(
                            '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass("d-none")
                        setTimeout(function() {
                            $("#trunk_name_msg").addClass("d-none")
                        }, 3000);
                    }
                }
            });
        };
    }
});
$(document).on('click', '.dnc-modify', function() {
    var pk = parseInt($(this).attr("data-dncid"));
    $.ajax({
        type: 'get',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/Administration/dnc/create_edit/',
        data: {
            'pk': pk
        },
        success: function(data) {
            $('#dnc_numeric').val(data['numeric'])
            if (data['global_dnc']) {
                $('#dnc_campaign').val(null).trigger('change');
                $('#dnc_campaign').prop('disabled', true)
            } else {
                $('#dnc_campaign').val(data['campaign']).trigger('change');
            }
            $('#dnc_status').val(data['status'])
            $('#global_dnc').prop('checked', data['global_dnc'])
            $('#dnc_number_pk').val(pk)
            $('#create-edit-dnc-modal').modal('show');
            //showSwal('success-message', 'User Group Successfully Created')
        },
        error: function(data) {
            console.log(data['responseJSON'])
        }
    });
});
$('#create-edit-dnc-modal').on('hidden.bs.modal', function() {
    $("#create_edit_dnc_form").trigger("reset");
    $('#dnc_campaign').val(null).trigger('change');
})

function wizardvalidation(validationForm) {
    validationForm.children("div").steps({
        headerTag: "h3",
        bodyTag: "section",
        transitionEffect: "slideLeft",
        onStepChanging: function(event, currentIndex, newIndex) {
            validationForm.val({
                ignore: [":disabled", ":hidden"]
            })
            validationForm.isValid();
            if (validationForm.isValid() == true) {
                return validationForm.val();
            }
        },
        onFinishing: function(event, currentIndex) {
            validationForm.val({
                ignore: [':disabled']
            })
            validationForm.isValid();
            if (validationForm.isValid() == true) {;
                return validationForm.val();
            }
        },
        onFinished: function(event, currentIndex) {
            showSwal('success-message', 'User Successfully Created')
        }
    });
}
$("#user-wizard-modal").on('hidden.bs.modal', function() {
    $("#user-form")[0].reset();
});

$("#uploaded-file").click(function(e) {
    $("#uploaded-file").val("")
    $(".confirm-user-upload, .confirm-dnc-upload, .cancel-uploaded-file, #proper-data, #improper-data").addClass("d-none")
    $(".dropify-clear").click()
    $("#validate-phonebook-file").removeClass("d-none")
})

$("#uploaded-file").change(function(e) {
        var fileName = e.target.files[0].name;
        $(".proper_data_div, .improper_data_div").addClass("d-none")
        if (fileName) {
            $(".validate-uploaded-file").removeClass("d-none")
            $(".dropify-render").text("").addClass("csv-download")
        }
    })
    // $(".phonebook-upload-file").change(function(e) {
    //  var fileName = e.target.files[0].name;
    //  if (fileName) {
    //      $(".confirm-edit-phone, .cancel-uploaded-file").addClass("d-none")
    //  }
    // })
uploadOptions = {
    cache: false,
    processData: false,
    contentType: false,
    beforeSend: function() {
        $('.preloader').fadeIn('fast');
    },
    success: function(data) {
        $('.preloader').fadeOut('fast');
        $('.phonebook-valid-loader,.user-valid-loader').fadeOut('fast');
        if (typeof data == "string"){
            var blob=new Blob([data]);
            var link=document.createElement('a');
            link.href=window.URL.createObjectURL(blob);
            link.download="user_upload_stats.csv";
            link.click();
            uploadFailAlert()
        }else if ("column_err_msg" in data) {
            $(data["column_id"]).text(data["column_err_msg"]).removeClass("d-none")
            if ($("#uploadedad-file-error").length == 0) {
                error_id = "#phonebook-err-msg"
            } else {
                error_id = "#upload-file-error"
            }
            setTimeout(function() {
                $(error_id).addClass("d-none")
            }, 5000);
        } else if ("empty_file" in data) {
            $('#empty-data').removeClass('d-none').html(data["empty_file"])
            setTimeout(function() {
                $("#empty-data").addClass("d-none")
            }, 3000);
        } else {
            showSwal('success-message', 'User Bulk Uploaded Sucessfully')
            // $(".cancel-uploaded-file").removeClass("d-none")
            // $(".validate-uploaded-file").addClass("d-none")
            // if ("correct_file" in data) {
            //     $("#proper-data").attr("href", data["correct_file"]).removeClass("d-none")
            //     $(".confirm-user-upload").removeClass("d-none")
            //     $("#proper-data span.msg").text("Proper Data: " + data["correct_count"])
            //     $(".proper_data_div").removeClass("d-none")
            // }
            // if ("incorrect_file" in data) {
            //     $(".improper_data_div").removeClass("d-none")
            //     $("#improper-data").attr("href", data["incorrect_file"]).removeClass("d-none")
            //     $("#improper-data span.msg").text("Improper Data: " + data["incorrect_count"])
            //     $('#empty-data').addClass('d-none')
            // }
        }
    },
    error: function(data) {
        $('.preloader').fadeOut('fast');
        $('.phonebook-valid-loader,.user-valid-loader').fadeOut('fast');
    },
}

// This Function is used to validate user uploaded file
$("#validate-uploaded-file").click(function() {
    var data = new FormData($('#user-upload-form').get(0));
    uploadOptions["data"] = data
    uploadOptions["url"] = $('#user-upload-form').attr('action')
    uploadOptions["type"] = $('#user-upload-form').attr('method')
    var fileExtension = ['csv', 'xls', 'xlsx'];
    if ($(".dropify-filename-inner").text()) {
        if ($.inArray($(".dropify-filename-inner").text().split('.').pop().toLowerCase(), fileExtension) == -1) {
            $("#upload-file-error").text("File format must be csv").removeClass("d-none")
            setTimeout(function() {
                $("#upload-file-error").addClass("d-none")
            }, 3000);
        } else {
            $.ajax(uploadOptions);
        }
    } else {
        $("#upload-file-error").text("Upload File To Validate").removeClass("d-none")
        setTimeout(function() {
            $("#upload-file-error").addClass("d-none")
        }, 3000);
    }

});

// This Function is used to validate phonebook uploaded file
$("#validate-phonebook-file").click(function() {
    var data = new FormData($('#phonebook-form').get(0));
    uploadOptions["data"] = data
    uploadOptions["url"] = $('#phonebook-form').attr('action')
    uploadOptions["type"] = $('#phonebook-form').attr('method')
    var fileExtension = ['csv', 'xls', 'xlsx'];
    if ($(".dropify-filename-inner").text()) {
        if ($.inArray($(".dropify-filename-inner").text().split('.').pop().toLowerCase(), fileExtension) == -1) {
            $("#phonebook-err-msg").text("File format must be csv").removeClass("d-none")
            setTimeout(function() {
                $("#phonebook-err-msg").addClass("d-none")
            }, 3000);
        } else if ($('#phonebook-campaign').val() == '') {
            $("#phonebook-err-msg").text("Select Campaign to validate the data").removeClass("d-none")
            setTimeout(function() {
                $("#phonebook-err-msg").addClass("d-none")
            }, 3000);
        } else {
            $('.phonebook-valid-loader').fadeIn('fast');
            $.ajax(uploadOptions);
        }
    } else {
        $("#phonebook-err-msg").text("Upload File To Validate").removeClass("d-none")
        setTimeout(function() {
            $("#phonebook-err-msg").addClass("d-none")
        }, 3000);
    }
});

$("#validate-dnc-file").click(function() {
    var form = new FormData($('#dnc-upload-form').get(0));
    var fileExtension = ['csv', 'xls', 'xlsx'];
    if ($(".dropify-filename-inner").text()) {
        if ($.inArray($(".dropify-filename-inner").text().split('.').pop().toLowerCase(), fileExtension) == -1) {
            $("#dnc-file-error").text("File format must be ['csv', 'xls', 'xlsx']").removeClass("d-none")
            setTimeout(function() {
                $("#dnc-file-error").addClass("d-none")
            }, 3000);
        } else {
            $.ajax({
                type: "POST",
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: "/Administration/dnc/",
                data: form,
                cache: false,
                processData: false,
                contentType: false,
                success: function(data) {
                    if ("column_err_msg" in data) {
                        $(data["column_id"]).text(data["column_err_msg"]).removeClass("d-none")
                        setTimeout(function() {
                            $(data["column_id"]).addClass("d-none")
                        }, 5000);
                    } else if ("empty_file" in data) {
                        $('#empty-data').removeClass('d-none').html(data["empty_file"])
                        setTimeout(function() {
                            $("#empty-data").addClass("d-none")
                        }, 3000);
                    } else {
                        $(".cancel-uploaded-file").removeClass("d-none")
                        $(".validate-uploaded-file").addClass("d-none")
                        if ("correct_file" in data) {
                            $("#proper-data").attr("href", data["correct_file"]).removeClass("d-none")
                            $(".confirm-dnc-upload").removeClass("d-none")
                            $("#proper-data span.msg").text("Proper Data: " + data["correct_count"])
                            $(".proper_data_div").removeClass("d-none")
                        }
                        if ("incorrect_file" in data) {
                            $(".improper_data_div").removeClass("d-none")
                            $("#improper-data").attr("href", data["incorrect_file"]).removeClass("d-none")
                            $("#improper-data span.msg").text("Improper Data: " + data["incorrect_count"])
                            $('#empty-data').addClass('d-none')
                        }
                    }
                },
                error: function(data) {}
            });
        }
    } else {
        $("#dnc-file-error").text("Upload File To Validate").removeClass("d-none")
        setTimeout(function() {
            $("#dnc-file-error").addClass("d-none")
        }, 3000);
    }
});


$("#cancel-uploaded-file, #confirm-upload-file").click(function() {
    data = {}
    current_element = $(this)
    if ($(this).hasClass("confirm-user-upload")) {
        data["perform_upload"] = true
    }
    var proper_file = $("#proper-data").attr("href")
    var improper_file = $("#improper-data").attr("href")
    data["proper_file"] = proper_file
    data["improper_file"] = improper_file
    $.ajax({
        type: 'post',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/UserManagement/Users/upload-operation/',
        data: data,
        beforeSend: function() {
          $('.preloader').fadeIn('fast');
        },
        success: function(data) {
            $('.preloader').fadeOut('fast');
            if (current_element.hasClass("confirm-user-upload")) {
                showSwal('success-message', 'User Uploaded Successfully')
            } else {
                showSwal('success-message', 'Upload Operation Cancelled')
            }
            $(".dropify-clear").click()
            $("#proper-data, #improper-data, #confirm-upload-file, #cancel-uploaded-file").addClass("d-none")
            $("#validate-uploaded-file").removeClass("d-none")
        },
        error: function(data) {},
    });
})

$(document).on("click", ".dropify-clear", function() {
    $("#validate-uploaded-file, #upload-priority").addClass("d-none")
    $(".proper_data_div, .improper_data_div").addClass("d-none")
    $(".dropify-filename-inner").text("")
})

// code related to create phonebook
$(".create-phonebook, #cancel-phonebook-upload").click(function() {
    var current_element = $(this)
    if($("#action_type").val()=="transfer_contacts"){
        $('.preloader').fadeIn('fast');
        var form = new FormData($('#phonebook-form').get(0));
        $.ajax({
                type: 'post',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/CRM/phonebook/transfer_contacts/' + phonebook_id + '/',
                data: form,
                cache: false,
                processData: false,
                contentType: false,
                success: function(data) {
                    if (current_element.hasClass("confirm-edit-phone")) {
                        $('.preloader').fadeOut('fast');
                        showSwal('success-message', 'Contacts transfer successfully', "/CRM/phonebook/")
                    }
                },
                error: function(data) {
                    $('.preloader').fadeOut('fast');
                    if (data["responseJSON"]["errors"]) {
                        $("#phonebook-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
                        setTimeout(function() {
                            $("#phonebook-err-msg").addClass("d-none")
                        }, 3000);
                    }

                }
            });        

    }
    else{
        var url = '/CRM/create-phonebook/'
        $("#phonebook-form").attr("href", "")
        if ($(this).hasClass("confirm-edit-phone")) {
            url = '/CRM/phonebook/edit/' + phonebook_id + '/'
        }
        var form = new FormData($('#phonebook-form').get(0));
        var form_valid = $('#phonebook-form')
        if (form_valid.isValid()) {
            $('.preloader').fadeIn('fast');
            $.ajax({
                type: 'post',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: url,
                data: form,
                cache: false,
                processData: false,
                contentType: false,
                success: function(data) {
                    $('.preloader').fadeOut('fast');
                    if (current_element.hasClass("confirm-edit-phone")) {
                        showSwal('success-message', 'List updated Successfully', "/CRM/phonebook/")
                    } else {
                        showSwal('success-message', 'List created Successfully', "/CRM/phonebook/")
                    }
                },
                error: function(data) {
                    $('.preloader').fadeOut('fast');
                    if (data["responseJSON"]["errors"]) {
                        $("#phonebook-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
                        setTimeout(function() {
                            $("#phonebook-err-msg").addClass("d-none")
                        }, 3000);
                    }

                }
            });
        }
    }
})
$("#phonebook_name").keyup(function() {
    $("#phonebook_slug").val($(this).val())
})

// Code related to campaign
// $(document).on('change', '#campaign-server', function() {
//     if ($(this).val() != "") {
//         $('form').find("#carrier-div").removeClass("d-none")
//         $('form').find("#carrier_list").val("")
//         $('form').find('#carrier_list option[data-server="' + $(this).val() + '"]').removeClass("d-none")
//         $('form').find('#carrier_list option[data-server!="' + $(this).val() + '"]').addClass("d-none")
//     } else {
//         $('form').find("#carrier-div").addClass("d-none")
//     }
// })

function campaign_pre_save_validation (form) {
    $(".selected-groups .badge-pill").each(function(){ 
        $(form).append("<input type='hidden' name='group' value='"+$(this).attr("data-id")+"'>")
    })
    $(".selected-disposition .badge-pill").each(function(){ 
        $(form).append("<input type='hidden' name='disposition' value='"+$(this).attr("data-id")+"'>")
    })
    $(".selected-relationtag .badge-pill").each(function(){ 
        $(form).append("<input type='hidden' name='relation_tag' value='"+$(this).attr("data-id")+"'>")
    })
    $(".selected-agents-status .badge-pill").each(function(){ 
        $(form).append("<input type='hidden' name='breaks' value='"+$(this).attr("data-id")+"'>")
    })
    if($('#prioritize-status').val()!='' && $('#prioritize-status').val()!=null){
        var prioritize_data = {}
        var priority_data = {}
        priority_data[$('input[type=radio][name=prioritize]:checked').val()] = true
        priority_data['status'] = $('#lead-priority-status').val()
        if($('input[type=radio][name=prioritize]:checked').val()==='tapd'){
            priority_data['period'] = $("#prioritize-period").val()
        }
        prioritize_data[$("#prioritize-status").val()] = priority_data
        prioritize_data = JSON.stringify(prioritize_data)
        $(form).append("<input type='hidden' name='lead_priotize' value='"+prioritize_data+"'>")
    }else{
         var prioritize_data = {}
         prioritize_data = JSON.stringify(prioritize_data)
        $(form).append("<input type='hidden' name='lead_priotize' value='"+prioritize_data+"'>")
    }
    var dial_method =  {}
    dial_method["manual"] = $("#campaign_manual").prop("checked")
    dial_method["inbound"] = $("#campaign_inbound").prop("checked")
    dial_method["ibc_popup"] = $("#ibc_popup").prop("checked")
    dial_method["sticky_agent_map"] = $("#sticky_id").prop("checked")
	dial_method["ivr"] = $("#ivr").prop("checked")
    dial_method['no_agent_audio'] = $("#no_agent_audio").prop("checked")
    dial_method['lead_api_campaign'] = $("#lead_api_campaign").prop("checked")
	if ($("#camp_outbound_check").prop("checked") == false) {
		dial_method["outbound"] = false
	}
	else {
		dial_method["outbound"] = $("#camp_outbound").val()
	}
	var dial_method_flag = true
	if (dial_method["manual"] == false && dial_method["inbound"] == false && $("#camp_outbound_check").prop("checked") == false) {
		$("#dial_method_msg").removeClass("d-none")
		$(".dial_method_div").addClass("border_color")
		dial_method_flag = false
	}
	else {
		$("#dial_method_msg").addClass("d-none")
		$(".dial_method_div").removeClass("border_color")
	}
	var api_mode_method = {}
	$("#dial_method").val(JSON.stringify(dial_method))

	// if($('#thirdparty_url').prop("checked") || $('#dap_url').prop("checked")){
	// 	var mode_selected = $('#api_mode_select').val()
	// 	api_mode_method[mode_selected] = $('#api_weburl').val()
	// 	api_mode_method['parameters'] = {}
	// 	$.each($('#api_parameters').select2('data'),function(index,val){
	// 		api_mode_method['parameters'][val['text']] = val['id']
	// 	})
	// }
	// $('#api_mode_select').change(function(){
	// 	if($('#api_mode_select').val() != ''){
	// 		$('#api_url_div, #api_url_div').removeClass('d-none')
	// 	}else{
	// 		$('#api_mode_select').attr('data-validation', 'required')

	// 	}
	// })

    valid =true
    var wfh_dict ={}
    $.each(wfh_vue.wfh_list,function(index,val){
        wfh_dict[index+1] = val
    })
    $('#wfh_dispo').val(JSON.stringify(wfh_dict))
    $('#weburl').val(JSON.stringify(api_mode_method))
    var vb_data = {};
    var vb_dtmf = {};
    if(voice_blaster_vue.vb_mode == '1'){
        if($($('.hint2mention').summernote('code')).text().trim() == ""){
            valid = false
            voice_blaster_vue.hasError = true
        } else {
            voice_blaster_vue.hasError = false
        }
    }
    if($('.hint2mention').length > 0){
        vb_data['vb_speech'] = $($('.hint2mention').summernote('code')).text().trim()
    }else{
        vb_data['vb_speech'] = ''
    }
    vb_data['vb_crm_fields'] = vb_crm_fields
    vb_data['hasDTMF'] = voice_blaster_vue.hasDTMF
    vb_data['vb_call_after'] = voice_blaster_vue.vb_call_after
    vb_data['vb_audio_duration'] = voice_blaster_vue.vb_audio_duration
    $.each(voice_blaster_vue.vb_dtmf, function(index,value){
        if(value){
            if(index+1 == 10){
                vb_dtmf[0] = value
            } else {
                vb_dtmf[index+1] = value
            }
        }
    })
    vb_data['vb_dtmf'] = vb_dtmf
    $('#vb_data').val(JSON.stringify(vb_data))
    var lead_recycle_dict = []
    incomplete_lead = false
    $('#accordion').children('div').each(function (i,current_child) {
        var lead_name = $(this).find(".lead_name").val()
        var lead_id = $(this).find(".existing_lead_id").val()
        var lead_count = $(this).find("#count").val()
        var schedule_type = $(this).find("#schedule_type").val()
        flag = empty_lead  = false
        default_dispo = ['CBR','Invalid Number','NC','Abandonedcall','Drop']
        $.merge(avail_dispo_list,default_dispo)
        if (avail_dispo_list.includes(lead_name) || lead_name == "Select Disposition"){
            flag = true
        }
        else {
            flag = false
        }
        if(lead_name == "Select Disposition") {
            lead_name = ""
        }
        if(schedule_type == "Select Time"){
            schedule_type = ""
        }
        if (flag ) {
            if (lead_name) {
                if (lead_count && schedule_type) {
                    child_dict = {}
                    child_dict["name"] = lead_name
                    child_dict["count"] = lead_count
                    if ($(this).find("#lr_start_time").val() && $(this).find("#lr_end_time").val()) {
                        date_dict = {"start_time": $(this).find("#lr_start_time").val(), "end_time": $(this).find("#lr_end_time").val()}
                        child_dict["schedule_period"] = JSON.stringify(date_dict)
                    }
                    else {
                        if (schedule_type == "schedule_time") {
                            incomplete_lead = true
                        }
                    }
                    child_dict["recycle_time"] = $(this).find("#lead_time").attr("data-interval")
                    child_dict["status"] = $(this).find("#lead-status").val()
                    child_dict["lead_id"] = lead_id
                    if (schedule_type) {
                        child_dict["schedule_type"] = schedule_type
                    }
                    lead_recycle_dict.push(child_dict)
                }
                else {
                    incomplete_lead = true
                    return false
                }
                
            }
            else {
                if (lead_list && $("#campaign-group-tab").hasClass("active") || $("#campaign-settings-tab").hasClass("active")) {
                    empty_lead = false
                }
                else {
                    empty_lead = true
                    return false
                }
            }
        }
        else {
            valid =false
            return dispositionAlert(lead_name)

        }
    })
    required_dispo = true
    if ($(".selected-disposition .badge-pill").length == 0){
     required_dispo =false
     $("#dispo-err-msg").removeClass("d-none")
    }
    else {
     $("#dispo-err-msg").addClass("d-none")
    }
    $("#lead_recycle_dict").val(JSON.stringify(lead_recycle_dict))
    return [dial_method_flag, valid, empty_lead, incomplete_lead, required_dispo]
}
$(".create-campaign-btn").click(function() {
    $("#campaign-create-form").isValid()
    response_data = campaign_pre_save_validation('#campaign-create-form')
    dial_method_flag = response_data[0]
    valid = response_data[1]
    var existing_campaign = $("#existing_camp_data").val()
    var trunk_list = add_trunk_vue.group_trunk_list[0]
    if(trunk_list["did_type"] == "single") {
        var did_val = [trunk_list["did"]]
        trunk_list["did"] = did_val
    }
    $("#trunk_did_data").val(JSON.stringify(trunk_list))
    if ($("#feedback-time").val() == "None") {
        $("#feedback-time").val("")
    }
    if (existing_campaign != "") {
        $("#existing_campaign").val(existing_campaign)
    }
    if (incomplete_lead == true) {
        $(".campaign-err-msg").text("Incomplet Lead Data").removeClass("d-none")
        setTimeout(function() {
            $(".campaign-err-msg").addClass("d-none")
        }, 3000);
        incomplete_lead = false
    } else if ($("#campaign-create-form").isValid() == true && dial_method_flag && valid  && required_dispo) {
        $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/CampaignManagement/Campaign/create/',
            data: $('#campaign-create-form').serialize(),
            success: function(data) {
                showSwal('success-message', 'Campaign Created Successfully', '/CampaignManagement/Campaigns/')
            },
            error: function(data) {
                if (data["responseJSON"]["camp_name_error"]){
                    $("#camp_name_exist").html(`<span class="help-block form-error">${data["responseJSON"]["camp_name_error"]}</span>`).addClass("has-error")
                    $("#campaign-name").removeClass("valid").addClass("error")                  
                }
                if (data["responseJSON"]["camp_callerid_error"]){
                    $("#camp_callerid_exist").html(`<span class="help-block form-error">${data["responseJSON"]["camp_callerid_error"]}</span>`).addClass("has-error")
                    $("#caller_id").removeClass("valid").addClass("error")                  
                }
                if (data["responseJSON"]["errors"]) {
                    $(".campaign-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
                    setTimeout(function() {
                        $(".campaign-err-msg").addClass("d-none")
                    }, 3000);
                }
            }
        });
    }
})


$("#feedback-time").datetimepicker({
    format: 'HH:mm',
    pickerPosition: 'top-right'
});

function reset_campaign() {
    var de_move_group = $("#profile-list-right").find('div')
    $("#profile-list-left").append(de_move_group)

    var de_move_dispos = $('#disposition-list-right').find('div')
    $('#disposition-list-left').append(de_move_dispos)

    var de_move_break = $("#agent-breaks-right").find('div')
    $("#agent-breaks-left").append(de_move_break)

    var de_move_relation = $("#relationtag-list-right").find('div')
    $("#relationtag-list-left").append(de_move_relation)

    $("#web_url").val("")
    $("#transfer_call").prop("checked", false)
    $("#conference").prop("checked", false)
    $("#users").val("").trigger('change');
    $("#schedule").val("")
    $("#status").val("")
    $("#description").text("")
    $("#que_call_count").prop("checked", false)
    $('*[name="callback_mode"]').attr("checked", false)
    $('*[value="self"]').attr("checked", "checked")
    $("#portifolio").prop("checked", false)
    $('*[name="dnc"]').attr("checked", false)
    $('*[value="local"]').attr("checked", "checked")
}


$(document).on('change', '#existing_camp_data', function() {
    reset_campaign()
    if ($(this).val()) {
        var camp_id = $(this).val()
        $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/api/fetch-existing-data/',
            data: {
                "instance_id": camp_id,
                "app_label": "callcenter",
                "model_name": "Campaign",
                "serializer": "ReadOnlyCampaignSerializer"
            },
            success: function(data) {
                var campaign_data = data["instance_info"]
                $("#agent-breaks-right div, .selected-groups div").remove()
                $.each(campaign_data['group'], function(index, value) {
                    var move_group = $("#profile-list-left").find('*[data-id="' + value["id"] + '"]')
                    $("#profile-list-right").append(move_group)
                });
                $.each(campaign_data['breaks'], function(index, value) {
                    var move_break = $("#agent-breaks-left").find('*[data-id="' + value["id"] + '"]')
                    $("#agent-breaks-right").append(move_break)
                });
                $.each(campaign_data['disposition'], function(index, value) {
                    var move_dispos = $('#disposition-list-left').find('*[data-id="' + value + '"]')
                    $('#disposition-list-right').append(move_dispos)
                })
                $.each(campaign_data['relation_tag'], function(index, value) {
                    var move_relationtag = $('#relationtag-list-left').find('*[data-id="' + value + '"]')
                    $('#relationtag-list-right').append(move_relationtag)
                })
                $("#web_url").val(campaign_data['weburl'])
                if (campaign_data['transfer'] == 'True') {
                    $("#transfer_call").prop("checked", true)
                } else {
                    $("#transfer_call").prop("checked", false)
                }
                if(campaign_data['auto_feedback'] == false){
                    $('#feedback-time').val('')
                }
                $("#transfer_call").val(campaign_data['transfer']).trigger('change');
                $("#conference").prop("checked", campaign_data["conference"])
                $("#que_call_count").prop("checked", campaign_data["show_queue_call_count"])
                $("#prefix").val(campaign_data["prefix"])
                $('*[value="' + campaign_data["callback_mode"] + '"]').attr("checked", "checked")
                $("#portifolio").prop("checked", campaign_data["portifolio"])
                if (campaign_data["dnc"] == "global") {
                    $('*[name="dnc"').attr("checked", false)
                    $('*[value="' + campaign_data["dnc"] + '"]').attr("checked", "checked")
                }
                $("#users").val(campaign_data['users']).trigger('change');
                $("#schedule").val(campaign_data["schedule"])
                $("#status").val(campaign_data["status"])
                $("#description").text(campaign_data["description"])


            },
            error: function(data) {
                if (data["responseJSON"]["errors"]) {
                    $(".user-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
                    setTimeout(function() {
                        $(".user-err-msg").addClass("d-none")
                    }, 3000);
                }
            }
        });
    }
})

$
$("#campaign_template").change(function() {
    if ($(this).val() == "default") {
        reset_campaign()
        $("#campaign-all-fields, #show-campaign").addClass("d-none")
        $("#campaign-show_all_fields").prop("checked", false)
    } else if ($(this).val() == "existing_campaign") {
        $("#existing_camp_data").val("").trigger("change")
        $("#show-campaign").removeClass("d-none")
    }
})
$(document).on('change', '#campaign-show_all_fields', function() {
    $("#campaign-all-fields").toggleClass("d-none")
})
$("#campaign-name").keyup(function() {
    var current_val = $(this).val()
    $(this).val(current_val.trim())
    $("#campaign-slug").val($(this).val().trim())
})
$('#campaign_inbound').on('change', function() {
    form_data = {
        'inbound_checked': $(this).val(),
        'campaign': $('#campaign-name').val()
    }
    if (!$(this).is(":checked")) {
        $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/api/checkskilled/',
            data: form_data,
            success: function(data) {
                if (data['error']) {
                    $("#skill-check-err-msg").text(data['error']).removeClass("d-none")
                    setTimeout(function() {
                        $("#skill-check-err-msg").addClass("d-none")
                    }, 3000);
                    if($('#ibc_popup').prop('checked') == false && $("#camp_outbound option:selected").val() == 'Progressive'){
                        $("#camp_outbound option[value='Progressive']").hide();
                        $("#camp_outbound option[value='Preview']").hide();
                        $("#camp_outbound option[value='Predictive']").prop('selected',true)
                        $("#progressive_time_div").addClass("d-none")
                    }else if($('#ibc_popup').prop('checked') == false && $("#camp_outbound option:selected").val() == 'Preview'){
                        $("#camp_outbound option[value='Progressive']").hide();
                        $("#camp_outbound option[value='Preview']").hide();
                        $("#camp_outbound option[value='Predictive']").prop('selected',true)
                    }
                    $('#campaign_inbound').prop('checked', true)
                    $('#ibc_div, #sticky_agent_map_div, #inbound_threshold_div').removeClass('d-none')
                }
            },
        })
    }
})
$(".edit-campaign-btn, #edit-campaign-settings-btn").click(function() {
    $("#campaign-edit-form").isValid()
    response_data = campaign_pre_save_validation("#campaign-edit-form")
    dial_method_flag = response_data[0]
    var valid = response_data[1]
    var empty_lead = response_data[2]
    if ($("#feedback-time").val() == "None") {
        $("#feedback-time").val("")
    }
    var trunk_list = add_trunk_vue.group_trunk_list[0]
    if (trunk_list) {
        if(trunk_list["did_type"] == "single") {
            var did_val = [trunk_list["did"]]
            trunk_list["did"] = did_val
        }
        $("#trunk_did_data").val(JSON.stringify(trunk_list))
    }
    if (empty_lead) {
        $("#lead-err-msg").text("Select lead name").removeClass("d-none")
        setTimeout(function() {
            $("#lead-err-msg").addClass("d-none")
        }, 3000);
    } else if (incomplete_lead == true) {
        $("#lead-err-msg").text("Incomplet Lead Data").removeClass("d-none")
        setTimeout(function() {
            $("#lead-err-msg").addClass("d-none")
        }, 3000);
        incomplete_lead = false
    } else {
        if ($("#campaign-edit-form").isValid() == true && dial_method_flag && valid && required_dispo) {
            $.ajax({
                type: 'put',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/CampaignManagement/Campaign/' + campaign_id + '/',
                data: $('#campaign-edit-form').serialize(),
                success: function(data) {
                    showSwal('success-message', 'Campaign Updated Successfully', "/CampaignManagement/Campaigns/")
                },
                error: function(data) {
                    if (data["responseJSON"]["camp_name_error"]){
                        $("#camp_name_exist").html(`<span class="help-block form-error">${data["responseJSON"]["camp_name_error"]}</span>`).addClass("has-error")
                        $("#campaign-name").removeClass("valid").addClass("error")                  
                    }
                    if (data["responseJSON"]["camp_callerid_error"]){
                        $("#camp_callerid_exist").html(`<span class="help-block form-error">${data["responseJSON"]["camp_callerid_error"]}</span>`).addClass("has-error")
                        $("#caller_id").removeClass("valid").addClass("error")                  
                    }
                    if (data["responseJSON"]["errors"]) {
                        $("#campaign-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
                        setTimeout(function() {
                            $("#campaign-err-msg").addClass("d-none")
                        }, 3000);
                    }
                }
            });
        }
    }
})
$(document).on('change', '.lead_name', function(e) {
    if ($(".lead_name option:selected[value='" + $(this).val() + "']").length > 1) {
        $(this).val("Select Disposition")
    }
    var current_element = $(this).attr("id").split("-")[1]
    if ($(this).val() != "Select Disposition") {
        $("#lead-heading-" + current_element).find('a').text($(this).val().toUpperCase())
    } else {
        $("#lead-heading-" + current_element).find('a').text("Lead Recycle")
    }
})

// This block of functions are realted to calltimes

        
$("#create-calltime-btn").click(function() {
    var weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    calltimes_form_data = {}
    stop_ajax = false
    $.each(weekdays, function( index, value ) {
        start_time = $("#"+value+"-start-timepicker input").val();
        stop_time  = $("#"+value+"-stop-timepicker input").val();
        audio_file_name = $("#"+value+"_audio_file").val();
        
        if(start_time != '' && stop_time == ''){
            $('#'+value+'_stop_err_msg').html("This fieldis required").removeClass("d-none");
            setTimeout(function(){ 
                $('#'+value+'_stop_err_msg').addClass('d-none')
            }, 3000);
            stop_ajax = true
            return false            
        }else if(start_time=='' && stop_time !=''){
            $('#'+value+'_start_err_msg').html("Start time is need...").removeClass('d-none');
            setTimeout(function(){ 
                $('#'+value+'_start_err_msg').addClass('d-none')
            }, 3000);
            stop_ajax = true
            return false
        }
        timings = {}
        timings['start_time'] = start_time
        timings['stop_time'] = stop_time
        timings['audio_file_name'] = audio_file_name
        calltimes_form_data[value] = timings
        if (start_time != '' && stop_time != ''){
            if(start_time == stop_time){
                $('#'+value+'_stop_err_msg').html("StartTime and EndTime should not be same...").removeClass("d-none");
                setTimeout(function(){ 
                    $('#'+value+'_stop_err_msg').addClass('d-none')
                }, 3000);
                stop_ajax = true
                return false
            }   
        }   
        // else if(audio_file_name !='' && start_time == '' && stop_time == ''){
        //  $('#'+value+'_audio_err_msg').html("Start & End time is need...").removeClass('d-none');
        //  setTimeout(function(){ 
        //      $('#'+value+'_audio_err_msg').addClass('d-none')
        //  }, 3000);
        //  stop_ajax = true
        //  return false
        // }
    });
    
    if (stop_ajax == false) {
        calltimes_form_data = JSON.stringify(calltimes_form_data)
        $('#schedule_time').val(calltimes_form_data);
        var pk = $('#calltime_id').val()
        if (pk) {
            type = "put"
            url = '/CampaignManagement/CampaignSchedule/' + pk + '/'
        } else {
            type = 'post'
            url = '/CampaignManagement/CampaignSchedule/create/'
        }
        if ($("#calltime-create-form").isValid() == true) {
            $.ajax({
                type: type,
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: url,
                data: $('#calltime-create-form').serialize(),
                success: function(data) {
                    if ("msg" in data) {
                        $("#calltime-err-msg").text(data["msg"]).removeClass("d-none")
                        setTimeout(function() {
                            $("#calltime-err-msg").addClass("d-none")
                        }, 3000);
                    } else {
                        showSwal('success-message', data["success"], "/CampaignManagement/CampaignSchedule/")
                    }
                },
                error: function(data) {
                    $("#calltime-name").removeClass("valid").addClass("error")
                    $("#calltime-name-error").removeClass("has-success").addClass("has-error")
                    $("#calltime-name-error").html("<span class='help-block form-error'>" + data["responseJSON"]["name"] + "</span>")
                        // $("#calltime-name-error").text(data["responseJSON"]["errors"]["name"])
                }
            });
        }
    }
})

$(document).on('change', '#existing_campschedule_data', function() {
    var camp_id = $(this).val()
    $.ajax({
        type: 'post',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/api/fetch-existing-data/',
        data: {
            "instance_id": camp_id,
            "app_label": "callcenter",
            "model_name": "CampaignSchedule",
            "serializer": "CampaignScheduleSerializer"
        },
        success: function(data) {
            var schedule = JSON.parse(data["instance_info"]["schedule"])
            var schedule_days = data["instance_info"]["schedule_days"]
            campaign_schedule_vue.campaign_schedule = schedule
            campaign_schedule_vue.schedule_days = schedule_days
            if (schedule_days === 'all_days' || schedule_days == 'mon_to_fri') {
                campaign_schedule_vue.all_audio_file = schedule['Monday']['audio_file_name']
                campaign_schedule_vue.all_start_time = schedule['Monday']['start_time']
                campaign_schedule_vue.all_stop_time = schedule['Monday']['stop_time']
            }
        },
        error: function(data) {

        }
    });
})

//calltimes functions ends here ........ 


// This function is used to edit user section
$("#edit-user-btn, #edit-user-settings-btn").click(function() {
    var current_user = $(this)
    if($("#caller_id").val() != "") {
        $("#caller_id").attr("data-validation", "length")
    }
    if ($("#email").val() != "") {
        $("#email").attr("data-validation", "email")
    }
    if ($("#user-edit-form").isValid() == true ) {
        $.ajax({
            type: 'put',
            headers: {"X-CSRFToken": csrf_token},
            url: '/UserManagement/Users/'+user_id+'/',
            data: $('#user-edit-form').serialize(),
            beforeSend: function() {
                $('.preloader').fadeIn('fast');
            },
            success: function (data) {
                $('.preloader').fadeOut('fast');
                showSwal('success-message', 'User Updated Successfully', '/UserManagement/Users/')
            },
            error: function (data) {
                $('.preloader').fadeOut('fast');
                if (data["responseJSON"]["email_id"]){
                    $("#email-error").html(`<span class="help-block form-error">${data["responseJSON"]["email_id"]}</span>`).addClass("has-error")
                    $("#email").removeClass("valid").addClass("error")                  
                }
                if (data["responseJSON"]["caller_id"]){
                    $("#callerid-error").html(`<span class="help-block form-error">${data["responseJSON"]["caller_id"]}</span>`).addClass("has-error")
                    $("#caller_id").removeClass("valid").addClass("error")
                }
                if (data["responseJSON"]["extension"]){
                    $("#extension-error").html(`<span class="help-block form-error">${data["responseJSON"]["extension"]}</span>`).addClass("has-error")
                    $("#extension").removeClass("valid").addClass("error")
                }
                if (data["responseJSON"]["username"]) {
                    $("#user-name-error").html(`<span class="help-block form-error">${data["responseJSON"]["username"]}</span>`).addClass('has-error')
                    $("#username").removeClass("valid").addClass("error")
                }
                 if (data["responseJSON"]["wfh_numeric"]) {
                    $("#wfh_numeric-error").html(`<span class="help-block form-error">${data["responseJSON"]["wfh_numeric"]}</span>`).addClass('has-error')
                    $("#wfh_numeric").removeClass("valid").addClass("error")
                }
                if (data["responseJSON"]["errors"]["employee_id"]) {
                    $("#employee_id-error").html(`<span class="help-block form-error">${data["responseJSON"]["errors"]["employee_id"]}</span>`).addClass('has-error')
                    $("#employee_id").removeClass("valid").addClass("error")
                }
                if (data["responseJSON"]["errors"] && !('employee_id' in data["responseJSON"]["errors"]) ) {
                    if (current_user.hasClass("edit-user")) {
                        $("#user-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
                        setTimeout(function(){ $("#user-err-msg").addClass("d-none") }, 3000);
                    }
                    else {
                        $("#user-settings-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
                        setTimeout(function(){ $("#user-settings-err-msg").addClass("d-none") }, 3000); 
                    }
                }
            }
        });
    }   
})
// This function is used to edit phone

$("#edit-phone-btn").click(function() {
    var current_user = $(this)
    if ($("#phone-edit-form").isValid() == true) {
        $.ajax({
            type: 'put',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/UserManagement/edit-phone/' + phone_id + '/',
            data: $('#phone-edit-form').serialize(),
            success: function(data) {
                showSwal('success-message', 'Phone Updated Successfully', '/UserManagement/Users/')
            },
            error: function(data) {
                if (data["responseJSON"]["errors"]) {
                    $("#phone-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
                    setTimeout(function() {
                        $("#phone-err-msg").addClass("d-none")
                    }, 3000);
                }
            }
        });
    }
})

var audio_form = $("#audio-upload-form");
audio_form.children("div").steps({
    headerTag: "h2",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        if ($('#audio-upload-form').hasClass("edit-audio")) {
            var current_id = $("#audio-id").val()
            url = '/CampaignManagement/edit-audio/' + current_id + '/'
        } else {
            url = '/CampaignManagement/upload-audio-file/'
        }
        var formData = new FormData($("#audio-upload-form")[0]);
        var valid = true
        var fileExtension = ['MP3', 'mp3', 'OGG', 'ogg'];
        if ($(".dropify-filename-inner").text() != "") {
            if ($.inArray($(".dropify-filename-inner").text().split('.').pop().toLowerCase(), fileExtension) == -1) {
                $("#file-extension-msg").removeClass("d-none").text("File formats must be mp3, ogg")
                setTimeout(function() {
                    $("#file-extension-msg").addClass("d-none")
                }, 3000);
                valid = false
            } else if ($('#uploaded-audio-file')[0].files[0].size > 2097152) {
                $("#file-extension-msg").removeClass("d-none").text("File Size must be less than, 2Mb")
                setTimeout(function() {
                    $("#file-extension-msg").addClass("d-none")
                }, 3000);
                valid = false
            }
        }
        if ($("#audio-upload-form").isValid() == true && valid == true) {
            $.ajax({
                url: url,
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                beforeSend: function() {
                    $('.preloader').fadeIn('fast');
                },
                success: function(data) {
                    $('.preloader').fadeOut('fast');
                    showSwal('success-message', 'Audio File Uploaded Successfully')
                },
                error: function(data) {
                     $('.preloader').fadeOut('fast');
                    if (data["responseJSON"]["name"]) {
                        $("#name-error").addClass("has-error").html(
                            '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>')
                        setTimeout(function() {
                            $("#name-error").addClass("d-none")
                        }, 3000);
                    }
                }

            });
        }
    }
});
// This function is used to save audio files
// $("#create-audio-file, .edit-audio").click(function() {
// if($(this).hasClass("edit-udio")) {
//  var current_id = $("#audio-id").val()
//  url = '/CampaignManagement/edit-audio/'+current_id+'/'
// }
// else {
//  url = '/CampaignManagement/upload-audio-file/'
// }
// var formData = new FormData($("#audio-upload-form")[0]);
// var valid = true
// var fileExtension = ['MP3', 'mp3', 'OGG', 'ogg'];
// if ($(".dropify-filename-inner").text() != "") {
//  if ($.inArray($(".dropify-filename-inner").text().split('.').pop().toLowerCase(), fileExtension) == -1) {
//      $("#file-extension-msg").removeClass("d-none").text("File formats must be mp3, ogg")
//      setTimeout(function(){ $("#file-extension-msg").addClass("d-none") }, 3000);
//      valid = false
//  }
// }
// if ($("#audio-upload-form").isValid() == true && valid == true ) {
//  $.ajax({
//      url : url,
//      type : 'POST',
//      data : formData,
//      processData: false, 
//      contentType: false,
//      success : function(data) {
//          showSwal('success-message', 'Audio File Uploaded Successfully')
//      },
//      error: function (data) {
//          if (data["responseJSON"]["name"]) {
//              $("#name-error").addClass("has-error").html(
//                  '<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>')
//              setTimeout(function(){ $("#name-error").addClass("d-none") }, 3000);
//          }
//      }

//  });
// }
// })
$(document).on('click', '.modify-audio-file', function() {
    $(".dtr-bs-modal").modal('hide');
    var current_id = $(this).attr("id").split("-")[2]
    $.ajax({
        type: 'GET',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/CampaignManagement/edit-audio/' + current_id + '/',
        data: {},
        success: function(data) {
            $("#audio_name").val(data["name"])
            $("#description").val(data["description"])
            $("#status").val(data["status"])
            if ("audio_file" in data && data["audio_file"]) {
                audio_file_path = data["audio_file"]
                audio_file_name = data["audio_file"].split("upload/")[1]
                $("#uploaded_file a").text(audio_file_name).attr(
                    "href", audio_file_path)
                $("#uploaded_file").removeClass("d-none")

            }
            $("#audio-id").val(current_id)
            $("#audio-upload-form").addClass("edit-audio")
            $("#audio-wizard-modal").modal('show');
        },
        error: function(data) {
            if (data["responseJSON"]["name"]) {
                $("#name-error").addClass("has-error").html(
                    '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass(
                    "d-none")
                setTimeout(function() {
                    $("#name-error").addClass("d-none")
                }, 3000);
            }
        }
    });

})
$("#audio-wizard-modal").on('hidden.bs.modal', function() {
    $("#audio-upload-form")[0].reset();
    $(".dropify-clear").click()
});

$("#fileupload-wizard-modal").on('hidden.bs.modal', function() {
    $("#user-upload-form")[0].reset();
    $(".dropify-clear").click()
    $("#improper-data, #proper-data, .confirm-user-upload, .cancel-uploaded-file").addClass("d-none")
});


$("#templateupload-wizard-modal").on('hidden.bs.modal', function() {
    $("#sms-template-upload-form")[0].reset();
    $(".dropify-clear").click()
    $("#improper-data, #proper-data, .confirm-user-upload, .cancel-uploaded-file").addClass("d-none")
    if(can_reload) {
         location.reload();
    }
});

$("#dncfileupload-wizard-modal").on('hidden.bs.modal', function() {
    $("#dnc-upload-form")[0].reset();
    $(".dropify-clear").click()
    $("#improper-data, #proper-data, .confirm-dnc-upload, .cancel-dnc-uploaded-file").addClass("d-none")
});

$("#audio-wizard-modal").on('hidden.bs.modal', function() {
    $("#audio-upload-form")[0].reset();
    $("#uploaded_file").addClass("d-none")
    $(".dropify-clear").click()
});
// script block starts here
$("#script-submit-btn").click(function() {
    var script_data = tinyMCE.get('scriptEditor').getContent();
    $("#script-data").val(script_data)
    var script_form = $("#script-create-form")
    if (script_form.isValid() == true ) {
        $.ajax({
            type: 'POST',
            headers: {"X-CSRFToken": csrf_token},
            url: '/CampaignManagement/Script/create/',
            data: script_form.serialize(),
            success: function (data) {
                if ($("#script_id").val() != "") {
                    showSwal('success-message', 'Script Successfully Updated', '/CampaignManagement/Scripts')
                }
                else {
                    showSwal('success-message', 'Script Successfully Created', '/CampaignManagement/Scripts')
                }
            },
            error: function (data) {
                if (data["responseJSON"]["name"]){
                    $("#script-name-error").html(`<span class="help-block form-error">${data["responseJSON"]["name"]}</span>`).addClass("has-error")
                    $("#name").removeClass("valid").addClass("error")
                }
                if ("name" in data["responseJSON"]) {
                    $("#script-name-error").addClass("has-error").removeClass("d-none").html(
                        '<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>')
                    setTimeout(function(){ $("#script-name-error").addClass("d-none") }, 3000);
                }
                
            }
        });
    }
})
// script block

// this function to create crm field by csv file upload

$(document).on("click", "input[name='crmField_file']", function() {
    $(this).change()
})

$(document).on("change", "input[name='crmField_file']", function() {
    $(".wizard li a[href='#finish']").text("Validate")
    $("#proper-data, .improper_data_div").addClass("d-none")
    $(".wizard li a[href='#previous']").addClass("d-none")

})
$(document).on('select2:select', '#crm_field_campaign', function(e) {
    var campaign = e.params.data["text"]
    var crm_name = $("input[name='name']").val()
    $.ajax({
        type: 'POST',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: "/CRM/check-campaign-avail/",
        data: {
            "campaign": campaign,
            "crm_name": crm_name
        },
        success: function(data) {
            if ("camp_exist" in data) {
                $("#campaign_error").removeClass("d-none")
                $("#campaign_error").text(data["camp_exist"]).addClass("text-danger")
                setTimeout(function() {
                    $("#crm_field_campaign option[value='" + campaign + "']").prop('selected', false).trigger("change")
                    $("#campaign_error").addClass("d-none")
                }, 3000);
            }
        },
        error: function(data) {}
    });
})
var crmField_upload_form = $('#crmField_upload_form')
crmField_upload_form.children("div").steps({
    headerTag: "h2",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        var current_element = $(this)
        if ($(".dropify-preview").css('display') != 'none') {
            if ($(".wizard li a[href='#finish']").text() == "Submit") {
                data = {}
                var proper_file = $("#proper-data").attr("href")
                var improper_file = $("#improper-data").attr("href")
                data["proper_file"] = proper_file
                data["improper_file"] = improper_file
                data["name"] = $("#crmField_name").val()
                data["campaign"] = $("#crm_field_campaign").val()
                data["perform_upload"] = true
                $.ajax({
                    type: 'post',
                    headers: {
                        "X-CSRFToken": csrf_token
                    },
                    url: '/CRM/upload-crm-field/',
                    data: data,
                    beforeSend: function() {
                        $('.preloader').fadeIn('fast');
                    },
                    success: function(data) {
                        $('.preloader').fadeOut('fast');
                        showSwal('success-message', 'Crm Uploaded Successfully')
                        $(".dropify-clear").click()
                        $("#proper-data, #improper-data, #confirm-upload-file, #cancel-uploaded-file").addClass("d-none")
                        $(".wizard li a[href='#finish']").text("Validate")
                    },
                    error: function(data) {
                        $('.preloader').fadeOut('fast');
                        if (data["responseJSON"]["name"]) {
                            $("#crm-error-msg").addClass("has-error").html(
                                '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass("d-none")
                            setTimeout(function() {
                                $("#crm-error-msg").addClass("d-none")
                            }, 3000);
                        }
                    }
                });
            } else {
                var formData = new FormData($("#crmField_upload_form")[0]);
                var valid = true
                var fileExtension = ['csv', 'xls', 'xlsx'];
                if ($(".dropify-filename-inner").text() != "") {
                    if ($.inArray($(".dropify-filename-inner").text().split('.').pop().toLowerCase(), fileExtension) == -1) {
                        $("#upload-file-error").text("File format must be csv").removeClass("d-none")
                        setTimeout(function() {
                            $("#upload-file-error").addClass("d-none")
                        }, 3000);
                    } else if (crmField_upload_form.isValid()) {
                        $.ajax({
                            type: 'POST',
                            headers: {
                                "X-CSRFToken": csrf_token
                            },
                            // url: '/CRM/upload-crm-field/',
                            url: '/CRM/validate-crm-field/',
                            data: formData,
                            cache: false,
                            processData: false,
                            contentType: false,
                            beforeSend: function() {
                                $('.preloader').fadeIn('fast');
                            },
                            success: function(data) {
                                $('.preloader').fadeOut('fast');
                                $(".wizard li a[href='#previous']").removeClass("d-none")
                                if ("column_err_msg" in data) {
                                    $('#empty-data').removeClass('d-none').html(data["column_err_msg"])
                                    setTimeout(function() {
                                        $("#empty-data").addClass("d-none")
                                    }, 3000);
                                } else {
                                    if ("correct_file" in data) {
                                        $("#proper-data").attr("href", data["correct_file"]).removeClass("d-none")
                                        $(".wizard li a[href='#finish']").text('Submit')
                                        $("#proper-data span.msg").text("Proper Data: " + data["correct_count"])
                                        $(".proper_data_div").removeClass("d-none")
                                    } else {
                                        $('#empty-data').removeClass('d-none')
                                        setTimeout(function() {
                                            $("#empty-data").addClass("d-none")
                                        }, 3000);
                                    }
                                    if ("incorrect_file" in data) {
                                        $(".improper_data_div").removeClass("d-none")
                                        $("#improper-data").attr("href", data["incorrect_file"]).removeClass("d-none")
                                        $("#improper-data span.msg").text("Improper Data: " + data["incorrect_count"])
                                        $('#empty-data').addClass('d-none')
                                    }
                                }
                            },
                            error: function(data) {
                                 $('.preloader').fadeOut('fast');
                                $("#upload-file-error").text(data["responseJSON"]["error"]).removeClass("d-none")
                                setTimeout(function() {
                                    $("#upload-file-error").addClass("d-none")
                                }, 3000);
                            }
                        });

                    }
                } else {
                    $("#upload-file-error").text("Please, select proper file to upload").removeClass("d-none")
                    setTimeout(function() {
                        $("#upload-file-error").addClass("d-none")
                    }, 3000);
                }
            }
        } else {
            $("#upload-file-error").text("Please, select file to upload").removeClass("d-none")
            setTimeout(function() {
                $("#upload-file-error").addClass("d-none")
            }, 3000);
        }

    }
})

$(crmField_upload_form).find("a[href='#previous']").click(function() {

    data = {}
    var proper_file = $("#proper-data").attr("href")
    var improper_file = $("#improper-data").attr("href")
    data["proper_file"] = proper_file
    data["improper_file"] = improper_file
    $.ajax({
        type: 'post',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/CRM/upload-crm-field/',
        data: data,
        success: function(data) {
            showSwal('success-message', 'Crm Upload Operation Cancelled')
            $(".dropify-clear").click()
            $("#proper-data, #improper-data, #confirm-upload-file, #cancel-uploaded-file").addClass("d-none")
            $(".wizard li a[href='#finish']").text("Validate")
        },
        error: function(data) {}
    });

})
$('#crmField_upload_modal').on('hidden.bs.modal', function() {
    $("#crmField_upload_form").trigger("reset");
    $("#crm_field_campaign").select2();
    $(".dropify-clear").click()
})


// This function is used to perform delete operation for all activities
function perform_delete(delete_type) {
    data = {}
    data["perform_operation"] = delete_type
    if (delete_highp == true) {
        data["select_all"] = true
    } else if (delete_type.indexOf("particular_entry") != -1) {
        if (delete_type.split("-")[2] == undefined){
            data["perform_operation"] = "delete"
        }
        else {
         data["perform_operation"] = delete_type.split("-")[2]   
        }
        var id = delete_type.split("-")[1]
        result = []
        result.push(id)
    }
    data["model_name"] = $("#model_name").val()
    data["app_name"] = $("#app_name").val()
    data["selected_entry"] = JSON.stringify(result)
    temp_operation = data["perform_operation"]
    if ($.inArray( data["model_name"], ["Campaign", "PauseBreak", "Disposition", "DialTrunk", "DiaTrunkGroup", "User", "Group", "Switch", "Phonebook"] ) != -1  && $.inArray( data["perform_operation"], ["Make InActive", "delete"] ) != -1) {
        $.ajax({
            type: 'POST',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/api/check-selected-entry/',
            data: data,
            success: function(response_data) {
                if (response_data["selected_entries"].length > 0){
                    data["selected_entry"] = JSON.stringify(response_data["selected_entries"])
                    $.ajax({
                        type: 'POST',
                        headers: {
                            "X-CSRFToken": csrf_token
                        },
                        url: '/api/delete-selected-entry/',
                        data: data,
                        success: function(data) {
                            $('.preloader').fadeOut('fast');
                            if (temp_operation == "Make Active") {
                                showSwal('success-message', 'Selected Entries Are Activated')
                            } else if (temp_operation == "Make InActive") {
                                showSwal('success-message', 'Selected Entries Are Inactivated')
                            } else {
                                showSwal('success-message', 'Selected Entries Are Deleted')
                            }
                        },
                        error: function(data) {
                            $('.preloader').fadeOut('fast');
                        }
                    });
                } else {
                    errorAlert('Operation Restricted', 'Agents are logged in with this ' + data["model_name"] + ', You can not perform delete or inactive operation')
                    $('.preloader').fadeOut('fast');
                    result = []
                }
            },
            error: function(data) {
                $('.preloader').fadeOut('fast');
            }
        });
    }
    else {
        $.ajax({
            type: 'POST',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/api/delete-selected-entry/',
            data: data,
            success: function(data) {
                $('.preloader').fadeOut('fast');
                if (temp_operation == "Make Active") {
                    showSwal('success-message', 'Selected Entries Are Activated')
                } else if (temp_operation == "Make InActive") {
                    showSwal('success-message', 'Selected Entries Are Inactivated')
                } else {
                    showSwal('success-message', 'Selected Entries Are Deleted')
                }
            },
            error: function(data) {
                $('.preloader').fadeOut('fast');
            }
        });

    }

}
// ends delete block

// This function is used to perform delete operation for all activities
function perform_download_action(action, id) {
    data = {}
    data["perform_operation"] = action  
    data["model_name"] = $("#model_name").val()
    data["app_name"] = $("#app_name").val()
    data["selected_entry"] = id
    $.ajax({
        type: 'POST',
        headers: {"X-CSRFToken": csrf_token},
        url: '/api/perform-action-on-entry/',
        data: data,
        success: function (data) {
            showSwal('success-message', data.msg)
        },
        error: function (data) {
            
        }
    });
}
// ends delete block

function phonebook_download(action, id) {
    data = {}
    data["selected_entry"] = id
    $.ajax({
        type: 'POST',
        headers: {"X-CSRFToken": csrf_token},
        url: '/api/download-phonebook/',
        data: data,
        success: function (data) {
            is_download=true
            showSwal('success-message', data.message)
        },
        error: function (data) {
            errorAlert('No Data Available', data.responseJSON.error)
        }
    });
}

// check entered value is number only starts
function isNumber(evt) {
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
    return true;
}
// check entered value is number only ends

// check paste value is number
function pasteNumber(event) {
    if (event.clipboardData.getData('text').match(/[^\d]/)) {
        event.preventDefault()
    }
}

// to checked read permission if other permission are checked in user role
$(document).on('click', '.permission_input', function() {
    if ($(this).prop("checked")) {
        $(this).closest("div").siblings().find("#R").prop("checked", true)
    } else {
        if ($(this).prop("id") == "R") {
            $(this).closest("div").siblings().find("#C,#U,#D").prop("checked", false)
        }
    }
});
//select all the permissions at once 

$(document).on('click','#select_all_permissions',function(){
    if($(this).prop("checked")){    
        $('.permission_input').closest("div").find("#R,#C,#U,#D").prop("checked",true)
    }else{
        $('.permission_input').closest("div").find("#R,#C,#U,#D").prop("checked",false)
    }
})

$("#additional_settings").change(function() {
    if ($(this).val() == 'custom') {
        $("#select_range_div").removeClass("d-none")
    } else {
        $("#select_range_div").addClass("d-none")
        $("#custom-range").val("")
    }
})
$.fn.select2.amd.require(['select2/selection/search'], function(Search) {
    var oldRemoveChoice = Search.prototype.searchRemoveChoice;

    Search.prototype.searchRemoveChoice = function() {
        oldRemoveChoice.apply(this, arguments);
        this.$search.val('');
    };
    $('#users, #phone_extensions, #call_mode, #user-group, #group, #user_timezone, .select2-class, #add_users, #contact_phonebook_select, #contact_campaign_select, #update_user_in_group, #crm_field_campaign, #avail_users, #update_crm_fields').select2();
});
$("#modal_add_group, #modal_update_group").on('hidden.bs.modal', function() {
    $("form")[0].reset();
});
$(document).on('change', '#schedule_type', function() {
    var parent = $(this).attr("data-parent")
    if ($(this).val() == "schedule_time") {
        $("#lead-card-" + parent).find("#lead-start-time, #lead-end-time").removeClass("d-none")
        $("#lead-card-" + parent).find("#lead-end-time input").attr("disabled", "disabled")
        $("#lead-card-" + parent).find("#lead-time-div").addClass("d-none").val("0")
        $("#lead-card-" + parent).find("#lead_time").val("0")

    } else if ($(this).val() == "recycle_time") {
        $("#lead-card-" + parent).find("#lead-end-time input").val("")
        $("#lead-card-" + parent).find("#lead-start-time input").val("")
        $("#lead-card-" + parent).find("#lead-start-time, #lead-end-time").addClass("d-none")
        $("#lead-card-" + parent).find("#lr_start_time, #lr_end_time").val("")
        $("#lead-card-" + parent).find("#lead-time-div").removeClass("d-none")
        $("#lead-card-" + parent).find("#lead_time").val("0")
    } else {
        $("#lead-card-" + parent).find("#lead-start-time, #lead-end-time, #lead-time-div").addClass("d-none")
        $("#lead-card-" + parent).find("#lr_start_time, #lr_end_time").val("")
        $("#lead-card-" + parent).find("#lead_time").val("0")
    }
})

function calculateInterval(parent_id) {
    var formatted_interval = 0
    var start_time = $("#lead-card-" + parent_id).find("#lr_start_time").val()
    if (start_time) {
        var end_time = $("#lead-card-" + parent_id).find("#lr_end_time").val()
        var count = $("#lead-card-" + parent_id).find("#count").val()
        var time_diff = moment.utc(moment(end_time, "HH:mm").diff(moment(start_time, "HH:mm"))).format("HH:mm")
        if (count != 0) {
            var interval = moment.duration(time_diff).asSeconds() / count
            var formatted_interval = moment.utc(interval * 1000).format('HH:mm');
        }
    }
    return [formatted_interval, interval]
}
// this function is used to set lead section name
$(document).on('blur', '#lr_start_time', function() {
    var parent = $(this).attr("data-parent").split("-")[2]
    var lead_name = $(parent).find(".lead_name").val()
    $(parent).find(".lr_start_time").val("")
    var frequency = $(parent).find("#count").val()
    var start_time = $(this).val()
    var end_time = $("#lead-card-" + parent).find("#lr_end_time").val()
    if (end_time != "") {
        var startTime = moment(start_time, "hh:mm");
        var endTime = moment(end_time, "hh:mm");
        startTime.toString()
        endTime.toString()
        if (startTime.isAfter(endTime) == true) {
            var end_time = moment.utc($(this).val(), 'HH:mm').add(1, 'hour').format('HH:mm')
            $("#lead-card-" + parent).find("#lead-end-time input").removeAttr("disabled").val(end_time)
        }
    } else {
        var end_time = moment.utc($(this).val(), 'HH:mm').add(1, 'hour').format('HH:mm')
        $("#lead-card-" + parent).find("#lead-end-time input").removeAttr("disabled").val(end_time)
    }
    var get_interval = calculateInterval(parent)
    $("#lead-card-" + parent).find("#lead-time-div").removeClass("d-none")
    $("#lead-card-" + parent).find("#lead_time").val(get_interval[0]).attr("data-interval", get_interval[1])
})

$(document).on('blur', '#lr_end_time', function() {
    var parent = $(this).attr("data-parent").split("-")[2]
    var lead_name = $("#lead-card-" + parent).find(".lead_name").val()
    var start_time = $("#lead-card-" + parent).find("#lr_start_time").val()
    var end_time = $(this).val()
    var startTime = moment(start_time, "hh:mm");
    var endTime = moment(end_time, "hh:mm");
    startTime.toString()
    endTime.toString()
    if (startTime.isAfter(endTime) == true) {
        var end_time = moment.utc($(this).val(), 'HH:mm').subtract(1, 'hour').format('HH:mm')
        $("#lead-card-" + parent).find("#lr_start_time").val(end_time)
    }
    var frequency = $(parent).find("#count").val()
    var get_interval = calculateInterval(parent)
    $("#lead-card-" + parent).find("#lead-time-div").removeClass("d-none")
    $("#lead-card-" + parent).find("#lead_time").val(get_interval[0]).attr("data-interval", get_interval[1])
})

$(document).on('blur', '#count', function() {
    var parent = $(this).attr("data-parent").split("-")[2]
    var get_interval = calculateInterval(parent)
    $("#lead-card-" + parent).find("#lead_time").val(get_interval[0]).attr("data-interval", get_interval[1])
})

$(document).on('blur', '#lead_time', function() {
    var parent = $(this).attr("data-parent").split("-")[2]
    var current_val = moment.duration($(this).val()).asSeconds()
    $("#lead-card-" + parent).find("#lead_time").attr("data-interval", current_val)
})


$("#add-lead-btn").click(function() {
    $("#accordion").find(".lead-heading").attr("aria-expanded", false)
    $("#accordion").find(".collapse-div").removeClass("show")
    var cloned_div = $("#lead-card-1").clone()
    var count = parseInt($("#get-count").val()) + 1
    $("#get-count").val(count)
    cloned_div.find('.schedule_type').val('Select Time');
    cloned_div.find('.lead_name').val('Select Disposition').attr("id", "lead_name-" + count);
    cloned_div.find("#lead-heading-1").attr("id", "lead-heading-" + count)
    cloned_div.find(".remove-lead").removeClass("d-none").attr("id", "remove-lead-" + count)
    cloned_div.find(".existing_lead_id").val(0)
        // cloned_div.find(".lead-heading").attr({"href":"#lead-collaps-"+count, "aria-expanded":true}).text("Recycle Lead-"+count)
    cloned_div.find(".lead-heading").attr({
        "href": "#lead-collaps-" + count,
        "aria-expanded": true
    }).text("Lead Recycle")
    cloned_div.find("#lead-collaps-1").attr({
        "aria-labelledby": "lead-heading-" + count,
        "id": "lead-collaps-" + count
    }).addClass("show")
    cloned_div.find("#schedule_type").attr("data-parent", count)

    cloned_div.find("#start_timepicker_1 div").find('input').attr("data-target", "#start_timepicker_" + count).val("").attr("data-parent", "#lead-card-" + count)
    cloned_div.find("#start_timepicker_1 div").attr("data-target", "#start_timepicker_" + count)
    cloned_div.find("#start_timepicker_1").attr("id", "start_timepicker_" + count)

    cloned_div.find("#end_timepicker_1 div").find('input').attr("data-target", "#end_timepicker_" + count).val("").attr("data-parent", "#lead-card-" + count)
    cloned_div.find("#end_timepicker_1 div").attr("data-target", "#end_timepicker_" + count)
    cloned_div.find("#end_timepicker_1").attr("id", "end_timepicker_" + count)
    cloned_div.find("#lead-start-time, #lead-end-time, #lead-time-div").addClass("d-none")
    cloned_div.find("#lead_time, #count").val(0).attr("data-parent", "#lead-card-" + count)
    cloned_div.attr("id", "lead-card-" + count)

    cloned_div.find("#lr_interval_1 div").find('input').attr("data-target", "#lr_interval_" + count).val("").attr("data-parent", "#lead-card-" + count)
    cloned_div.find("#lr_interval_1 div").attr("data-target", "#lr_interval_" + count)
    cloned_div.find("#lr_interval_1").attr("id", "lr_interval_" + count)
    $("#accordion").append(cloned_div)
    $(".lr-start-time, .lr-end-time, .lr-interval-time").datetimepicker({
        format: 'HH:mm'
    });
})
$(document).on('click', '.remove-lead', function() {
    var current_element = $(this).attr("id")
    var parent_id = current_element.split("-")[2]
    var delete_lead_id = $(this).attr("data-lead_id")
    if (delete_lead_id) {
        $("#campaign-edit-form").append("<input type='hidden' name='delete_lead_id' value='" + delete_lead_id + "'>")
    }
    if ($('#accordion').children('div').length > 1) {
        var count = parseInt($("#get-count").val()) - 1
        $("#get-count").val(count)
        $("#start_timepicker_" + parent_id + ", #end_timepicker_" + parent_id + ",#lr_interval_" + parent_id).data("datetimepicker").destroy();
        $("#lead-card-" + parent_id).remove()
        $('#accordion').children('div').each(function(i, current_child) {
            var child_id = $(this).attr("id").split("-")[2]
            i = i + 1
            $(this).find(".lr-start-time").data("datetimepicker").destroy()
            $(this).find(".lr-end-time").data("datetimepicker").destroy()
            $(this).find(".lr-interval-time").data("datetimepicker").destroy()
            var lead_name = $(this).find(".lead_name").val()
            if (lead_name == "Select Disposition") {
                lead_name = ""
            }
            $(this).find(".card-header").attr("id", "lead-heading-" + i)
            $(this).find(".remove-lead").removeClass("d-none").attr("id", "remove-lead-" + i)
            if (lead_name) {
                $(this).find(".lead-heading").attr({
                    "href": "#lead-collaps-" + i,
                    "aria-expanded": true
                }).text(lead_name.toUpperCase())
            } else {
                $(this).find(".lead-heading").attr({
                    "href": "#lead-collaps-" + i,
                    "aria-expanded": true
                }).text("Lead Recycle")
            }
            $(this).find(".collapse-div").attr({
                "aria-labelledby": "lead-heading-" + i,
                "id": "lead-collaps-" + i
            }).addClass("show")
            $(this).attr("id", "lead-card-" + i)
            $(this).find("#schedule_type").attr("data-parent", i)
            $(this).find(".lead_name").attr("id", "lead_name-" + i)
            $(this).find(".lr-start-time").attr("id", "start_timepicker_" + i)
            $(this).find(".lr-start-time div").attr("data-target", "#start_timepicker_" + i).data("target", "#start_timepicker_" + i)
            $(this).find(".lr-start-time div").find('input').data({
                "target": "#start_timepicker_" + i,
                "parent": "#lead-card-" + i
            }).attr({
                "data-target": "#start_timepicker_" + i,
                "data-parent": "#lead-card-" + i
            })
            $(this).find(".lr-end-time").attr("id", "end_timepicker_" + i)
            $(this).find(".lr-end-time div").attr("data-target", "#end_timepicker_" + i).data("target", "#end_timepicker_" + i)
            $(this).find(".lr-end-time div").find('input').data({
                "target": "#end_timepicker_" + i,
                "parent": "#lead-card-" + i
            }).attr({
                "data-target": "#end_timepicker_" + i,
                "data-parent": "#lead-card-" + i
            })
            $(this).find(".lr-interval-time div").find('input').data({
                "target": "#lr_interval_" + i,
                "parent": "#lead-card-" + i
            }).attr({
                "data-target": "#lr_interval_" + i,
                "data-parent": "#lead-card-" + i
            })
            $(this).find(".lr-interval-time div").attr("data-target", "#lr_interval_" + i).data("target", "#lr_interval_" + i)
            $(this).find(".lr-interval-time").attr("id", "lr_interval_" + i)
            $(this).find(".lr-start-time, .lr-end-time, .lr-interval-time").datetimepicker({
                format: 'HH:mm'
            });
        });
        $("#accordion").find(".lead-heading").attr("aria-expanded", false)
        $("#accordion").find(".collapse-div").removeClass("show")
    } else {
        $("#start_timepicker_1, #end_timepicker_1").data("datetimepicker").destroy();
        $("#lead-card-" + parent_id).find('#schedule_type').val('Select Time');
        $("#lead-card-" + parent_id).find('.lead_name').val('Select Disposition');
        $("#lead-heading-" + parent_id).find("a").text("Lead Recycle")
        $("#lead-card-" + parent_id).find('input:text').val('');
        $("#lead-collaps-" + parent_id).addClass("show")
        $("#lead-card-" + parent_id).find('#count').val(0)
        $("#lead-collaps-" + parent_id).find("#lead-start-time, #lead-end-time, #lead-time-div").addClass("d-none")
        $("#lead-card-" + parent_id).find("#start_timepicker_1, #end_timepicker_1, #lr_interval_1").datetimepicker({
            format: 'HH:mm'
        });
    }

});
var avail_dispo_list = []
$("#lead-settings-tab").click(function() {

    required_dispo = true
    var dial_method = false
    if ($("#campaign_inbound").prop("checked") == true || $("#campaign_manual").prop("checked") == true || $("#camp_outbound_check").prop("checked") == true) {
        dial_method = true
    }
    else {
        $("#dial_method_msg").removeClass("d-none")
        // $("#lead-recycle-settings").removeClass("show active")
    }
    if ($("#campaign-create-form").isValid() && required_dispo && dial_method) {
        
        $(".lead_name option").remove();
        $(".lead_name").append("<option value='Select Disposition'>Select Disposition</option>")
        $(".selected-disposition .badge-pill").each(function(){ 
            avail_dispo_list.push($(this).text())
            $(".lead_name").append("<option value='"+$(this).text()+"'>"+$(this).text()+"</option>")
        })
        if($('#wfh').prop('checked')){
            $.each(wfh_vue.wfh_list, function(index,value){
                if($.inArray(avail_dispo_list, value) == -1){
                    avail_dispo_list.push(value)
                    $(".lead_name").append("<option value='"+value+"'>"+value+"</option>")
                }
            })
        }
        $.each(voice_blaster_vue.vb_dtmf, function(index,value){
            avail_dispo_list.push(value)
            $(".lead_name").append("<option value='"+value+"'>"+value+"</option>")
        })
        $(".lead_name").append("<option value='Drop'>Drop</option><option value='NC'>NC</option> \
            <option value='Invalid Number'>Invalid Number</option><option value='Abandonedcall'>Abandonedcall</option>\
            <option value='AutoFeedback'>AutoFeedback</option><option value='DropCallback'>DropCallback</option>\
            <option value='CBR'>CBR</option><option value='NF(No Feedback)'>NF(No Feedback)</option>")
        if (lead_list) {
            $(lead_list).each(function(index,value){
                if ($("#lead-collaps-"+(index+1)).find(".lead_name option[value='"+value[index+1]+"']").length > 0 ) {
                    $("#lead-collaps-"+(index+1)).find(".lead_name").val(value[index+1])
                }
                else {
                    $("#lead-collaps-"+(index+1)).find(".lead_name").append("<option selected value='"+value[index+1]+"'>"+value[index+1]+"</option>")
                }
            });
        }
        $(this).attr("href", "#lead-recycle-settings")
        $(".tab-pane").removeClass("show active")
        $("#lead-recycle-settings").addClass("show active")
    }
    else {
        $(this).attr("href", "#")
        $("#lead-recycle-settings").removeClass("show active")
    }
})
$(document).on('click', '#campaign_inbound', function() {
    if ($(this).prop("checked")) {
        $('#ibc_div, #inbound_threshold_div, #sticky_agent_map_div,#no_agent_audio_div').removeClass('d-none')
        $("#camp_outbound option[value='Progressive']").hide();
        $("#camp_outbound option[value='Preview']").hide();
    } else {
        $("#camp_outbound option[value='Progressive']").show();
        $("#camp_outbound option[value='Preview']").show();
        $('#ibc_div, #inbound_threshold_div, #sticky_agent_map_div,#no_agent_audio_div').addClass('d-none')
        $("#ibc_popup,#no_agent_audio").prop("checked", false);
    }
})

$("#camp_outbound_check").click(function() {
    if ($(this).prop("checked")) {
        $("#outbound-div").removeClass("d-none")
        if ($("#camp_outbound").val() == "Predictive") {
            $("#portifolio").css("pointer-events", "none").attr("disabled", true)
        }
    } else {
        $("#outbound-div").addClass("d-none")
        $('#progressive_time_div').addClass("d-none")
        $("#camp_outbound").val("Predictive")
        $('#progressive_time').val("")
    }
})

$(document).on('change', "#camp_outbound", function() {
    if ($("#camp_outbound option:selected").val() == 'Predictive') {
        $("#portifolio").css("pointer-events", "none").attr("disabled", true)
        $("#portifolio").prop("checked", false)
    } else {
        $("#portifolio").css("pointer-events", "").attr("disabled", false)
    }
    if ($("#camp_outbound option:selected").val() == 'Progressive') {

        $("#progressive_time").val('02:00');

        $('#progressive_time_div').removeClass("d-none")

        if ($('#progressive_time option:selected').val() == '') {
            $('#progressive_time').attr('data-validation', 'required')
        }
    } else {
        $('#progressive_time_div').addClass("d-none")
        $('#progressive_time').val("")
    }
})
$("#campaign-settings-tab").click(function() {
    if ($("#campaign-edit-form").isValid()) {
        $(this).attr("href", "#campaign-additional-settings")
        $(".tab-pane").removeClass("show active")
        $("#campaign-additional-settings").addClass("show active")
    }
})
$("#lead-prioritize-tab").click(function() {
    if ($("#lead-prioritize-tab").isValid()) {
        $(this).attr("href", "#lead-prioritize-settings")
        $(".tab-pane").removeClass("show active")
        $("#lead-prioritize-settings").addClass("show active")
        if($('input[name=prioritize]:checked').val()!=='tapd'){
            $("#prioritize-period-select").addClass("d-none")
        }else{
            $("#prioritize-period-select").removeClass("d-none")
        }
        if($('#prioritize-status').val()==''){
            $("#after-class, #after-priotitize, #after-period").addClass("d-none")
        }
    }
})
$("#lead-priority-status").click(function(){
     if($(this).is(":checked")) {
        $("#lead-priority-status").val(true);
    }else{
        $("#lead-priority-status").val(false);
    }
})

$("#prioritize-status").change(function(){
  if($(this).val()!==''){
    $("#after-class, #after-priotitize, #after-period").removeClass("d-none")
  }else{
    $("#after-class, #after-priotitize, #after-period").addClass("d-none")
  }
});

//Prioritize
$('input[type=radio][name=prioritize]').change(function() {
    current_selectd[''+this.value+'']=true
    if(this.value==='tapd'){
        $("#prioritize-period-select").removeClass("d-none")
        current_selectd['tac']=false
        current_selectd['tap']=false
        current_selectd['period']=$('#prioritize-period').val()
    }else{
        $("#prioritize-period-select").addClass("d-none")
    }
    if(this.value==='tac'){
        current_selectd['tapd']=false
        current_selectd['period']=''
        current_selectd['tap']=false
    }
    if(this.value==='tap'){
        current_selectd['tapd']=false
        current_selectd['period']=''
        current_selectd['tac']=false
    }
});


$(".crm-fields-modify").click(function() {
    var id = $(this).attr("id").split("-")[2]
    $.ajax({
        type: 'POST',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/Administration/CrmField/edit/' + id + '/',
        success: function(data) {
            if (['dropdown', 'radio'].includes(data["field_type"])) {
                $("#edit-crm-field-modal").find("#field_options_div").removeClass("d-none");
                $("#edit-crm-field-modal").find("#field_options").val(data["options"]);
            } else if (['text', 'textarea', 'integer'].includes(data["field_type"])) {
                $("#edit-crm-field-modal").find("#field_size_div").removeClass("d-none");
                $("#edit-crm-field-modal").find("#field_size").val(data["size"]);
            }
            $("#edit-crm-field-modal").find("#field").val(data["field"]);
            $("#edit-crm-field-modal").find("#field_type").val(data["field_type"]);
            $("#edit-crm-field-modal").find("#editable").prop("checked", data["editable"]);
            $("#edit-crm-field-modal").find("#field_priority").val(data["priority"]);
            $("#edit-crm-field-modal").find("#field_status").val(data["status"]);
            $("#edit-crm-field-modal").modal('show');
            $("#edit-crm-field-modal").find(".update-crm-fields").attr("id", "update-crm-fields-" + id)
        },
        error: function(data) {}
    });
})
$("#edit-crm-field-modal").on('hidden.bs.modal', function() {
    $("#update-crm-fields-form")[0].reset();
    $(this).find("#field_size_div, #field_options_div").addClass("d-none");
});
var CrmFieldWizard = $("#update-crm-fields-form");
CrmFieldWizard.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {}
});
$(document).on('click', '.update-crm-fields', function() {
    var current_element = $(this).attr("id").split("-")[3]
    var form = $("#update-crm-fields-form").serialize()
    $.ajax({
        type: 'put',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/Administration/CrmField/edit/' + current_element + '/',
        data: form,
        success: function(data) {
            showSwal('success-message', 'CRM fields updated successfully')
        },
        error: function(data) {
            if ("field" in data["responseJSON"]) {
                $("#field-msg").addClass("has-error").html(
                    '<span class="help-block form-error">' + data["responseJSON"]["field"] + '</span>').removeClass("d-none")
                setTimeout(function() {
                    $("#field-msg").addClass("d-none")
                }, 3000);
            }
        }
    });

})

$(".sample_phonebook").click(function() {
    var file_type = ""
    if ($(this).hasClass("csv")) {
        file_type = "csv"
    } else {
        file_type = "xls"
    }
    if($("#action_type").val() == "transfer_contacts") {
        url = `/api/download-sample-contact-file/transfer_contacts/${file_type}/`
        $(this).attr("href", url)
    }
    else {
        var campaign_name = $("#phonebook-campaign :selected").attr("data-name")
        if (campaign_name) {
            if($("#action_type").val() == "update"){
                var dup_check = $('#duplicate_check').val()
                if (dup_check){
                    var selected_col = 'all'
                    if($('#update_crm_fields').val().join(',')){
                        selected_col = $('#update_crm_fields').val().join(',')
                    }
                    url = `/api/get-sample-update-phonbook-file/?campaign=${campaign_name}&col_list=${selected_col}&duplicate_check_col=${dup_check}&file_type=${file_type}`
                    $(this).attr("href", url)
                }else{
                    $('#phonebook-err-msg').text("Please select Reference Field").removeClass('d-none')
                    setTimeout(function() {
                        $('#phonebook-err-msg').addClass("d-none")
                    }, 5000);
                }
            } else{
                var url = `/CRM/get-sample-phonebook/${campaign_name}/${file_type}/`
                $(this).attr("href", url)
            }
        } else {
            $('#phonebook-err-msg').text("Please select campaign first").removeClass('d-none')
            setTimeout(function() {
                $('#phonebook-err-msg').addClass("d-none")
            }, 5000);
        }

    }

})
function dynamic_phonebook(selected_phonebook = "") {
    var campaign = $("#contact_campaign_select").val()
    if (campaign) {
        $("#contact_phonebook_select").find("option").remove()
        if (selected_phonebook) {
            $("#contact_phonebook_select").append(new Option("Select Phonebook", "", true, true))
        } else {
            $("#contact_phonebook_select").append(new Option("Select Phonebook", "", false, false))
        }
        $.each(phonebook_list, function(index, value) {
            if (value.campaign == campaign && value.status == "Active") {
                if (selected_phonebook == value.id) {
                    var new_op = new Option(value.name, value.id, true, true)
                } else {
                    var new_op = new Option(value.name, value.id, false, false)
                }
                $("#contact_phonebook_select").append(new_op).trigger('change');
            }
        });

        $("#phonebook-div").removeClass("d-none")
        $("#filter_contacts_info").removeClass("d-none")

    }
}
$("#contact_campaign_select").change(function() {
    if ($(this).val() != "") {
        $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/api/get-dispo/',
            data: {
                'campaign_id': $(this).val()
            },
            success: function(data) {
                $("#contact_phonebook_select").find("option").remove()
                // $("#contact_phonebook_select").append(new Option("Select Phonebook", "", true, true))
                $.each(data['phonebook_list'], function(index, value) {
                    var new_phonbook = new Option(value.name, value.id, false, false)
                    $("#contact_phonebook_select").append(new_phonbook).trigger('change');
                });
                $("#disposition").find("option").remove()
                // $("#disposition").append(new Option("Select Disposition", "", true, true))
                $.each(data['dispo_list'], function(index, value) {
                    var new_dispo = new Option(value, value, false, false)
                    $("#disposition").append(new_dispo).trigger('change');
                });
                $("#contact_agent_select").find("option").remove()
                $.each(data['users'], function(index, value) {
                    var new_user = new Option(value.username, value.username, false, false)
                    $("#contact_agent_select").append(new_user).trigger('change');
                });
            }
        })
        $(".contact-filter-div").removeClass("d-none")
    } else {
        $(".contact-filter-div").addClass("d-none")
    }
    $('#contact_info_download_toggle').addClass('d-none')
})

$('#filter_contacts_info').click(function() {
    $.ajax({
        type: 'get',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/CRM/ContactInfo/',
        data: {
            "phonebook": $('#contact_phonebook_select').val(),
            "campaign": $("#contact_campaign_select").val()
        },
        success: function(data) {
            var columns_list = []
            $.each(data['columns_list'], function(index, value) {
                var column_dict = {}
                column_dict['data'] = value
                column_dict['name'] = value
                column_dict['className'] = value
                column_dict['title'] = value.replace('_', ' ')
                columns_list.push(column_dict)
            })
            $.each(data['crm_fields'], function(index, value) {
                var column_dict = {}
                var data = value.replace(/  +/g, ' ').replace(/ /g, "_").replace(':', '.').toLowerCase();
                column_dict['data'] = 'contact_info.' + data
                column_dict['title'] = value
                columns_list.push(column_dict)
            })
            columns_list.push({
                'data': 'id',
                'title': 'Action'
            })
            if ($.fn.DataTable.isDataTable('#contact-info-table')) {
                contact_info_table.clear().destroy();
                $('#contact-info-table').empty()
            }
            contact_info_table = $('#contact-info-table')
            if(data["report_visible_cols"].length > 0) {
                contact_info_table = contactInfoTable(table, columns_list, data["report_visible_cols"])
            }
            else {
                contact_info_table = contactInfoTable(table, columns_list)

            }

        }
    })
})
$('#contact-info-table').on('processing.dt', function(e, settings, processing) {
    if (!processing) {
        if (contact_info_table.data().any()) {
            $('#contact_info_download, #contact_info_download_toggle').removeClass('d-none')
        }
    }
})
$(".contact_info_download").click(function() {
    is_download = true;
    var col_title = ""
    var col_name = ""
    if($(this).hasClass('pending_contacts')){
        var columns = pending_contact_table.settings().init().columns
        pending_contact_table.columns().every(function(index) {
            if (this.visible()) {
                if (columns[index].title != 'Action') {
                    if (col_title) {
                        col_title = col_title + ',' + columns[index].title
                    } else {
                        col_title = columns[index].title
                    }
                    if (col_name) {
                        col_name = col_name + ',' + columns[index].data
                    } else {
                        col_name = columns[index].data
                    }
                }
            }
        })
        $('#col_title_list').val(col_title)
        $('#col_name_list').val(col_name)
        $('#contact_info_download_val').val('download')
        var form = $("#pending_report_form");
    }else{
        var columns = contact_info_table.settings().init().columns
        contact_info_table.columns().every(function(index) {
        if (this.visible()) {
            if (columns[index].title != 'Action') {
                if (col_title) {
                    col_title = col_title + ',' + columns[index].title
                } else {
                    col_title = columns[index].title
                }
                if (col_name) {
                    col_name = col_name + ',' + columns[index].data
                } else {
                    col_name = columns[index].data
                }
            }
        }
        })
        $('#col_title_list').val(col_title)
        $('#col_name_list').val(col_name)
        $('#contact_info_download_val').val('download')
        $('#contact_info_download_type').val($(this).attr('id'))
        var form = $("#report_form");
    }
     $.ajax({
        type: 'post',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: location.pathname,
        data: form.serialize(),
        success: function(data) {
            showSwal('success-message', data.message)
        },
        error: function(data) {
            console.log(data);
        },
        complete: function(){
            $('#contact_info_download_val').val('')
            $('#col_title_list').val('')
            $('#col_name_list').val('')
        }
    })
})

$("#update-contact-btn").click(function() {
    var id = $(this).attr("data-contact-id")
    custom_raw_data = {}
    $(".section_div").each(function() {
        var section_name = $(this).attr("id")
        $(this).find("input").each(function() {
            custom_raw_data[$(this).attr("id")] = $(this).val()
        })
    })
    $("#customer_raw_data").val(JSON.stringify(custom_raw_data))
    var form = $("#edit-contact-info").serialize()
    if ($("#edit-contact-info").isValid()) {
        $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/CRM/ContactInfo/' + id + '/',
            data: form,
            success: function(data) {
                showSwal('success-message', 'Contact Detail Updated', '/CRM/ContactInfo/')
            },
            error: function(data) {

            }
        });
    }
})

$("#upload-ndnc, #upload-priority").click(function() {
    var data = new FormData($('#ndnc-upload-form').get(0));
    var fileExtension = ['csv'];
    if ($(".dropify-filename-inner").text()) {
        if ($.inArray($(".dropify-filename-inner").text().split('.').pop().toLowerCase(), fileExtension) == -1) {
            $("#upload-file-error, #csv-error").text("File format must be csv").removeClass("d-none")
            setTimeout(function() {
                $("#upload-file-error, #csv-error").addClass("d-none")
            }, 3000);
        } else {
            $.ajax({
                type: $('#ndnc-upload-form').attr('method'),
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: $('#ndnc-upload-form').attr('action'),
                cache: false,
                processData: false,
                contentType: false,
                data: data,
                beforeSend: function() {
                    $('.preloader').fadeIn('fast');
                },
                success: function(data) {
                    $('.preloader').fadeOut('fast');
                    showSwal('success-message', 'Data uploaded successfully')
                },
                error: function(data) {
                    $('.preloader').fadeOut('fast');
                    $("#csv-error").text(data.responseJSON.msg);
                }
            });
        }
    } else {
        $("#upload-file-error").text("Upload File").removeClass("d-none")
        setTimeout(function() {
            $("#upload-file-error").addClass("d-none")
        }, 3000);
    }
})

$("#cancel-ndnc-upload, #cancel-priority-upload").click(function() {
    showSwal('success-message', 'Upload Operation Cancelled')
    $(".dropify-clear").click()
})
$('#starting-date, #ending-date').datepicker({
    endDate: '+0d',
    enableOnReadonly: true,
    todayHighlight: true,
    format: 'yyyy-mm-dd',
    orientation: 'bottom auto',
    autoclose: true,
});

$("#filter-report, #agent_reports_download, .agent_reports_download").click(function() {
    var start_date = moment($("#start-date input").val())
    var end_date = moment($("#end-date input").val())
    var btn_type = $(this).text()
    var all_users = $('#agent_activity_users option').map(function() {
        return $(this).val();
    }).get();
    var all_campaigns = $('#agent_report_campaign option').map(function() {
        return $(this).val();
    }).get();
    if (end_date < start_date) {
        $("#end-date-error").removeClass("d-none")
    } else {
        if (btn_type != 'Filter') {
            var col_name = ""
            $(".dataTables_scrollHeadInner #column_name th").each(function(index) {
                temp_name = $(this).attr("data-field_name")
                if (temp_name) {
                    if (col_name) {
                        col_name = col_name + "," + temp_name
                    } else {
                        col_name = temp_name
                    }
                }
            });
            $('#column_name_list').val(col_name)
            $('#agent_reports_download').val("download")
            $('#agent_reports_download_type').val($(this).attr('id'))
            $('#selected_records').val(result)
        } else {
            $('#agent_reports_download').val("")
            $('#agent_reports_download_type').val($(this).attr('id'))
        }
        $("#call_details_flag").val("true")
        $('#all_users').val(all_users)
        $('#all_campaigns').val(all_campaigns)
        if($('#down_zip').val()){
            $("#report_form").submit()
        }else{
            var form = $("#report_form");
            $("#end-date-error").addClass("d-none")
             $.ajax({
                type: 'post',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: location.pathname,
                data: form.serialize(),
                success: function(data) {
                    is_download=true
                    showSwal('success-message', data.message)
                },
                error: function(data) {
                    console.log(data);
                }
            })
        }
        
    }
})

$("#bulk_call_reacording_download").click(function(event) {
    $.ajax({
        type: 'POST',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: url,
        data: {
            customer_cid : $('#destination_extension').val(),
            selected_campaign : $('#agent_report_campaign').val(),
            all_campaigns : $('#agent_report_campaign option').map(function() { return $(this).val(); }).get(),
            selected_user : $('#agent_activity_users').val(),
            all_users : $('#agent_activity_users option:not(.d-none):not(:first)').map(function() { return $(this).val(); }).get(),
            start_date : $("#start-date input").val(),
            end_date : $("#end-date input").val(),
            agent_reports_download:true
        },
         success: function(data) {
         }
     })
})

$('#agent_report_campaign,#agent_activity_users,#agent_activity_agent').select2()
if($('#disposition').length != 0 && $('#disposition').is('input') == false) {
    $('#disposition').select2() 
}
$(document).on('change.select2', '#agent_report_campaign,#agent_activity_users,#selected_columns1,#agent_activity_agent', function() {
    // $('#agent_report_campaign,#agent_activity_users,#selected_columns1').change(function(){
    if ($('#agent_report_campaign').val() || $('#agent_activity_users').val() || $('#selected_columns1').val() != ""|| $('#agent_activity_agent').val() != "") {
        $('#agent_reports_download').removeClass('d-none')
    } else {
        $('#agent_reports_download').addClass('d-none')
    }
})
report_selected_user = ""
$(document).on('change.select2', '#agent_report_campaign', function(e) {
    var campaign = $(this).val()
    if (campaign != "") {
        $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/api/get-campaign-users/',
            data: {
                "campaign": campaign
            },
            success: function(data) {
                $('#agent_activity_users').find('option').remove()
                // var newOption = new Option("Select User", "", true, true);
                // $("#agent_activity_users").append(newOption).trigger('change');
                if (jQuery.isEmptyObject(data["users"]) == false) {
                    $('#agent_activity_users').val(null).trigger('change');
                    $.each(data["users"], function(index, value) {
                        if (report_selected_user == value["id"]) {
                            var newOption = new Option(value.username, value.id, true, true);
                            $("#agent_activity_users").append(newOption).trigger('change');
                        }
                        else {
                            var newOption = new Option(value.username, value.id, false, false);
                            $("#agent_activity_users").append(newOption).trigger('change');
                        }
                    });

                } else {
                    $('#agent_activity_users').find('option').remove()
                }
                if (jQuery.isEmptyObject(data["disposition"]) == false) {
                    $('#disposition option').addClass("d-none")
                    $.each(data["disposition"], function(index, value) {
                        $('#disposition option[value="' + value["name"] + '"]').removeClass("d-none")
                    });
                } else {
                    $('#disposition option').addClass("d-none")
                    $('#disposition option[value=""]').removeClass("d-none")
                }

            },
            error: function(data) {

            }
        });
    } else {
        $('#agent_activity_users').find('option').remove()
        $.each(users, function(index, value) {
            var newOption = new Option(value.username, value.id, false, false);
            $("#agent_activity_users").append(newOption).trigger('change');
        })
    }
})

$("#lead_list_campaign,#campaign_list").change(function(){
    if($('#lead_list_campaign,#campaign_list').val()!=''){
        $('#download-lead-sample,#download-third-party-sample').removeClass('d-none');
        $("#csv-error").text("Click on Sample CSV to download file.");
        if($('#uploaded-file').val()!=''){
            $('#upload-priority').removeClass('d-none')
        }else{
            $('#upload-priority').addClass('d-none');
        }
    }else{
        $("#csv-error").text("Please Select Campaign");
        $('#download-lead-sample,#download-third-party-sample, #upload-priority').addClass('d-none');
    }
})
$("#uploaded-file").change(function(){
    if($('#uploaded-file').val()!='' && $('#lead_list_campaign,#campaign_list').val()!=''){
        $('#upload-priority').removeClass('d-none')
    }else{
        $('#upload-priority').addClass('d-none')
    }
})
$("#download-lead-sample").click(function(){
     var campaign_name = $('#lead_list_campaign').children('option:selected').text()
    var campaign_id = $('#lead_list_campaign').val();
    if(campaign_id!=''){
        $.ajax({
            type: 'GET',
            xhrFields: {
                responseType: 'blob'
            },
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/CRM/lead-priority-csv/',
            data: {
                "campaign_name": campaign_name,
                "campaign_id": campaign_id,
            },
            success: function(data) {
                try {
                    var a = document.createElement('a');
                    var url = window.URL.createObjectURL(data);
                    a.href = url;
                    a.download = 'lead-priority.csv';
                    document.body.append(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                    $("#csv-error" ).text("Successfully Downloaded");
                }
                catch(err) {
                  
                }
                
            },
            error:function(data){
                $("#csv-error").text("Columns Not Found or Priority is not active in campaign");
            }
        });
    }
})


$("#download-third-party-sample").click(function(){
     var campaign_name = $('#campaign_list').children('option:selected').text()
    var campaign_id = $('#campaign_list').val();
    if(campaign_id!=''){
        $.ajax({
            type: 'GET',
            xhrFields: {
                responseType: 'blob'
            },
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/api/third-party-csv/',
            data: {
                "campaign_name": campaign_name,
                "campaign_id": campaign_id,
            },
            success: function(data) {
                try {
                    var a = document.createElement('a');
                    var url = window.URL.createObjectURL(data);
                    a.href = url;
                    a.download = 'third-party-user.csv';
                    document.body.append(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                    $("#csv-error" ).text("Successfully Downloaded");
                }
                catch(err) {
                  
                }
                
            },
            error:function(data){
                $("#csv-error").text("Columns Not Found or Priority is not active in campaign");
            }
        });
    }
})

$("#script_campaign_select").change(function() {
    var campaign_name = $(this).children('option:selected').text()
    var campaign_id = $(this).val();
    var script_id = $("input[name='script_id']").val()
    if ($(this).val() != "") {
        $.ajax({
            type: 'POST',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/CampaignManagement/Script/get-crm-fields/',
            data: {
                "campaign_name": campaign_name,
                "campaign_id": campaign_id,
                "script_id": script_id
            },
            success: function(data) {
                if ('script_exists' in data) {
                    $("#script_campaign_select").addClass('error')
                    $("#script_campaign_select").parent().addClass('has-error')
                    $("#script_error").removeClass("d-none");
                    $("#script_error").text(data["script_exists"]);
                } else {
                    $("#script_error").addClass("d-none");
                    $("#script_error").text("");
                    var editorField_list = []
                    $.each(data['contact_fields'], function(index, value) {
                        var editiorField_dict = {}
                        editiorField_dict['text'] = editiorField_dict['value'] = value
                        editorField_list.push(editiorField_dict)
                    });
                    if (tinymce.get('scriptEditor')) {
                        tinymce.remove('#scriptEditor');
                    }
                    addScriptEditior(editorField_list)
                }
            },
            error: function(data) {

            }
        });
    } else {
        $('#namespace_fields').val('')
    }
    tinyMCE.activeEditor.setContent('');

})

$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
});

$("#administration_logout").click(function() {
    $.ajax({
        type: 'get',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/logout/',
        data: session_details[extension],
        success: function(data) {
            window.location.href = '/'
        }
    });
});

var group_user_count = 0
    // var group_user_list = []

function get_users_in_group(current_element, group_user_list) {
    var users = $(current_element).attr("data-content").split(",")
    var changed_list = []
    if (users != "") {
        $.each(users, function(index, value) {
            if (value != " ") {
                if ($.inArray(value.trim(), group_user_list) == -1) {
                    changed_list.push(value.trim())
                }
            }
        });
    }
    return changed_list
}
var previous_hopper = 0
function portfolio_hopper_calculation(hopper_count, users_count){
    if(hopper_count && users_count){
        let user_wise_contacts = Math.round(hopper_count/users_count)
        $('#portfolio_hopper').text(user_wise_contacts+" contacts per User in portfolio")   
    }else{
        $('#portfolio_hopper').text(hopper_count+" contacts per User in portfolio")
    }
}
function calculate_hopper_level(group_id, dial_ratio) {
    var selected_user = $(".camp_users option:selected")
    var group_user_list = []
    if ($(group_id).children('div').length > 0) {
        $(group_id).children('div').each(function() {
            var changed_list = get_users_in_group(this, group_user_list)
            $.merge(group_user_list, changed_list);
            if (selected_user) {
                $(selected_user).each(function() {
                    var current_user = $(this).attr("data-username")
                    if (group_user_list.includes(current_user) == false) {
                        group_user_list.push(current_user)
                    }
                });
            }
        })
    } else {
        $(selected_user).each(function() {
            group_user_list.push($(this).attr("data-username"))
        });
    }
    if(previous_hopper !=0 && previous_hopper > Math.ceil(group_user_list.length * dial_ratio)){
       $("#hopper_level").val(previous_hopper) 
   }else{
    $("#hopper_level").val(Math.ceil(group_user_list.length * dial_ratio))
   }
$("#hopper_level_count_hidden").val("Total Users("+group_user_list.length+")* Dial Ratio ("+dial_ratio+") = "+Math.ceil(group_user_list.length * dial_ratio))
    var newArray = group_user_list.filter(function(v){return v!==''});
    portfolio_hopper_calculation($("#hopper_level").val(), newArray.length)
}
$(document).on('change','#portifolio',function(){
    if (this.checked == true) {
         $('#portfolio_hopper').removeClass('d-none')
        calculate_hopper_level("#profile-list-right", $('#dial_ratio').val())
    }else{
        $('#portfolio_hopper').addClass('d-none')
    }
})
$(document).on('change', '#dial_ratio', function() {
    calculate_hopper_level("#profile-list-right", $(this).val())
})
$(document).on('change', '#hopper_level', function() {
    var selected_user = $(".camp_users option:selected")
    var group_user_list = []
    if ($('#profile-list-right').children('div').length > 0) {
        $('#profile-list-right').children('div').each(function() {
            var changed_list = get_users_in_group(this, group_user_list)
            $.merge(group_user_list, changed_list);
            if (selected_user) {
                $(selected_user).each(function() {
                    var current_user = $(this).attr("data-username")
                    if (group_user_list.includes(current_user) == false) {
                        group_user_list.push(current_user)
                    }
                });
            }
        })
    } else {
        $(selected_user).each(function() {
            group_user_list.push($(this).attr("data-username"))
        });
    }
    var newArray = group_user_list.filter(function(v){return v!==''});
    portfolio_hopper_calculation($("#hopper_level").val(), newArray.length)
})
dragula([document.getElementById("profile-list-left"), document.getElementById("profile-list-right")]).on('drop', function(el, target) {
    var target = $(target).attr("id")
    var element = $(el)
    var dial_ratio = $('#dial_ratio').val()
    calculate_hopper_level("#profile-list-right", dial_ratio)

})
$(document).on('change', '.camp_users', function() {
    var selected_user = $(".camp_users option:selected")
    dial_ratio = $("#dial_ratio").val()
    if (!dial_ratio) {
        dial_ratio = 1.5
    }
    var group_user_list = []
    if ($("#profile-list-right").children('div').length > 0) {
        $("#profile-list-right").children('div').each(function() {
            var changed_list = get_users_in_group(this, group_user_list)
            $.merge(group_user_list, changed_list);
            $(selected_user).each(function() {
                var current_user = $(this).attr("data-username")
                if (group_user_list.includes(current_user) == false) {
                    group_user_list.push(current_user)
                }
            });

        })
    } else {
        $(selected_user).each(function() {
            group_user_list.push($(this).attr("data-username"))
        });
    }

    if(previous_hopper !=0 && previous_hopper > Math.ceil(group_user_list.length * dial_ratio)){
        $("#hopper_level").val(previous_hopper) 
    }else{
        $("#hopper_level").val(Math.ceil(group_user_list.length * dial_ratio))
    }
    var newArray = group_user_list.filter(function(v){return v!==''});
    portfolio_hopper_calculation($("#hopper_level").val(), newArray.length)
    $("#hopper_level_count_hidden").val("Total Users("+group_user_list.length+")* Dial Ratio ("+dial_ratio+") = "+Math.ceil(group_user_list.length * dial_ratio))
})
$('[data-name="hopper_level"]').popover({
        trigger : 'hover',
        title : 'Minimum Hopper Count',
        html:true,
        content:function(){
            return $('#hopper_level_count_hidden').val()
        } 
    })
$("#phonebook-campaign").change('click', function() {
    if ($(this).val() != "") {
        $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/CRM/duplicate-list-for-phonebook/',
            data: {
                "campaign": $("#phonebook-campaign :selected").text(),
                "phonebook_id": phonebook_id
            },
            success: function(data) {
                $("#duplicate_check option").remove()
                $("#crm_field option").remove()
                $('#update_crm_fields').empty().trigger("change");
                $("#duplicate_check").append(new Option("select field", ""))
                $("#duplicate_check").append(new Option("numeric", "numeric"))
                $("#crm_field").append(new Option("select crm field", ""))
                $("#update_crm_fields").append(new Option('user', 'user'))
                if(data["contact_list"].length > 0 ){
                    $.each(data["contact_list"], function(index, value) {
                        $("#crm_field").append(new Option(value, value))
                        if($.inArray(value,['status','uniqueid']) == -1){
                            $("#update_crm_fields").append(new Option(value, value))
                        }
                    })
                }
                if (data["columns"].length > 0) {
                    $.each(data["columns"], function(index, value) {
                        $("#duplicate_check, #crm_field, #update_crm_fields").append(new Option(value, value))
                    })
                }
                $('#update_crm_fields').trigger('change')
                duplicate_check = $("#ext_duplicate_check").val()
                if (duplicate_check != "") {
                    $("#duplicate_check").val(duplicate_check)
                    $('#update_crm_fields').find('option[value="'+duplicate_check+'"]').attr('disabled','disabled')
                }
                else{
                    $("#duplicate_check").val("")
                }
            },
            error: function(data) {
                if ("field_error" in data["responseJSON"]) {
                    if (data["responseJSON"]["field_error"]) {
                        $("#field_error").removeClass("d-none").text(data["responseJSON"]["field_error"])
                        $("#phonebook-campaign").val(data["responseJSON"]["campaign_name"]).trigger("change")
                        setTimeout(function() {
                            $("#field_error").addClass("d-none")
                        }, 3000);
                    }

                }

            }
        });
    }
})
$('#duplicate_check').change(function(){
    $('#update_crm_fields option').attr('disabled',false)
    if($(this).val()){
        $('#update_crm_fields').find('option[value="'+$(this).val()+'"]').attr('disabled','disabled')
    }
    $('#update_crm_fields').select2()
    $('#update_crm_fields').val(null).trigger('change')
})

$(document).on("click", ".download-sample-file", function() {
    var file_name = $(this).attr("file_name")
    var file_type = $(this).attr("file_type")
    url = `/api/download-sample-file/${file_name}/${file_type}/`
    $(this).attr("href", url)
})
$(document).on("click", ".download-sample-contact-file", function() {
    var col_name = $("#crm_field").val()
    if(col_name == "") {
        col_name = "numeric"
    }
    var file_type = $(this).attr("file_type")
    url = `/api/download-sample-contact-file/${col_name}/${file_type}/`
    $(this).attr("href", url)
})

$("#cancel-dnc-uploaded-file, #confirm-dnc-upload-file").click(function() {
    data = {}
    current_element = $(this)
    if ($(this).hasClass("confirm-dnc-upload")) {
        data["perform_upload"] = true
    }
    var proper_file = $("#proper-data").attr("href")
    var improper_file = $("#improper-data").attr("href")
    data["proper_file"] = proper_file
    data["improper_file"] = improper_file
    $.ajax({
        type: 'post',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/Administration/dnc-upload/',
        data: data,
        success: function(data) {
            if (current_element.hasClass("confirm-user-upload")) {
                showSwal('success-message', 'DNC Uploaded Successfully')
            } else {
                showSwal('success-message', 'Upload Operation Cancelled')
            }
            $(".dropify-clear").click()
            $("#proper-data, #improper-data, #confirm-dnc-upload-file, #cancel-dnc-uploaded-file").addClass("d-none")
            $("#validate-dnc-file").removeClass("d-none")
        },
        error: function(data) {}
    });
})

$("#api_weburl").change(function(){
    $.ajax({
        type: 'get',
        url: $("#api_weburl").val(),
        success: function(){
            $("#api_url_err_msg").html();
        },
        error: function(xhr, status, data) {
            $("#api_weburl").val('')
            $("#api_url_err_msg").html(`<span class="help-block form-error">Invalid API Url</span>`)
            $("#api_weburl").removeClass('valid');
            $("#api_weburl").addClass('error');
        }
      });
});

$(document).on('click', '#thirdparty_url', function() {
    if (this.checked == true) {
        $('#api_options_div').removeClass('d-none')
    } else {
        $('#api_options_div').addClass('d-none')
        $('#api_mode_select,#api_weburl').val('')
        $('#dap_url').prop('checked',false)
    }
})

$(document).on('click', '#dap_url', function() {
    if (this.checked == true) {
        $("#api_mode_select option[value='API-in-Iframe']").hide()
    } else {
        $("#api_mode_select option[value='API-in-Iframe']").show()
    }
})

function lead_list_churn(id) {
    data = {
        'id': id
    }
    $.ajax({
        type: 'GET',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/CRM/phonebook/lead-list-Churn/' + id + '/',
        data: data,
        success: function(data) {
            $("#summery_div").addClass("d-none")
            $("#churn_list_form")[0].reset()
            $('#lead-phonebook-churn, #user-churn').val('')
            $('#lead-phonebook-churn option, #user-churn option').remove()

            $('#leadchurn-smbt-button').val()
            $.each(data['camp_all_users'], function(index, value) {
                $('#user-churn').append($("<option ></option>").attr("value", value).text(value));
            })
            $.each(data['dispo_list'], function(index, value) {
                $('#lead-phonebook-churn').append($("<option ></option>").attr("value", data['dispo_list'][index]).text(data['dispo_list'][index]));
            })
            $('#lead-phonebook-churn').append(
                $("<option value='Drop'>Drop</option><option value='NC'>NC</option>\
                    <option value='Invalid Number'>Invalid Number</option>\
                    <option value='Abandonedcall'>Abandonedcall</option>\
                    <option value='AutoFeedback'>AutoFeedback</option>\
                    <option value='DropCallback'>DropCallback</option>\
                    <option value='NF(No Feedback)'>NF(No Feedback)</option>"))
            $('#LeadListModal').modal('show');
            $('#leadchurn-smbt-button').val(id)
        },
        error: function(data) {}
    });
}
$(document).on('click', '#leadchurn-smbt-button, #leadchurn-count-click', function() {
    if ($('#churn_list_form').isValid()) {
        selected_churn_dispos = $('#lead-phonebook-churn').val()
        var start_date = moment($("#start-date input").val())
        var end_date = moment($("#end-date input").val())
        if (end_date < start_date) {
            $("#end-date-error").removeClass("d-none")
            $("#leadchurn-err-msg").text("Start should be less than of end_time....").removeClass("d-none")
            setTimeout(function() {
                $("#leadchurn-err-msg").addClass("d-none")
            }, 3000);
            return false;
        }
        lead_id = $('#leadchurn-smbt-button').val()
        $('#lead_value').val($(this).attr('id'))
        if (selected_churn_dispos.length > 0) {
            $('.preloader').fadeIn('fast');
            //churn_dispos=JSON.stringify(selected_churn_dispos)
            $.ajax({
                type: 'POST',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/CRM/phonebook/lead-list-Churn/' + lead_id + '/',
                data: $('#churn_list_form').serialize(),
                success: function(data) {
                    if(data['final_count']>=0){
                        $('.preloader').fadeOut('fast');
                        $("#summery_div").removeClass("d-none")
                        $(".text_msg_content").text("Total Contacts: "+data["final_count"])
                    }
                    else if(data['updated_count'] >= 0){
                        $('#lead-phonebook-churn, #user-churn').val('')
                        $('#lead-phonebook-churn option, #user-churn option').remove()
                        $('#leadchurn-smbt-button').val()
                         $('.preloader').fadeOut('fast');
                         $("#summery_div").removeClass("d-none")
                         $(".text_msg_content").text("Total Contacts Updated: "+data["updated_count"])
                        $("#churn_list_form")[0].reset()
                        setTimeout(function() {
                            $('#LeadListModal').modal('hide');
                        }, 3000);
                    }
                    //     $('#LeadListModal').modal('hide');
                    //     $('#lead-phonebook-churn').val('')
                    //     $('#lead-phonebook-churn option').remove()
                    //     $('#leadchurn-smbt-button').val()
                    //     $('.preloader').fadeOut('fast');
                    //     showInfoToast("Updated Contacts" + ' ' + data['updated_count'] + "", 'top-right')
                },
                error: function(data) {
                    $('.preloader').fadeOut('fast');
                }
            });
        } else {
            $("#leadchurn-err-msg").text("Please select atleast one dispo....").removeClass("d-none")
            setTimeout(function() {
                $("#leadchurn-err-msg").addClass("d-none")
            }, 3000);
            return false;
        }
    }
});
$(document).on('change', '#paginate_by, #search_by', function() {
    var temp_search = $("#search_by").val()
    $("#search_by").val(temp_search.trim())

    $("#filter_form").submit()
})
$(document).on('change', '#column_name', function() {
    $("#search_by").val("")
    if ($(this).val() != "") {
        $("#search_by").removeClass("d-none")
    } else {
        $("#search_by").addClass("d-none")
        $("#filter_form").submit()
    }
})

// spaces block in fields
$('.noSpace').keyup(function() {
    this.value = this.value.replace(/\s/g, '');
});

$(document).on("keydown", ".blockfirstspace", function(evt) {
    var firstChar = $(".blockfirstspace").val()
    if (evt.keyCode == 32 && firstChar == "") {
        return false;
    }
});

pagination_vue = new Vue({
    el: '#pagination_vue',
    delimiters: ['${', '}'],
    data: {
        total_records: total_records,
        total_pages: total_pages,
        page: page,
        has_next: has_next,
        has_prev: has_prev,
        start_index:0,
        end_index:0,
    },
    methods: {
        changePage(value) {
            $('#page').val(value)
            get_pagination_data(value, false)
        }
    }
})

function get_pagination_data(page, refresh_cell = false) {
    $("#page").val(page)
    $("#refresh_cell").val(refresh_cell)
    if ($("#filter_form").length > 0) {
        custom_pagination_table.processing(true)
        var form = $("#filter_form")
        $.ajax({
            type: 'get',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: location.pathname,
            data: form.serialize(),
            success: function(data) {
                custom_pagination_table.clear()
                custom_pagination_table.rows.add(data['table_data']); // Add new data
                custom_pagination_table.columns.adjust().draw(false); // Redraw the DataTable
                pagination_vue.total_records = data['total_records']
                pagination_vue.total_pages = data['total_pages']
                pagination_vue.page = data['page']
                pagination_vue.has_next = data['has_next']
                pagination_vue.has_prev = data['has_prev']
                pagination_vue.start_index = data['start_index']
                pagination_vue.end_index = data['end_index']
                query_set_list = data["id_list"]
                if (select_all_checked == true) {
                    $('tbody input[type="checkbox"]:not(:checked)').trigger('click');
                    result = query_set_list
                }
                custom_pagination_table.columns.adjust().responsive.recalc();
            },
            error: function(data) {},
            complete: function(data){
                custom_pagination_table.processing(false)
            }
        });
    } else {
        $("#report_form").append('<input type="hidden" name="page" id="page" value="' + page + '">')
        if ($("#filter-report").length > 0) {
            $("#filter-report").click()
        }
    }
}

function get_pagination_data_phonebook(page, refresh_cell = false) {
    $("#page").val(page)
    $("#refresh_cell").val(refresh_cell)
    if ($("#filter_form").length > 0) {
        var form = $("#filter_form")
        $.ajax({
            type: 'get',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: location.pathname,
            data: form.serialize(),
            success: function(data1) {
                custom_pagination_table.rows().every(function(rowIdx, tableLoop, rowLoop) {
                    var current_ele = this
                    var data = this.data();
                    jQuery.grep(data1["table_data"], function(n, i) {
                        if (data["id"] == n["id"]) {
                            data["percentage"] = n["percentage"]
                            if ($.inArray(data["id"].toString(), result) != -1) {
                                data["checked"] = true
                            }
                            if("downloaded_file_name" in n){
                                data["downloaded_file_name"] = n["downloaded_file_name"]
                                data["downloaded_file_path"] = n["downloaded_file_path"]
                            }
                            if("download_actions" in n){
                                data["download_actions"] = n["download_actions"]
                            }
                            if("improper_file_name" in n){
                                data["improper_file_name"] = n["improper_file_name"]
                            }
                            data["last_updated_contact_count"] = n["last_updated_contact_count"]
                            current_ele.data(data)
                        }
                    })
                })
                $('#crm-list-table tr').each(function() {

                })
            },
            error: function(data) {}
        });
    } else {
        $("#report_form").append('<input type="hidden" name="page" id="page" value="' + page + '">')
        if ($("#filter-report").length > 0) {
            $("#filter-report").click()
        }
    }
}

function get_phonebook_status(key){
     $.ajax({
            type: 'get',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/CRM/phonebook/status/?key='+key+'&is_refresh='+is_refresh_lead_list,
            success: function(data1) {
                var phonebook_status = Object.keys(data1);
                for (i = 0; i < phonebook_status.length; i++) {
                    var key_phonebook = phonebook_status[i];
                    if(data1[''+key_phonebook+'']==='Completed'){
                        
                        $("#success-"+key_phonebook).html('<p class="text-success" id="success-' + key_phonebook + '">Completed</p>')

                    }else{
                        $("#success-"+key_phonebook).html("<div class='progress progress-lg mt-2'><div class='progress-bar bg-success' role='progressbar' style=\"width:" + data1[''+key_phonebook+''] + "%\" aria-valuenow=" + data1[''+key_phonebook+''] + "% aria-valuemin=\"0\" aria-valuemax=\"100\" id='progress-" + key_phonebook + "'>" + data1[''+key_phonebook+''] + "%</div>");
                        $('.sch-download , .file-download').click(function(){
                            $('.sch-download , .file-download').addClass('disabled')
                        });
                        $('.fa-undo-alt').click(function(){
                            $('.fa-undo-alt').removeClass('disabled')
                        });
                    }
                   
                }
                if('is_refresh' in data1){
                    if(data1['is_refresh']==true){
                        is_refresh_lead_list = true
                        var page = pagination_vue.page
                        refresh_cell_interval = get_pagination_data_phonebook(page, refresh_cell=false);

                    }else{
                        is_refresh_lead_list = false
                    }
                }else{
                    is_refresh_lead_list = false
                }
            },
            error: function(data) {}
        });
}

if ((location.pathname.indexOf("phonebook") != -1 && ! /\d/.test(location.pathname)) || (location.pathname.indexOf("download") != -1 && ! /\d/.test(location.pathname))) {
    status_key = 'phonebook'
    if(location.pathname.indexOf("download") != -1 && ! /\d/.test(location.pathname)){
        status_key = 'download'
    }
    get_phonebook_status(status_key)
    refresh_cell_interval = setInterval(
        function () { 
            get_phonebook_status(status_key) 
        }, 
    3000);

}else{
    try{
        clearInterval(refresh_cell_interval)
    }catch(err){

    }
    
}


if (location.pathname.indexOf("phonebook") != -1 && ! /\d/.test(location.pathname)) {
    if(pagination_vue){
        var page = pagination_vue.page
        refresh_cell_interval = get_pagination_data_phonebook(page, refresh_cell=false); 
    }
    
}

$(document).on('click', '.pagination_submit', function() {
    var page = $(this).attr("data-page")
    $("#page").val(page)
    if ($("#filter_form").length > 0) {
        var form = $("#filter_form")
        $.ajax({
            type: 'get',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: location.pathname,
            data: form.serialize(),
            success: function(data) {
                $(".append_table").html(data["data"])
                var user_table = $('.table')
                selective_datatable(user_table); //datatbale jquery
                if (select_all_checked == true) {
                    $('thead input[name="select_all"]').prop("checked", true)
                }
            },
            error: function(data) {}
        });
    } else {
        $("#report_form").append('<input type="hidden" name="page" id="page" value="' + page + '">')
        if ($("#filter-report").length > 0) {
            $("#filter-report").click()
        }
    }
})

//feedback time vaidation check
$(document).on('click', '#feedback-timer-checkbox', function() {
    if (this.checked == true) {
        $('#feedbacktime_div, #feedback-timer-checkbox').removeClass('d-none')
        $('#feedback-time').val('02:00')
    } else {
        $('#feedbacktime_div, #feedback-timer-checkbox').addClass('d-none')
        $('#feedback-time').val('')
    }
})

$('#query_modal').on('hidden.bs.modal', function(e) {
    css_query_vue.campaign_list = []
    css_query_vue.download_query_index = null
    $('#result_table').find('tr').not(":first").remove()
    $('#download_query_data').addClass('d-none')

})

// select2 multiple select component in vue
Vue.component('select2', {
    props: ['options', 'value'],
    template: '<select v-bind:name="name" class="form-control"></select>',
    mounted: function() {
        var vm = this
        $(this.$el)
            // init select2
            .select2({
                data: this.options
            })
            .val(this.value)
            .trigger('change')
            // emit event on change.
            .on('change', function() {
                if ($(this).val() != null) {
                    vm.$emit('input', $(this).val())
                    vm.$emit('blur', null)
                }
            })
    },
    watch: {
        value: function(value) {
            // update value
            if ([...value].sort().join(",") !== [...$(this.$el).val()].sort().join(",")) {
                $(this.$el)
                    .val(value)
                    .trigger('change')
            }
        },
        options: function(options) {
            // update options
            $(this.$el).select2({
                data: options
            })
        }
    },
    destroyed: function() {
        $(this.$el).off().select2('destroy')
    }
})

Vue.component('single-select', {
    props: ['options', 'value'],
    template: '#single_select_template',
    mounted: function() {
        var vm = this
        $(this.$el)
            // init select2
            .select2({
                data: this.options
            })
            .val(this.value)
            .trigger('change')
            // emit event on change.
            .on('change', function() {
                if ($(this).val() != null) {
                    vm.$emit('input', $(this).val())
                    vm.$emit('blur', null)
                    vm.$emit('where-change')
                }
            })
    },
    watch: {
        value: function(value) {
            // update value
            if (Array.isArray(value)){
                if (value[0] !== $(this.$el).val()) {
                    $(this.$el)
                    .val(value[0])
                    .trigger('change')
                }
            } else {
                if (value !== $(this.$el).val()) {
                    $(this.$el)
                    .val(value)
                    .trigger('change')
                }
            }
        },
        options: function(options) {
            // update options
            $(this.$el).select2({
                data: options
            })
        }
    },
    destroyed: function() {
        $(this.$el).off().select2('destroy')
    }
})
var css_query_vue = new Vue({
        el: '#add_more_query',
        delimiters: ["${", "}"],
        data: {
            css_id: null,
            query_list: [],
            orderCol_options: [],
            campaign_list: [],
            order_list: [],
            css_phonebook_list: [],
            selected_phonebook: [],
            phonebook_order: "",
            order: '',
            priority: '',
            status: 'Active',
            result: [],
            selected_campaign: "",
            selected_campaign_id : null,
            current_edit: null,
            current_edit_data: {},
            showForm: false,
            componentKey: 0,
            validated: 0,
            isDisabled: 0,
            condition: '',
            crm_fields_inquery: {},
            disable_campaign: false,
            disposition_list: [],
            contact_status_list : [],
            integer_fields:[],
            float_fields:[],
            download_query_index : null,
        },
        filters: {
            replaceQueue: function (value) {
                if (!value) return ''
                value = value.toString()
                return value.replace("AND status != 'Queued' ","")
            }
        },
        watch: {
            selected_campaign(value) {
                var vm = this
                vm.orderCol = []
                vm.orderCol_options = []
                vm.css_phonebook_list = []
                vm.componentKey += 1
                if (value != "" && value != "Select Campaign") {
                    $.ajax({
                        type: "post",
                        headers: {
                            "X-CSRFToken": csrf_token
                        },
                        url: '/api/get-crmfields-bycampaign/',
                        data: {
                            "campaign": value,
                            "css_id": vm.css_id
                        },
                        success: function(data) {
                            var option_list = []
                            vm.orderCol_options = []
                            vm.css_phonebook_list = []
                            $.each(data['phonebook_list'], function(k, ph_data) {
                                var ph_dict = {}
                                ph_dict['id'] = ph_data['id']
                                ph_dict['text'] = ph_data['name']
                                ph_dict['title'] = 'dsadasdjasdj'
                                css_query_vue.css_phonebook_list.push(ph_dict)
                            })
                            css_query_vue.integer_fields = data['integer_fields']
                            css_query_vue.float_fields = data['float_fields']
                            css_query_vue.orderCol_options = data['crm_db_fields']
                            css_query_vue.disposition_list = data['disposition_list']
                            css_query_vue.contact_status_list = data['status_list']
                            vm.selected_campaign_id = $('#campaign').select2('data')[0]['data-campaign-id']
                            vm.$nextTick(function() {
                                if (css_query_vue.current_edit != null) {
                                    var value = {...css_query_vue.result[css_query_vue.current_edit]
                                    }
                                    css_query_vue.query_list = value.css_fields
                                    css_query_vue.priority = value.priority
                                    css_query_vue.status = value.status
                                    css_query_vue.order_col = value.order_col
                                    css_query_vue.order_list = value.order_list
                                    css_query_vue.order = value.order
                                    css_query_vue.result.splice(css_query_vue.current_edit, 1)
                                    css_query_vue.current_edit = null
                                }
                            })
                        },
                        error: function(data) {

                            $("#campaign_error").html(`<span class="help-block form-error">${data["responseJSON"]["errors"]}</span>`)
                            setTimeout(function() {
                                $("#campaign_error").html("")
                            }, 3000);
                            vm.selected_campaign = ""
                            vm.selected_campaign_id = null
                        }
                    })
                }
            },
            order_list: {
                handler(val){
                    var vm = this
                    $.each(val, function(index,order_dict){
                        var m = order_dict.columns.filter(e => $.inArray(e, ['created_date', 'modified_date', 'priority','contact_status','disposition','last_dialed_date','dial_count','churncount']) == -1)
                        if('order_col' in vm.crm_fields_inquery && m.length ==0){
                            delete vm.crm_fields_inquery['order_col_'+index]
                        }else if(m.length>0){
                            vm.crm_fields_inquery['order_col_'+index] = m
                        }
                    })
                },
                deep:true,
                // var m = val.filter(e => $.inArray(e, ['created_date', 'modified_date', 'priority','contact_status','disposition','last_dialed_date','dial_count','churncount']) == -1)
                // if (m.length == 0) {
                //     delete this.crm_fields_inquery['order_col']
                // } else {
                //     this.crm_fields_inquery['order_col'] = m
                // }
            },
            result(val) {
                if (val.length > 0) {
                    this.disable_campaign = true
                } else {
                    this.disable_campaign = false
                }
            }
        },
        methods: {
            changeCondition() {
                if (this.condition == 'where') {
                    this.order_col = []
                    this.order = ""
                    this.query_list.push({
                        "value": "",
                        "operator": "",
                        "table_column": "",
                        "logical_operator": "",
                        "selected_date_col": "custom_val",
                        "selected_period": "days",
                        "arth_operation": "+",
                        "arth_value": 0,
                        "dispo_status_val":[''],
                        "datatype":'',
                    })
                    this.order_list = []
                    this.crm_fields_inquery = {}
                } else {
                    this.query_list = []
                    this.crm_fields_inquery = {}
                    this.order_col = []
                    this.order = ""
                    if(this.condition == 'order by'){
                        this.order_list.push({'columns':[],'order_type':'ASC'})
                    }else{
                        this.order_list = []
                    }
                }
            },
            checkCrmField(key, val) {
                if($('#where-column_'+key).select2('data')[0]['datatype']){
                    val.datatype = $('#where-column_'+key).select2('data')[0]['datatype'];
                    $('#value-column_'+key).removeClass('d-none')
                    $('#value-column_'+key).text( "Please enter valid input in "+val.datatype+' format only')
                }else{
                    val.datatype = ''
                    $('#value-column_'+key).addClass('d-none')
                }
                if ($.inArray(val.table_column, ['created_date', 'modified_date','priority','contact_status','disposition','last_dialed_date','dial_count','churncount']) == -1) {
                    this.crm_fields_inquery[key] = val.table_column
                    val.selected_date_col = 'custom_val'
                    val.operator = ''
                } else if($.inArray(val.table_column, ['priority','dial_count','churncount']) != -1) {
                    val.selected_date_col = 'custom_val'
                    val.operator = ''
                } else {
                    delete this.crm_fields_inquery[key]
                    val.selected_date_col = 'selectdp'
                    val.operator = ''
                }
            },
            addCss() {
                if (this.selected_campaign == "") {
                    $("#campaign_error").html(`<span class="help-block form-error">Please select campaign</span>`)
                } else {
                    this.showForm = true
                }
            },
            removeCss(cssId) {
                this.query_list.splice(cssId, 1)
                if (this.query_list.length == cssId) {
                    this.query_list[cssId - 1].logical_operator = ''
                }
            },
            addquerysection(index, value) {
                var vm = this
                if ($.inArray(value, ['OR', 'AND', 'CAND', 'COR']) != -1) {
                    if (Object.keys(vm.query_list).length == parseInt(index) + 1) {
                        vm.order_col = []
                        vm.order = ''
                        vm.order_list = []
                        Object.keys(vm.crm_fields_inquery).filter(function(val,index){
                            if (val.includes('order_col')){
                                delete vm.crm_fields_inquery[val]
                            }
                        })
                        vm.query_list.push({
                            "value": "",
                            "operator": "",
                            "table_column": "",
                            "logical_operator": "",
                            "selected_date_col": "custom_val",
                            "selected_period": "day",
                            "arth_operation": "+",
                            "arth_value": 0,
                            "dispo_status_val":[''],
                        })
                    }
                } else {
                    vm.query_list.splice(parseInt(index) + 1)
                    if (value =='') {
                        vm.order_col = []
                        vm.order = ''
                        vm.order_list = []
                        Object.keys(vm.crm_fields_inquery).filter(function(val,index){
                            if (val.includes('order_col')){
                                delete vm.crm_fields_inquery[val]
                            }
                        })
                    } else {
                        vm.order_list.push({'columns':[],'order_type':'ASC'})
                    }
                }
            },
            addOrderBy(){
                var m  = this.order_list.filter(val => val.columns.length==0)
                if (m.length > 0)
                    return
                this.order_list.push({'columns':[],'order_type':'ASC'})
            },
            removeOrderBy(index){
                var vm = this
                var temp = {}
                for (i=index; i<vm.order_list.length;i++){
                    if ('order_col_'+(i+1) in vm.crm_fields_inquery){
                        temp['order_col_'+i] = [...vm.crm_fields_inquery['order_col_'+(i+1)]]
                        delete vm.crm_fields_inquery['order_col_'+(i+1)]
                    }
                }
                this.order_list.splice(index, 1)
                delete vm.crm_fields_inquery['order_col_'+index]
            },
            createQuery() {
                var vm = this
                var form = $('#css-create-form')
                let error = false
                if (form.isValid() == true) {
                    // css_query_vue.isDisabled = 1
                    var result_dict = {}
                    css_query_vue.componentKey += 1
                    $('#query_table').find(".dataTables_empty").parents('tbody').empty();

                    if (Object.keys(vm.crm_fields_inquery).length === 0) {
                        var sql_query = `SELECT *, id as contact_id FROM crm_contact WHERE campaign='${vm.selected_campaign}'`
                    } else {
                        var sql_query = `SELECT crm_contact.*, crm_contact.id as contact_id FROM crm_contact WHERE campaign='${vm.selected_campaign}'`
                    }
                    if (vm.selected_phonebook.length > 1) {
                        if (vm.phonebook_order == 'include') {
                            sql_query = `${sql_query} AND phonebook_id IN ( select id from crm_phonebook where status='Active' AND campaign='${vm.selected_campaign_id}' AND id IN (${vm.selected_phonebook.toString()} ))`
                        } else if (vm.phonebook_order == 'exclude') {
                            sql_query = `${sql_query} AND phonebook_id NOT IN ( select id from crm_phonebook where status='InActive' AND id IN (${vm.selected_phonebook.toString()} ))`
                        }
                    } else if (vm.selected_phonebook.length == 1) {
                        if (vm.phonebook_order == 'include') {
                            sql_query = `${sql_query} AND phonebook_id = ( select id from crm_phonebook where status='Active' AND id = ${vm.selected_phonebook.toString()})`
                        } else if (vm.phonebook_order == 'exclude') {
                            sql_query = `${sql_query} AND phonebook_id != ${vm.selected_phonebook.toString()} AND phonebook_id IN ( select id from crm_phonebook where status='Active' AND campaign='${vm.selected_campaign_id}')`
                        }
                    } else {
                        sql_query = `${sql_query} AND phonebook_id IN ( select id from crm_phonebook where status='Active' AND campaign='${vm.selected_campaign_id}')`
                    }
                    sql_query = `${sql_query} AND status != 'Queued'`
                    if (vm.condition == 'where') {
                        sql_query = `${sql_query} AND ( `
                    } else if (vm.condition == 'order by') {
                        sql_query = `${sql_query} order by `
                    }
                    sql_where = ''
                    previous_logical_operator = ''
                    $.each(vm.query_list, function(index, query_dict) {
                        if (query_dict.logical_operator == 'CAND' || query_dict.logical_operator == 'COR') {
                            if ($.inArray(previous_logical_operator, ['CAND','COR']) == -1 ){
                                sql_query = `${sql_query} (`
                            }
                        }
                        if ($.inArray(query_dict.table_column, ['created_date', 'modified_date', 'priority','disposition','contact_status','last_dialed_date','dial_count','churncount']) == -1) {
                            var cf_array = query_dict.table_column.split(":")
                            var column_dt_type = ''
                            if(query_dict.datatype=='datetimefield' || query_dict.datatype=='datefield'){
                                column_dt_type = '::timestamp'
                                if(moment(query_dict.value,'YYYY-MM-DD', true).isValid()===false){
                                    query_dict.value = ''
                                    $('#value-field_value'+index).val('')
                                    $('#value-column_'+index).removeClass('d-none')
                                    $('#value-column_'+index).text( "Please enter valid input in "+query_dict.datatype+' yyyy-mm-dd format only')
                                    error = true
                                    return false
                                }else{
                                    $('#value-column_'+index).addClass('d-none')
                                    $('#value-field_value'+index).val(query_dict.value)
                                }
                            }else if(query_dict.datatype=='integer'){
                                column_dt_type = '::BIGINT'
                                if(/^[0-9,]*$/.test(query_dict.value)==false){
                                    query_dict.value = ''
                                    $('#value-field_value'+index).val('')
                                    $('#value-column_'+index).removeClass('d-none')
                                    $('#value-column_'+index).text( "Please enter valid input in "+query_dict.datatype+' format only')
                                    error = true
                                    return false
                                }else{
                                    $('#value-column_'+index).addClass('d-none')
                                    $('#value-field_value'+index).val(query_dict.value)
                                }
                            }
                            else if(query_dict.datatype=='float'){
                                column_dt_type = '::float'
                                if(/^[0-9,.]*$/.test(query_dict.value)==false){
                                    query_dict.value = ''
                                    $('#value-field_value'+index).val('')
                                    $('#value-column_'+index).removeClass('d-none')
                                    $('#value-column_'+index).text( "Please enter valid input in "+query_dict.datatype+' format only')
                                    error = true
                                    return false
                                }else{
                                    $('#value-column_'+index).addClass('d-none')
                                    $('#value-field_value'+index).val(query_dict.value)
                                }
                            }else if(query_dict.datatype=='timefield'){
                                column_dt_type = '::time'
                                if(moment(query_dict.value, 'HH:mm:ss', true).isValid()===false){
                                    query_dict.value = ''
                                    $('#value-field_value'+index).val('')
                                    $('#value-column_'+index).removeClass('d-none')
                                    $('#value-column_'+index).text( "Please enter valid input in "+query_dict.datatype+' format only')
                                    error = true
                                    return false
                                    // form.isValid()
                                }else{
                                    $('#value-column_'+index).addClass('d-none')
                                    $('#value-field_value'+index).val(query_dict.value)
                                }
                            }
                            crm_field_query = `crm_contact.customer_raw_data -> '${cf_array[0]}' ->> '${cf_array[1]}'`
                            if (query_dict.operator == "IN" || query_dict.operator == 'NOT IN') {
                                var in_options = query_dict.value.split(',')
                                $.each(in_options, function(index, value) {
                                    in_options[index] = "'" + value + "'"
                                })
                                crm_field_query = `(${crm_field_query})${column_dt_type} ${query_dict.operator} ( ${in_options.join(',')} )`
                            } else if (query_dict.operator == "LIKE") {
                                crm_field_query = `${crm_field_query} LIKE '%%${query_dict.value}%%'`
                            } else if ($.inArray(query_dict.operator, ['ISNULL', 'IS NOT NULL']) == -1)  {
                                if (query_dict.selected_date_col == "custom_val") {
                                    crm_field_query = `(${crm_field_query})${column_dt_type} ${query_dict.operator} '${query_dict.value}'${column_dt_type}`
                                } else if (query_dict.selected_date_col == "selectdp") {
                                    if(column_dt_type ==''){
                                        crm_field_query = `NULLIF(${crm_field_query},'')::timestamp ${query_dict.operator} '${query_dict.value}'`
                                    }else{
                                        crm_field_query = `NULLIF(${crm_field_query},'')::timestamp ${query_dict.operator} '${query_dict.value}'::timestamp`
                                    }
                                    
                                } else {
                                    if(column_dt_type ==''){
                                        crm_field_query = `NULLIF(${crm_field_query},'')::date ${query_dict.operator} current_date ${query_dict.arth_operation} interval '${query_dict.arth_value} ${query_dict.selected_period}'`
                                    }else{

                                        crm_field_query = `${crm_field_query} ${query_dict.operator} current_date ${query_dict.arth_operation} interval '${query_dict.arth_value} ${query_dict.selected_period}'`
                                    }
                                }
                            } else if (query_dict.operator == 'ISNULL' || query_dict.operator == 'IS NOT NULL') {
                                crm_field_query = `${crm_field_query} ${query_dict.operator}`
                            }
                            sql_where = `${sql_where} ${crm_field_query}`
                        } else if ($.inArray(query_dict.table_column, ['disposition','contact_status']) != -1) {
                            if (query_dict.table_column == 'contact_status'){
                                sql_where = `${sql_where} crm_contact.status`
                            } else {
                                sql_where = `${sql_where} crm_contact.${query_dict.table_column}`
                            }
                            if (query_dict.operator == "IN" || query_dict.operator == 'NOT IN') {
                                var in_options = [...query_dict.dispo_status_val]
                                $.each(in_options, function(index, value) {
                                    if (value == 'blank') {
                                        in_options[index] = "''"
                                    } else {
                                        in_options[index] = `'${value}'`
                                    }
                                })
                                sql_where = `${sql_where} ${query_dict.operator} ( ${in_options.join(',')} ) `
                            } else if ($.inArray(query_dict.operator, ['ISNULL', 'IS NOT NULL']) == -1)  {
                                if (query_dict.dispo_status_val == 'blank') {
                                    sql_where = `${sql_where} ${query_dict.operator} ''`
                                } else{
                                    sql_where = `${sql_where} ${query_dict.operator} '${query_dict.dispo_status_val[0]}'`
                                }
                            } else if (query_dict.operator == 'ISNULL' || query_dict.operator == 'IS NOT NULL')  {
                                sql_where = `${sql_where} ${query_dict.operator}`
                            }
                        } else if($.inArray(query_dict.table_column, ['priority','dial_count','churncount']) != -1) {
                            sql_where = `${sql_where} crm_contact.${query_dict.table_column}`
                            if (query_dict.operator == "IN" || query_dict.operator == 'NOT IN') {
                                var in_options = query_dict.value.split(',')
                                $.each(in_options, function(index, value) {
                                    in_options[index] = "'" + value + "'"
                                })
                                sql_where = `${sql_where} ${query_dict.operator} ( ${in_options.join(',')} )`
                            } else if (query_dict.operator == "LIKE") {
                                sql_where = `${sql_where} LIKE '%%${query_dict.value}%%'`
                            } else if ($.inArray(query_dict.operator, ['ISNULL', 'IS NOT NULL']) == -1)  {
                                sql_where = `${sql_where} ${query_dict.operator} '${query_dict.value}'`
                            } else if (query_dict.operator == 'ISNULL' || query_dict.operator == 'IS NOT NULL')  {
                                sql_where = `${sql_where} ${query_dict.operator}`
                            }
                        } else {
                            sql_where = `${sql_where} ${query_dict.table_column}::date ${query_dict.operator}`
                            if (query_dict.selected_date_col == "custom") {
                                sql_where = sql_where + " current_date " + query_dict.arth_operation + " interval '" +
                                    query_dict.arth_value + " " + query_dict.selected_period + "' "
                            } else {
                                sql_where = sql_where + "'" + query_dict.value + "' "
                            }
                        }
                        if (query_dict.logical_operator == 'order by' | query_dict.logical_operator == '') {
                            if (previous_logical_operator == 'CAND' | previous_logical_operator == 'COR'){
                                sql_where = sql_where + ')) ' + query_dict.logical_operator
                            } else {
                                sql_where = sql_where + ') ' + query_dict.logical_operator
                            }
                        } else if(query_dict.logical_operator == 'CAND' | query_dict.logical_operator == 'COR') {
                            sql_where = sql_where + ' ' + query_dict.logical_operator.substring(1) + ' '
                        } else {
                            if (previous_logical_operator == 'CAND' | previous_logical_operator == 'COR'){
                                sql_where = sql_where + ') ' + query_dict.logical_operator + ' '
                            } else {
                                sql_where = sql_where + ' ' + query_dict.logical_operator + ' '
                            }
                        }
                        previous_logical_operator = query_dict.logical_operator
                    })
                    if (error){
                        return false
                    }
                    sql_query = sql_query + sql_where
                    var order_query = ''
                    if (vm.order_list.length > 0){
                        $.each(vm.order_list, function(index, order_col_dict){
                            if (index > 0) {
                                order_query = order_query + ", "
                            }
                            if (order_col_dict.columns.length > 0){
                                $.each(order_col_dict.columns, function(col_index,order_column){
                                    if (col_index > 0) {
                                        order_query = order_query + ", "
                                    }
                                    if ($.inArray(order_column, ['created_date', 'modified_date','priority','disposition','contact_status','last_dialed_date','dial_count','churncount']) == -1) {
                                        var order_cf_arr = order_column.split(":")

                                        if($.inArray(order_column, vm.integer_fields) !=-1){
                                            order_query = order_query + " (crm_contact.customer_raw_data -> '" + order_cf_arr[0] + "'->>'" + order_cf_arr[1] + "')::BIGINT"
                                        }else if($.inArray(order_column, vm.float_fields) !=-1){
                                            order_query = order_query + " (crm_contact.customer_raw_data -> '" + order_cf_arr[0] + "'->>'" + order_cf_arr[1] + "')::float"
                                        }
                                        else{
                                            order_query = order_query + " crm_contact.customer_raw_data -> '" + order_cf_arr[0] + "'->'" + order_cf_arr[1] + "'"
                                        }

                                    } else {
                                        if (order_column == 'contact_status') {
                                            order_query = `${order_query} crm_contact.status`
                                        } else {
                                            order_query = `${order_query} crm_contact.${order_column}`
                                        }
                                    }
                                })
                                order_query = order_query + ' ' + order_col_dict.order_type
                            }
                        })
                    }
                    // if (vm.order_col.length > 0) {
                    //     $.each(vm.order_col, function(index, order_column) {
                    //         if (index > 0) {
                    //             order_query = order_query + ", "
                    //         }
                    //         if ($.inArray(order_column, ['created_date', 'modified_date','priority','disposition','contact_status','last_dialed_date','dial_count','churncount']) == -1) {
                    //             var order_cf_arr = order_column.split(":")

                    //             if($.inArray(order_column, vm.integer_fields) !=-1){
                    //                 order_query = order_query + " (crm_contactinfo.customer_raw_data -> '" + order_cf_arr[0] + "'->>'" + order_cf_arr[1] + "')::BIGINT"
                    //             }else{
                    //                 order_query = order_query + " crm_contactinfo.customer_raw_data -> '" + order_cf_arr[0] + "'->'" + order_cf_arr[1] + "'"
                    //             }

                    //         } else {
                    //             if (order_column == 'contact_status') {
                    //                 order_query = `${order_query} crm_contact.status`
                    //             } else {
                    //                 order_query = `${order_query} crm_contact.${order_column}`
                    //             }
                    //         }
                    //     })
                    //     order_query = order_query + ' ' + vm.order
                    // }
                    sql_query = sql_query + ' ' + order_query
                    vm.showForm = false
                    result_dict['query_string'] = sql_query
                    result_dict['priority'] = vm.priority
                    result_dict['status'] = vm.status
                    result_dict['condition'] = vm.condition
                    result_dict['css_fields'] = vm.query_list
                    result_dict['selected_phonebook'] = vm.selected_phonebook
                    result_dict['phonebook_order'] = vm.phonebook_order
                    result_dict['crm_fields_inquery'] = vm.crm_fields_inquery
                    result_dict['order'] = vm.order
                    result_dict['order_col'] = vm.order_col
                    result_dict['order_list'] = vm.order_list
                    if (vm.current_edit != null) {
                        vm.result.splice(vm.current_edit, 0, result_dict)
                    } else {
                        vm.result.push(result_dict)
                    }
                    vm.flushCssData()
                }
            },
            cancelQuery() {
                if (this.current_edit != null) {
                    this.result.splice(this.current_edit, 0, this.current_edit_data)
                }
                this.flushCssData()
            },
            deleteQuery(index) {
                this.result.splice(index, 1)
                if (this.result.length == 0) {
                    css_query_vue.validated = 0
                }
            },
            executeQuery(index) {
                var vm = this
                query_string = vm.result[index].query_string
                    // $('.preloader').fadeIn('fast');
                $.ajax({
                    type: 'post',
                    headers: {
                        "X-CSRFToken": csrf_token
                    },
                    url: '/CampaignManagement/check-query/',
                    data: {
                        'query_string': vm.$options.filters.replaceQueue(query_string)
                    },
                    success: function(data) {
                        $('#query_modal').modal('show');
                        $('#total_data_count').text(data['total_contact'])
                        $('#result_table').find('tr').not(":first").remove();
                        $.each(data['queryset'], function(key, value) {
                            $('#result_table').append("<tr>" +
                                "<td>" + value.id + "</td>" +
                                "<td>" + value.campaign + "</td>" +
                                "<td>" + value.phonebook + "</td>" +
                                "<td>" + value.user + "</td>" +
                                "<td>" + value.numeric + "</td>" +
                                "<td>" + value.status + "</td>" +
                                "</tr>")
                        })
                        if (data['queryset'].length > 0){
                            vm.download_query_index = index
                            $('#download_query_data').removeClass('d-none')
                        }
                    },
                    error: function(data) {
                        showDangerToast('error',data['responseJSON']['error'],'top-right')
                    }
                })
            },
            downloadQueryResult(index) {
                var vm = this
                query_string = vm.result[index].query_string
                    // $('.preloader').fadeIn('fast');
                $.ajax({
                    type: 'get',
                    headers: {
                        "X-CSRFToken": csrf_token
                    },
                    url: '/CampaignManagement/check-query/',
                    data: {
                        'query_string': vm.$options.filters.replaceQueue(query_string)
                    },
                    success: function(data) {
                       showSwal('dwnld-success-message', data["message"])
                    },
                    error: function(data) {
                    }
                })
            },
            SaveQuery() {
                if (this.result != '' && $('#css-create-form').isValid() == true) {
                    var url = '/CampaignManagement/css/create/'
                    var type = 'post'
                    if (this.css_id != null) {
                        url = `/CampaignManagement/css/${this.css_id}/`
                        type = 'put'
                    }
                    $.ajax({
                        type: type,
                        headers: {
                            "X-CSRFToken": csrf_token
                        },
                        url: url,
                        data: {
                            'raw_query': JSON.stringify(this.result),
                            'name': $('#name').val(),
                            'status': $('#status').val(),
                            'campaign': css_query_vue.selected_campaign
                        },
                        success: function(data) {
                            if (type == 'put') {
                                showSwal('success-message', 'Css Successfully Updated', '/CampaignManagement/css/')
                            } else {
                                showSwal('success-message', 'Css Successfully Created', '/CampaignManagement/css/')
                            }
                        },
                        error: function(data) {
                            console.log(data)
                            $("#css_name_error").html(`<span class="help-block form-error">
                            ${data["responseJSON"]["name"]}</span>`).addClass('has-error')
                            $("#css_name_error").parent().find('input').removeClass('valid').addClass('error')
                        }
                    })
                }
            },
            onEdit(index, value) {
                if (this.current_edit == null) {
                    this.showForm = true
                    css_query_vue.componentKey += 1
                    this.$nextTick(function() {
                        this.current_edit = index
                        var value = {...this.result[index]
                        }
                        this.current_edit_data = {...this.result[index]
                        }
                        this.query_list = value.css_fields
                        this.priority = value.priority
                        this.status = value.status
                        this.order_col = value.order_col
                        this.order_list = value.order_list
                        this.order = value.order
                        this.selected_phonebook = value.selected_phonebook
                        this.phonebook_order = value.phonebook_order
                        this.condition = value.condition
                        this.crm_fields_inquery = value.crm_fields_inquery
                        this.result.splice(index, 1)
                        this.isDisabled = 1
                    })
                }
            },
            flushCssData() {
                this.query_list = []
                this.priority = ''
                this.order_col = []
                this.order_list = []
                this.condition = ''
                this.selected_phonebook = []
                this.phonebook_order = ""
                this.componentKey += 1
                this.current_edit = null
                this.current_edit_data = {}
                this.showForm = false
            },
        },
    })
$('#download_query_data').click(function(){
    css_query_vue.downloadQueryResult(css_query_vue.download_query_index)
})
    //skill create vue js 
var skill_vue = new Vue({
    el: '#skilledrouting_vue',
    delimiters: ["${", "}"],
    data: {
        skilled_camp: [""],
        dial_numbers: ['default', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '*', '#'],
        dummy_labels: [],
        campaign: [],
        hash_key_val: '',
        star_key_val: '',
        skills_route: [{
            label: '',
            campaign: '',
        }],
        remove_camp: true,
    },
    watch: {
        skilled_camp() {
            this.remove_camp = this.skills_route.length > 1
        },
    },
    methods: {
        AddSkill(index, label) {
            let checkEmptyfield = this.skills_route.filter(field => field.label === '' || field.campaign === '')
            if (checkEmptyfield.length >= 1 && this.skills_route.length > 0)
                return
            this.skills_route.push({
                label: "",
                campaign: "",
                error: false
            })
        },
        RemoveSkill(index, label) {
            var vm = this
            if (vm.remove_camp) {
                var remove_dict = vm.skills_route.splice(index, 1)
                var temp_error = false
                $.each(vm.skills_route, function(index, val) {
                    if (remove_dict[0].label == val.label) {
                        if (temp_error == false) {
                            val.error = false
                            temp_error = true
                        } else {
                            val.error = true
                        }
                    }
                })
            }

        },
        onEditSkill(value) {
            var vm = this
            vm.skills_route = []
            $.each(value, function(key, val) {
                vm.skills_route.push({
                    label: key,
                    campaign: val,
                    error: false
                })
            })
        },
        selectNumber(event, index_val) {
            var vm = this
            if (event.target.value == 'default') {
                vm.skills_route.splice(index_val + 1, vm.skills_route.length)
                vm.skills_route[index_val].error = false
            } else {
                $.each(vm.skills_route, function(index, val) {
                    if (index != index_val) {
                        if (event.target.value == val.label) {
                            vm.skills_route[index_val].error = true
                            return false
                        } else {
                            val.error = false
                        }
                    } else {
                        vm.skills_route[index_val].error = false
                    }
                })
            }
        }
    }
})

function skill_data_update() {
    skill_dict = {}
    var audio_dict = {}
    audio_dict['welcome_file'] = $('#welcome_audio').val()
    $.each(skill_vue.skills_route, function(key, val) {
        skill_dict[val['label']] = val['campaign']
    })
    delete add_trunk_vue.group_trunk_list[0]["old_trunk"]
    delete add_trunk_vue.group_trunk_list[0]["options"]
    var trunk_list = add_trunk_vue.group_trunk_list[0]
    if(trunk_list["did_type"] == "single") {
        var did_val = [trunk_list["did"]]
        trunk_list["did"] = did_val
    }
    data = {
        'skill': JSON.stringify(skill_dict),
        'name': $('#skill_name').val(),
        'skill_id': JSON.stringify(trunk_list),
        'schedule': $('#schedule').val(),
        'status': $('#status').val(),
        'audio': JSON.stringify(audio_dict),
        'd_abandoned_camp': $('#d_abandoned_camp').val(),
        'skill_popup': $('#skill_popup').prop('checked'),
        'callback': $('#callback').val()
    }
}
var skill_create_form = $('#create-skilled-routing-form')
$('#create-skill-btn').click(function() {
    if (skill_create_form.isValid() == true) {
        skill_data_update()
        $.ajax({
            type: "post",
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/CampaignManagement/create/skilled/',
            data: data,
            success: function(data) {
                showSwal('success-message', 'Skill Successfully Created', '/CampaignManagement/skilled/')
            },
            error: function(data) {
                if (data["responseJSON"]["errors"]) {
                    $(".skill-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
                    setTimeout(function() {
                        $(".skill-err-msg").addClass("d-none")
                    }, 3000);
                }
            }
        })
    }
})
$('#css_order_by').change(function() {
    if ($(this).val() != "") {
        $('#css_order_div').removeClass('d-none')
    } else {
        $('#css_order_div').addClass('d-none')
    }
})
$('#edit-skill-btn').click(function() {
    var skill_edit_form = $('#create-skilled-routing-form-edit')
    var id = $('#skillmap-id').val()
    if (skill_edit_form.isValid() == true) {
        skill_data_update()
        $.ajax({
            type: "put",
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/CampaignManagement/skilled/' + id + '/',
            data: data,
            success: function(data) {
                showSwal('success-message', 'Skill Successfully Updated', '/CampaignManagement/skilled/')
            },
            error: function(data) {
                if (data["responseJSON"]["errors"]) {
                    $(".skill-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
                    setTimeout(function() {
                        $(".skill-err-msg").addClass("d-none")
                    }, 3000);
                }
            }
        })
    }
})

Vue.component('datepicker', {
    props: ['value', 'isRequired', 'name'],
    template: `<div class="input-group date datepicker p-0">
                <input type="text" class="form-control crm-form-control" placeholder="yyyy-mm-dd"
                :data-validation="[isRequired ? 'required' : '']">
                <span class="input-group-addon input-group-append">
                </span>
            </div>`,
    mounted: function() {
        var vm = this
        vm.$nextTick(function() {
            $(vm.$el)
                .datepicker({
                    enableOnReadonly: false,
                    todayHighlight: true,
                    autoclose: true,
                    format: "yyyy-mm-dd"
                });
            $(vm.$el).datepicker('update', this.value);
            $(vm.$el).on('changeDate', function(e) {
                vm.$emit('set-date', e.format("yyyy-mm-dd"))
                vm.$emit('blur', null)
            })
        })
    },
    watch: {
        value: function(value) {
            // update value
            $(this.$el).datepicker('update', value);
        }
    },
})

$('.import-jsondata').click(function() {
    var form = new FormData($('.import-json-form').get(0));
    var file_length = $('#import-file').get(0).files.length;
    if (file_length > 0) {
        if ($("#import-file").val().split('.').pop().toLowerCase() == 'json') {
            if ($(this).attr('id') == 'import-disposition-data') {
                url_form = '/api/import-dispo-jsondata/'
            }
            if ($(this).attr('id') == 'import-relation-data') {
                url_form = '/api/import-relation-jsondata/'
            }
            $.ajax({
                type: 'post',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: url_form,
                data: form,
                processData: false,
                contentType: false,
                beforeSend: function() {
                    $('.preloader').fadeIn('fast');
                },
                success: function(data) {
                    $('.preloader').fadeOut('fast');
                    if ("disposuccess" in data) {
                        showSwal('success-message', 'Imported Successfully ', '/CampaignManagement/Dispositions/')
                    }
                    if ("relationsuccess" in data) {
                        showSwal('success-message', 'Imported Successfully ', '/CampaignManagement/RelationTags/')
                    }
                    if ("error" in data) {
                        $("#error_message").text(data['error']).removeClass("d-none")
                        setTimeout(function() {
                            $("#error_message").addClass("d-none")
                        }, 3000);
                    }
                },
                error: function(data) {
                    $('.preloader').fadeOut('fast');
                    console.log(data)
                }
            })
        } else {
            $("#error_message").text("File format must be Json").removeClass("d-none")
            setTimeout(function() {
                $("#error_message").addClass("d-none")
            }, 3000);
        }
    } else {
        $("#error_message").text("Upload Json file").removeClass("d-none")
        setTimeout(function() {
            $("#error_message").addClass("d-none")
        }, 3000);
    }
})

$(document).on('change', '.import_dispo', function(e) {
    var parent_id = $(this).data("parent")
    $("#existing-dispo-" + parent_id).removeClass("d-none")

})

$(document).on('keyup','#dial_time_out', function(e) {
    var variable_value = $(this).val()
    $("#variables").val(`originate_timeout=${variable_value}`)
})

$(document).on('keyup','#variables', function(e) {
    var variable_value = $(this).val()
    $("#dial_time_out").val(variable_value.match(/\d+/))
})
$(document).on('blur','#dial_time_out', function(e) {
    var variable_value = $(this).val()
    if(variable_value == "") {
        $("#variables").val(`originate_timeout=25`)
        $(this).val(25)
    }
})

$(document).on('blur','#variables', function(e) {
    var variable_value = $(this).val()
    if (variable_value.match(/\d+/) == null) {
        $(this).val('originate_timeout=25')
        $("#dial_time_out").val(25)
    }
})



 //skill create vue js 
var wfh_vue = new Vue({
    el: '#wfh_vue',
    delimiters: ["${", "}"],
    data: {
        wfh_list: ['Redial','CallBack'],
        blockRemoval:true,
    },
    watch: {
    wfh_list () {
      this.blockRemoval = this.wfh_list.length <= 2
    }
  },
    methods: {
        AddSkill(index) {
            let checkEmptyfield = this.wfh_list.filter(field => field === '')
            if (checkEmptyfield.length >= 1 && this.wfh_list.length > 0)
                return
            this.wfh_list.push('')
        },
        RemoveSkill(index) {
            var vm = this
                var remove_dict = vm.wfh_list.splice(index, 1)
        },
    },
    //  mounted () {
    //     this.AddSkill()
    // },
})

//wfh checked 
$(document).on('click', '#wfh', function(){
    if($(this).prop("checked")){
        $('#wfh_vue').removeClass('d-none')
    }else{
        $('#wfh_vue').addClass('d-none')
    }
})
 
 //voice blaster options vue
 var voice_blaster_vue = new Vue({
    el: '#voice_blaster_vue',
    delimiters: ["${", "}"],
    data: {
        hasVoiceBlaster : false,
        vb_mode : null,
        vb_audio : '',
        hasDTMF : false,
        vb_dtmf: [],
        hasError : false,
        vb_call_after : 0,
        vb_audio_duration : 0,
    },
    watch: {
        hasError(val){
            if(val){
                $('.note-editor').css('border-color','#b74b47')
            }else{
                $('.note-editor').css('border-color','#a9a9a9')
            }
        },
        hasDTMF(val){
            if(val){
                if(this.vb_dtmf.length == 0){
                    this.addVBoptions()
                }
            }else{
                this.vb_dtmf = []
            }
        },
        vb_mode(val){
            if(val == 0){
                $(".hint2mention").summernote("code", `<p><br></p>`)
            } else {
                this.vb_audio = '';
                this.vb_audio_duration = 0;
            }
        }
    },
    methods: {
        addVBoptions(index){
            let checkEmptyfield = this.vb_dtmf.filter(field => field === '')
            if (checkEmptyfield.length >= 1 && this.vb_dtmf.length > 0)
                return
            this.vb_dtmf.push({
                'dispo':'',
                'is_sms':'',
            })
        },
        removeVBoptions(index) {
            var vm = this
            vm.vb_dtmf.splice(index, 1)
        },
    }
})

$("#sms_campaign_select").change(function() {
    var campaign_name = $(this).children('option:selected').text()
    var campaign_id = $(this).val();
    if ($(this).val() != "") {
        $.ajax({
            type: 'POST',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: '/SMSManagement/Sms-Template/get-crm-fields/',
            data: {
                "campaign_name": campaign_name,
                "campaign_id": campaign_id,
            },
            success: function(data) {
                var editorField_list = []
                $.each(data['contact_fields'], function(index, value) {
                    var editiorField_dict = {}
                    editiorField_dict['text'] = editiorField_dict['value'] = value
                    editorField_list.push(editiorField_dict)
                });
                if (tinymce.get('scriptEditor')) {
                    tinymce.remove('#scriptEditor');
                }
                addScriptEditior(editorField_list,height=100)
            },
            error: function(data) {
            }
        });
    }
    tinyMCE.activeEditor.setContent('');
})
$("#sms-template-submit-btn").click(function() {
    var sms_data= tinyMCE.get('scriptEditor').getContent();
    if (tinyMCE.get('scriptEditor').getContent({format : 'text'}).length > 150){
        $("#script-err-msg").removeClass("d-none").text("Msg length should be less than 150 characters")
        setTimeout(function(){ $("#script-err-msg").addClass("d-none") }, 3000);
        return false
    }
    $("#sms-template-data").val(sms_data)
    var template_form = $("#sms-template-create-form")

    if ($("#sms_template_id").val() != "") {
        var url = `/SMSManagement/Sms-Template/edit/${$("#sms_template_id").val()}/`
    }
    else {
        var url = '/SMSManagement/Sms-Template/create/'
    }

    if (template_form.isValid() == true ) {
        $.ajax({
            type: 'POST',
            headers: {"X-CSRFToken": csrf_token},
            url: '',
            data: template_form.serialize(),
            success: function (data) {
                if ($("#sms_template_id").val() != "") {
                    showSwal('success-message', 'Sms Template Successfully Updated', '/SMSManagement/sms-template/')
                }
                else {
                    showSwal('success-message', 'Sms Template Successfully Created', '/SMSManagement/sms-template/')
                }
            },
            error: function (data) {
                if (data["responseJSON"]["name"]){
                    $("#script-name-error").html(`<span class="help-block form-error">${data["responseJSON"]["name"]}</span>`).addClass("has-error")
                    $("#name").removeClass("valid").addClass("error")
                }
                if ("name" in data["responseJSON"]) {
                    $("#script-name-error").addClass("has-error").removeClass("d-none").html(
                        '<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>')
                    setTimeout(function(){ $("#script-name-error").addClass("d-none") }, 3000);
                }
                
            }
        });
    }
})
$('[name="template_type"]').change(function(){
    if ($(this).val() == 0) {
        $("#sms_campaign_select").val("").trigger("change")
        $(".camp_required").addClass("d-none")
        $("#sms_campaign_select").removeAttr("data-validation")
        $("#sms_template_error").addClass("d-none").text("")
        $("#camp_div").addClass("d-none")
    }
    else{
        $(".camp_required").removeClass("d-none")   
        $("#sms_campaign_select").attr("data-validation","required")
        $("#sms_template_error").removeClass("d-none")
        $("#camp_div").removeClass("d-none")
    }
})
$(".sample_sms_template").click(function() {
    var file_type = ""
    if ($(this).hasClass("csv")) {
        file_type = "csv"
    } else {
        file_type = "xls"
    }
    var campaign_name = $('#sms_template_campaign :selected').val()
    if (campaign_name =="") {
        campaign_name = "dummy"
    }
    var url = `/SMSManagement/get-sample-template/${campaign_name}/${file_type}/`
    $(this).attr("href", url)
})
can_reload = false
$("#uploade-sms-template").click(function() {
    var data = new FormData($('#sms-template-upload-form').get(0));
    if($('#sms-template-upload-form').isValid()){
        $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            cache: false,
            processData: false,
            contentType: false,
            url: $('#sms-template-upload-form').attr('action'),
            data: data,
            beforeSend: function() {
                $('.preloader').fadeIn('fast');
            },
            success: function(data) {
                $('.preloader').fadeOut('fast');
                if("incorrect_file" in data) {
                    $("#improper-data").attr("href",data["incorrect_file"]).removeClass("d-none")
                    $("#improper-data .msg").text(data["incorrect_msg"])
                    if("correct_msg" in data) {
                        $("#upload-file-msg").text(data["correct_msg"])
                        $("#proper-data").removeClass("d-none")
                        can_reload = true
                    }

                }
                else {
                    showSwal('success-message', 'SMS Templates Successfully Updated')
                }
                $(".dropify-clear").click()
                $("#uploade-sms-template").addClass("d-none")
                
            },
            error: function(data) {
                $('.preloader').fadeOut('fast');
                $("#upload-file-error").text(data['responseText']).removeClass("d-none")
                setTimeout(function() {
                    $("#upload-file-error").addClass("d-none")
                }, 3000);
            }
        });
    }
});

$("#upload-holidays").click(function() {
    var data = new FormData($('#holidays-upload-form').get(0));
    if($('#holidays-upload-form').isValid()){
        $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            cache: false,
            processData: false,
            contentType: false,
            url: $('#holidays-upload-form').attr('action'),
            data: data,
            beforeSend: function() {
                $('.preloader').fadeIn('fast');
            },
            success: function(data) {
                $('.preloader').fadeOut('fast');
                if("incorrect_file" in data) {
                    $("#improper-data").attr("href",data["incorrect_file"]).removeClass("d-none")
                    $("#improper-data .msg").text(data["incorrect_msg"])
                    if("correct_msg" in data) {
                        $("#upload-file-msg").text(data["correct_msg"])
                        $("#proper-data").removeClass("d-none")
                        can_reload = true
                    }

                }
                else if("empty_file" in data){
                    $('.preloader').fadeOut('fast');
                    $("#upload-file-error").text(data['empty_file']).removeClass("d-none")
                    setTimeout(function() {
                        $("#upload-file-error").addClass("d-none")
                    }, 3000);
                }
                else {
                    showSwal('success-message', 'Holidays Successfully Uploaded')
                }
                $(".dropify-clear").click()
                $("#upload-holidays").addClass("d-none")
                
            },
            error: function(data) {
                $('.preloader').fadeOut('fast');
                $("#upload-file-error").text(data['responseText']).removeClass("d-none")
                setTimeout(function() {
                    $("#upload-file-error").addClass("d-none")
                }, 3000);
            }
        });
    }
});


$("#sms_trigger_on, #email_trigger_on").change(function(){
    if($(this).val() == "1") {
        $("#disposition_div").removeClass("d-none")
    }
    else{
        $("#disposition").val("").trigger("change")
        $("#disposition_div").addClass("d-none")   
    }
})
$("#sms-gateway-submit-btn").click(function(){
    var form = $("#sms-gateway-create-form")
    var url = "/SMSManagement/Sms-Gateway/create/"
    if ($("#sms_gateway_id").val() != "") {
        url = `/SMSManagement/Sms-Gateway/edit/${$("#sms_gateway_id").val()}/`
    }
    if(form.isValid()) {
        $.ajax({
            type: 'post',
            headers: {"X-CSRFToken": csrf_token},
            url: url,
            data: form.serialize(),
            success: function (data) {
                if($("#sms_gateway_id").val() !="") {
                    showSwal('success-message', 'SMS Gateway Successfully Updated', '/SMSManagement/gateway-settings/')
                }
                else {
                    showSwal('success-message', 'SMS Gateway Successfully Created', '/SMSManagement/gateway-settings/')   
                }
            },
            error: function (data) {
                if('name' in data["responseJSON"]){
                    $("#name").removeClass('valid').addClass('error');
                    $("#gateway-name-error").addClass("has-error").html(
                        '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass("d-none")
                    setTimeout(function() {
                        $("#gateway-name-error").addClass("d-none")
                    }, 3000);
                }
            }
        })
    }
    
})

$("#email-gateway-submit-btn").click(function(){
    var form = $("#email-gateway-create-form")
    var url = "/EmailManagement/EmailGateway/create/"
    if ($("#email_gateway_id").val() != "") {
        url = `/EmailManagement/EmailGateway/edit/${$("#email_gateway_id").val()}/`
    }
    if(form.isValid()) {
        $.ajax({
            type: 'post',
            headers: {"X-CSRFToken": csrf_token},
            url: url,
            data: form.serialize(),
            success: function (data) {
                if($("#email_gateway_id").val() !="") {
                    showSwal('success-message', 'Email Gateway Successfully Updated', '/EmailManagement/EmailGateway/')
                }
                else {
                    showSwal('success-message', 'Email Gateway Successfully Created', '/EmailManagement/EmailGateway/')   
                }
            },
            error: function (data) {
                if('name' in data["responseJSON"]){
                    $("#name").removeClass('valid').addClass('error');
                    $("#gateway-name-error").addClass("has-error").html(
                        '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass("d-none")
                    setTimeout(function() {
                        $("#gateway-name-error").addClass("d-none")
                    }, 3000);
                }
            }
        })
    }
    
})

$('[name="gateway_mode"]').change(function(){
    if ($(this).val() == 0) {
        $("#whats_app_gateway_div").addClass("d-none")
        $("#sms_gateway_div").removeClass("d-none")
    }
    else{
      $("#whats_app_gateway_div").removeClass("d-none")
      $("#sms_gateway_div").addClass("d-none")
    }
})
//Thirdparty Api Modules Js 

$(document).on('click','#create-thirdparty-btn,#edit-thirdparty-btn ', function(){
     var current_element = $(this)
    var api_mode_method = {}
      var mode_selected = $('#api_mode_select').val() 
    api_mode_method[mode_selected] = $('#api_weburl').val() 
    api_mode_method['parameters'] = {}
    $.each($('#api_parameters').select2('data'), function(index, val) {
        api_mode_method['parameters'][val['text']] = val['id']
    })
    $('#weburl').val(JSON.stringify(api_mode_method))
    $('#dynamic_api').val($('#dynamic_api').prop('checked'))
    $('#click_url').val($('#click_url').prop('checked'))
    var  url =  '/CampaignManagement/third-party-api/create/'
    var form_data = $('#thirdparty-create-form').serialize()
    var form = $("#thirdparty-create-form")
     if ($(this).hasClass("edit-thirdparty-btn")) {
        url = '/CampaignManagement/third-party-api/' + thirdparty_id + '/'
        var form_data = $('#thirdparty-edit-form').serialize()
        var form = $("#thirdparty-edit-form")
    }

    if(/^(http|https|ftp):\/\/[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/i.test($("#api_weburl").val())==false){
        $("#api_weburl").val('')
    } 

    if(form.isValid()=== true){   
      $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url:url ,
            data: form_data,
            success: function(data) {
            if (current_element.hasClass("edit-thirdparty-btn")) {
                showSwal('success-message', 'Thirdparty Crm Updated Successfully', '/CampaignManagement/third-party-api/')
            }else{
                showSwal('success-message', 'Thirdparty Crm Created Successfully', '/CampaignManagement/third-party-api/')
                }
            },
            error:function(data){
              if (data['responseJSON']['name']){
                    $("#thirdparty_name_exist").html(`<span class="help-block form-error">${data['responseJSON']['name']}</span>`).addClass("has-error")
                    $("#thirdparty_name_exist").removeClass("valid").addClass("error")                  
                }
                 if (data['responseJSON']['campaign']){
                    $("#camp_exists").html(`<span class="help-block form-error">${data['responseJSON']['campaign']}</span>`).addClass("has-error")
                    $("#camp_exists").removeClass("valid").addClass("error")                  
                }
            }
        })
    }
})

$(document).on('change','#api_campaign_crm,#api_campaign_vb',function(){
    var model_name = $(this).prop('id') 
    if (model_name == 'api_campaign_crm'){ 
        var camp_id = $('#api_campaign_crm option:selected').val()
        var camp_name = $.trim($('#api_campaign_crm option:selected').text())
        var select_length = $('#api_campaign_crm option:selected').length;
    }else{
         var camp_id = $('#api_campaign_vb option:selected').val()
        var camp_name = $.trim($('#api_campaign_vb option:selected').text())
        var select_length = $('#api_campaign_vb option:selected').length;
    }
    if(select_length <= 1){
        if($("#api_campaign_vb option").hasClass('common')){
            $("#api_campaign_vb option").removeClass('common')
        }
        $.ajax({
             type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url:'/api/check-api-crm-campaings/',
            data:{'camp_id':camp_id,"camp_name":camp_name,'model_name':model_name},
            success:function(data){
            if('assigned' in data){
                $("#camp_exists").text(data['assigned']).removeClass("d-none")
                        setTimeout(function() {
                            $("#camp_exists").addClass("d-none")
                        }, 3000); 
            }
            vb_crm_data = data['crm_field']
            $('#api_parameters').html("")
            if(select_length != 0){ 
                 var user_info = ['user_id','username','user_extension','campaign_id', 'campaign_name']
                    $.each(user_info,function(index,val){
                       $('#api_parameters').append("<option value="+val+">"+val+"</option>")
                    })
             }
              if('camp_ids' in data){
                $.each(data['crm_field'],function(index,val){
                   $('#api_parameters').append("<option value="+index+">"+val+"</option>")
                })
                if(model_name == 'api_campaign_crm'){  
                    $.each(data['camp_ids'], function(index,val){
                        $("#api_campaign_crm option[value='"+val+"']").addClass('common')
                        // if(data['camp_ids'].indexOf(parseInt($('#api_campaign option').val())) != -1 ){
                        // }
                    })
                }else{
                    $.each(data['camp_ids'], function(index,val){
                        $("#api_campaign_vb option[value='"+val+"']").addClass('common')
                        // if(data['camp_ids'].indexOf(parseInt($('#api_campaign option').val())) != -1 ){
                        // }
                    })
                }
            }   
            },
            error:function(data){

            }
        })  
    }else{
        if(model_name == 'api_campaign_crm'){    
            $.each($(this).val(),function(index,val){
               if(!$("#api_campaign_crm option[value='" + val + "']").hasClass('common')){
                    $("#api-camp-error").text("This Campign Crm fields are diffrent cant access").removeClass("d-none")
                            setTimeout(function() {
                                $("#api-camp-error").addClass("d-none")
                            }, 3000); 
                    $("#api_campaign_crm option[value='" + val + "']").prop("selected", false).trigger("change")
                   }
            })
        }else{
            $.each($(this).val(),function(index,val){
               if(!$("#api_campaign_vb option[value='" + val + "']").hasClass('common')){
                    $("#api-camp-error").text("This Campign Crm fields are diffrent cant access").removeClass("d-none")
                            setTimeout(function() {
                                $("#api-camp-error").addClass("d-none")
                            }, 3000); 
                    $("#api_campaign_vb option[value='" + val + "']").prop("selected", false).trigger("change")
                   }
            })

        }
    }
})

$(document).on('click', '#dynamic_api', function() {
    if(this.checked == true){
        $('#api_parameters_div').removeClass('d-none')
    }else{
        $('#api_parameters_div').addClass('d-none')
       $('#api_parameters').val('').trigger('change')
    }
})
// ends Thirdparty Api Modules Js 
 
// Voice Blaster js code goes here 
const voiceblasterdata =() =>{
    var vb_data = {};
    var vb_dtmf = {};
    if(voice_blaster_vue.vb_mode == '1'){
        if($($('.hint2mention').summernote('code')).text().trim() == ""){
            valid = false
            voice_blaster_vue.hasError = true
        } else {
            voice_blaster_vue.hasError = false
        }
    }
    if($('.hint2mention').length > 0){
        vb_data['vb_speech'] = $($('.hint2mention').summernote('code')).text().trim()
    }else{
        vb_data['vb_speech'] = ''
    }
    vb_data['vb_crm_fields'] = vb_crm_fields
    vb_data['hasDTMF'] = voice_blaster_vue.hasDTMF
    vb_data['vb_call_after'] = voice_blaster_vue.vb_call_after
    vb_data['vb_audio_duration'] = voice_blaster_vue.vb_audio_duration
    $.each(voice_blaster_vue.vb_dtmf, function(index,value){
        if(value){
            if(index+1 == 10){
                vb_dtmf[0] = value
            } else {
                vb_dtmf[index+1] = value
            }
        }
    })
    vb_data['vb_dtmf'] = vb_dtmf
    $('#voice_blaster').val($('#voice_blaster').prop('checked'))
    $('#vb_data').val(JSON.stringify(vb_data))

}


$(document).on('click','#create-voiceblaster-btn,#edit-voiceblaster-btn' ,function(){
    voiceblasterdata()
    var current_element = $(this)
    var form = $('#create-voiceblaster-form')
    var url = "/CampaignManagement/voiceblaster/create/"
    var form_serializer = $('#create-voiceblaster-form').serialize()
    if (current_element.hasClass('edit-voiceblaster-btn')){
        form =  $('#edit-voiceblaster-form')
        url = "/CampaignManagement/voiceblaster/"+ vb_id +"/"
        form_serializer = $('#edit-voiceblaster-form').serialize()
    }
    if(form.isValid()){ 
        $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url:url,
            data:form_serializer,
            success:function(data){
              if (current_element.hasClass("edit-voiceblaster-btn")) {
                showSwal('success-message', 'Campaign Updated Successfully', '/CampaignManagement/voiceblaster/')
            }else{
                showSwal('success-message', 'Campaign Create Successfully', '/CampaignManagement/voiceblaster/')
                }
            },
            error:function(data){
                if (data['responseJSON']['name']){
                    $("#vb_name_exist").html(`<span class="help-block form-error">${data['responseJSON']['name']}</span>`).addClass("has-error")
                    $("#vb_name_exist").removeClass("valid").addClass("error")                  
                }
                 if (data['responseJSON']['campaign']){
                    $("#camp_exists").html(`<span class="help-block form-error">${data['responseJSON']['campaign']}</span>`).addClass("has-error")
                    $("#camp_exists").removeClass("valid").addClass("error")                  
                }
            },
        })
    }
})
// uplod contacts to delete starts here
$("#uploaded-delete-contactfile").click(function(e) {
    $("#uploaded-delete-contactfile").val("")
    $(".dropify-clear").click()
    $("#submit-uploaded-file, #show_summery").addClass("d-none")
    $(".error_text").addClass("d-none")
    $("#summery_div").addClass("d-none")
    // $("#submit-uploaded-file").removeClass("d-none")
})

$("#uploaded-delete-contactfile").change(function(e) {
    var fileName = e.target.files[0].name;
    if (fileName) {
        $("#submit-uploaded-file, #show_summery").removeClass("d-none")
        $(".dropify-render").text("").addClass("csv-download")
    }
})
$("#submit-uploaded-file, #show_summery").click(function() {
    var vm = $(this)
    $('.preloader').fadeIn('fast');
    if(vm.attr("id") == "show_summery") {
        $("#show_summery_val").val("true")
    }
    else {
        $("#show_summery_val").val("")   
    }
    var data = new FormData($('#delete-contact-upload-form').get(0));
    var fileExtension = ['csv', 'xls', 'xlsx'];
    if ($(".dropify-filename-inner").text()) {
        if ($.inArray($(".dropify-filename-inner").text().split('.').pop().toLowerCase(), fileExtension) == -1) {
            $("#upload-file-error").text("File format must be csv").removeClass("d-none")
            setTimeout(function() {
                $("#upload-file-error").addClass("d-none")
            }, 3000);
        } else {
            $.ajax({
            type: 'post',
            headers: {
                "X-CSRFToken": csrf_token
            },
            url: $('#delete-contact-upload-form').attr('action'),
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(data) {
                $('.preloader').fadeOut('fast');
                if(vm.attr("id") == "show_summery") {
                    $("#summery_div").removeClass("d-none")
                    $("#count").text(data["total_contacts"])
                    $("#all_contact_count").text(data["all_contact_count"])
                    if(data["total_contacts"]==0){
                        $(".error_text").removeClass("d-none")
                    }
                }
                else {
                    $("#summery_div").addClass("d-none")
                    $(".error_text").addClass("d-none")
                    showSwal('success-message', 'Data Deleted Successfully')
                }
            },
            error: function(data) {
                $("#upload-file-error").text(data["responseJSON"]["msg"]).removeClass("d-none")
                    setTimeout(function() {
                        $("#upload-file-error").addClass("d-none")
                    }, 3000);
                    }
        });
        }
    } else {
        $("#upload-file-error").text("Upload File To Validate").removeClass("d-none")
        setTimeout(function() {
            $("#upload-file-error").addClass("d-none")
        }, 3000);
    }

});
$(".delete_contact_modal").on('hidden.bs.modal', function() {
    $("#delete-contact-upload-form")[0].reset();
    $(".dropify-clear").click()
    $("#submit-uploaded-file, #show_summery").addClass("d-none")
    $("#summery_div").addClass("d-none")
    $(".error_text").addClass("d-none")
    $("#action_type").prop('selectedIndex',0);
});
// uplod contacts to delete ends here

$('.trunk_type').change(function(){
    if($(this).val() =="trunk_group"){
        add_trunk_vue.hide_single_trunk=true
        $("#trunk_group_select").val("")
        $("#trunk_group").removeClass("d-none")
        $("#carrier-div").addClass("d-none")
    }
    else {
        add_trunk_vue.hide_single_trunk=false
        add_trunk_vue.group_trunk_list=[{"trunk_priority":1, "trunk_id":"","did_type":"","did":[],"did_start":"","did_end":"","options":[]}]
        $("#trunk_group").addClass("d-none")   
        $("#carrier-div").removeClass("d-none")
    }
})

$('.email_type').change(function(){
    if($(this).val() =="1"){
        $("#available_email_disposition").removeClass("d-none")
    }
    else {
         $("#available_email_disposition").addClass("d-none")   
    }
})

$("#action_type").change(function(){
    $('#update_crm_fields').val(null).trigger('change')
    if($(this).val() == "update") {
        $("#unique_id_update_js, #reference_field").removeClass("d-none")
        $("#duplicate_field").addClass("d-none")
        setTimeout(function(){ $('#unique_id_update_js').addClass("d-none") }, 5000);
    }
    else {
        $("#duplicate_field").removeClass("d-none")
        $("#reference_field").addClass("d-none")
    }
    if ($(this).val() == "update" || $(this).val() == "transfer_contacts" || $(this).val() == 'insert') {
        $("#search_type_div").removeClass("d-none")
        if($(this).val() == "update"){
           $("#update_col_type").removeClass("d-none")
        }else{
            $("#update_col_type").addClass("d-none")
        }
    }
    else if ($(this).val() == "delete_contacts") {
        $("#upload_delete_modal").modal("show")
    }
    else {
        $("#search_type_div").addClass("d-none")
        $("#update_col_type").addClass("d-none")  
    }
})
user_lead_data_campaign_wise_detail_table = $('#userwise-campaign-details-table').DataTable({
    scrollX:true,
    overflowX:'auto',
    "order": [[ 1, "asc" ]],
    "columnDefs": [{
        targets: [2],
        className: "assign_data_count"
    },
    {
        targets: [0],
        width: "1%",
        orderable:false,
        render : function(data){
            if (data){
                return '<span class="state-dot" style="background-color: #04B76B;"></span>';
            }else{
                return '<span class="state-dot" style="background-color: #FF5E6D;"></span>'
            }
        }
    }],
});

campaign_lead_detail_table = $('#campaign-phonebook-table').DataTable({
    scrollX:true,
    overflowX:'auto',
    "columnDefs": [{
        targets: [1,2,3,4,5],
        className: "text-center"
    }]
});

function showCampaignLead(campaign_name){
    $.ajax({
        type: 'GET',
        url: '/api/get-phonebook-details/',
        data:{
            campaign_name:campaign_name
        },
        success: function(data) {
            $('#campaign_lead_deatails').modal('show');
            if ("without_css" in data) {
                $(".css_data").removeClass("d-none")
                $("#with_css").text(data["with_css"])
                $("#without_css").text(data["without_css"])

            }
            else{
                $(".css_data").addClass("d-none")
            }
            campaign_lead_detail_table.clear()
            campaign_lead_detail_table.rows.add(data['lead_list_detail']); // Add new data
            campaign_lead_detail_table.columns.adjust().draw(true); // Redraw the DataTable
            campaign_lead_detail_table.columns.adjust().responsive.recalc();
            setTimeout(function(){ $('.ll_total_data').trigger("click") }, 500);
        }
    })
}
function showUserwiseLead(username){
    $.ajax({
        type: 'GET',
        url: '/api/get-userwisecampaign-leadlist/',
        data:{
            username:username
        },
        success: function(data) {
            if('msg' in data){
                showInfoToast(data['msg'],'text-center')
            }else{    
                $('#user_camp_campaign_lead_deatails').modal('show');
                user_lead_data_campaign_wise_detail_table.clear()
                user_lead_data_campaign_wise_detail_table.rows.add(data['user_wise_campaign_data']); // Add new data
                user_lead_data_campaign_wise_detail_table.draw(true); // Redraw the DataTable
            }
        }
    })
}

$('#user_camp_campaign_lead_deatails').on('shown.bs.modal', function(e){
    user_lead_data_campaign_wise_detail_table.columns.adjust().responsive.recalc();
});


function selectUnselectAll(from_id, to_id, remove_class){
    var de_move_group = $(""+from_id+"").find('div:not(.d-none)')
    $(""+to_id+"").append(de_move_group)
    $("."+remove_class+""+" div:not(.d-none)").remove()
}
$(document).on('click', '#admin_to_agent_switchscreen',function(){
    var form_data = {
        'id':$(this).attr('id')
    }
    var url = '/agent/'
    $.ajax({
        type:'post',
        headers: {
                "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()
            },
        url: '/agentscreen/',
        data:form_data,
        success:function(data){
            if(data['return_to_agent']){
                window.location = url
            }
        }   
    })
})

$(document).on('click', '.contact-info', function(){
    var row = $(this).parents('tr')
    var row_data = contact_info_table.row(row).data()
    $.ajax({
        type:'GET',
        headers: {
                "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()
            },
        url: '/api/get-edit-contact/'+row_data.id+'/',
        data:{},
        success:function(data){
            $('#contact_info_modal').modal('show')
            contact_info_vue.fields = data.crm_fields
            contact_info_vue.temp_data = data.crm_fieds_data
            contact_info_vue.field_data = data.crm_data
            contact_info_vue.createAlternateDict(data.alt_numeric)
            contact_info_vue.numeric = data.contact.numeric
            contact_info_vue.phonebook_list = data.phonebook_list
            contact_info_vue.selected_phonebook = data.contact.phonebook
            contact_info_vue.status_list = data.contact_status
            contact_info_vue.selected_status = data.contact.status
            contact_info_vue.email = data.contact.email
            contact_info_vue.first_name = data.contact.first_name
            contact_info_vue.last_name = data.contact.last_name
            contact_info_vue.user = data.contact.user
            contact_info_vue.contact_id = row_data.id
            if(data.contact.status=='Queued'){
                $("#status").attr('disabled', true)
            }else{
                $("#status").attr('disabled', false)
            }
        }   
    })
})
$("#contact_info_modal").on('hidden.bs.modal', function() {
    $("#edit-contact-info")[0].reset();
    contact_info_vue.resetFields()
});

$("#email-template-submit-btn").click(function() {
    var script_data = tinyMCE.get('scriptEditor').getContent();
    $("#script-data").val(script_data)
    var script_form = $("#script-create-form")
    if (script_form.isValid() == true ) {
        $.ajax({
            type: 'POST',
            headers: {"X-CSRFToken": csrf_token},
            url: '/EmailManagement/EmailTemplate/create/',
            data: script_form.serialize(),
            success: function (data) {
                if ($("#script_id").val() != "") {
                    showSwal('success-message', 'Email Template Successfully Updated', '/EmailManagement/EmailTemplate/')
                }
                else {
                    showSwal('success-message', 'Email Template Successfully Created', '/EmailManagement/EmailTemplate/')
                }
            },
            error: function (data) {
                if (data["responseJSON"]["name"]){
                    $("#script-name-error").html(`<span class="help-block form-error">${data["responseJSON"]["name"]}</span>`).addClass("has-error")
                    $("#name").removeClass("valid").addClass("error")
                }
                if ("name" in data["responseJSON"]) {
                    $("#script-name-error").addClass("has-error").removeClass("d-none").html(
                        '<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>')
                    setTimeout(function(){ $("#script-name-error").addClass("d-none") }, 3000);
                }
                
            }
        });
    }
})

$(document).on('change','#template_campaign',function(){
    var camp_name = $.trim($('#template_campaign option:selected').text())
    var select_length = $('#template_campaign option:selected').length;
    var selected_campaigns = $('#template_campaign').val()
    if (select_length <=1) {
        $.ajax({
            type: 'POST',
            headers: {"X-CSRFToken": csrf_token},
            url: '/api/check-email-crm-fields/',
            data: {"camp_id": $(this).val(), "camp_name":camp_name, "campaign_to_keep":itemsToKeep},
            success: function (data) {
                $('#template_campaign').empty()
                if(data['campaign_list'].length>0){
                    $.each(data['campaign_list'], function( index, value ) {
                        if($.inArray( value.id.toString(), selected_campaigns ) != -1) {
                            $('#template_campaign').append('<option value='+value.id+' selected>'+value.name+'</option>')
                        }
                        else {
                            $('#template_campaign').append('<option value='+value.id+'>'+value.name+'</option>')   
                        }
                    })
                    $('#template_campaign').select2('destroy').select2()
                }
               // addScriptEditior([])
               editorField_list = []
               $.each(data["contact_fields"], function(index,value){
                    var editorField_dict = {}
                    editorField_dict['text'] = editorField_dict['value'] = value
                    editorField_list.push(editorField_dict)

                })
                if (tinymce.get('scriptEditor')) {
                        tinymce.remove('#scriptEditor');
                    }
                addScriptEditior(editorField_list)
            },
            error: function (data) {
                
                
            }
        });
    }
})

var module_management_vue = new Vue({
    el :'#module_management_vue',
    delimiters: ["${", "}"],
    data: {
        data : [],
        role_pk : null,
        access_levels : {},
        status: {},
        modules : {},
        agent_disable : true,
        select_all_permissions : false,
        form_data : {
            name : '',
            description: null,
            access_level:'3',
            status : '1',
            permissions : {}
        }
    },
    methods: {
        disablePermission(value){
            if ( value == '3' ){
                this.select_all_permissions = false
                this.agent_disable = true;
                this.form_data.permissions = {...this.permission_dict}
            } else {
                this.agent_disable = false;
            }
        },
        checkRead(event,value){
            
            if(value.status=='Active'){
                value.status='Inactive'
            }else{
                value.status='Active'
            }
        },
        checked_parent(event, value){
            if(value.status=='Active'){
                value.status='Inactive'
            }else{
                value.status='Active'
            }
            for(var i=0; i<value.parent_menu.length;i++){
                value.parent_menu[i]['status'] = value.status
            }
        },
        saveModules(){
            var vm = this
            var type = 'put'
            $.ajax({
                type: type,
                headers: {
                    "X-CSRFToken": csrf_token
                },
                data:{data:JSON.stringify(vm.data)},
                success: function(data) {
                    showSwal('success-message', data['success'], '/Administration/modules/')
                }
            })
        }
    },
    watch : {
        select_all_permissions(val){
            var vm = this
            if (val) {
                $.each(vm.modules, function(index,module_dict) {
                    vm.form_data.permissions[module_dict.name] = [...module_dict.permission_list]
                })
            } else {
                vm.form_data.permissions = {...vm.permission_dict}
            }
        },
        form_data(val) {
            if (val.access_level != '3'){
                this.agent_disable = false
            }
        }
    }
})

var module_validation_form = $("#module-form");
module_validation_form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function(event, currentIndex) {
        if (module_validation_form.isValid() == true) {
            $.ajax({
                type: 'post',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/Administration/modules/',
                data: module_validation_form.serialize(),
                success: function(data) {
                    showSwal('success-message', 'Switch Successfully Created')
                },
                error: function(data) {
                    console.log(data,'error')
                }
            });
        };
    }
})


$('#broadcast_send').click(function(){
   var form = $('#broadcast-form')
   if(form.isValid()){
    $.ajax({
            type: 'post',
            headers: {"X-CSRFToken": csrf_token},
            url: '/api/broadcast-usermessage/',
            data: form.serialize(),
            success:function(data){
                if(data['user'].length > 0){
                    socket.emit('broadcast_message_to_users',{'users':data['user'],'message':data['broadcast_message'],'type':data['type'],
                        'broadcast_time':data['broadcast_time']})
                    showInfoToast('Messaged Broadcasted Successfully',"top-right")
                }else{
                    showWarningToast('No Users to Broadcasted',"top-right")
                }
                $('#broadcast_message').val('')
            }   
        });
   }
});

function daemon_action(daemon, action) {
    var pagerefresh = ""
    custom_pagination_table.processing(true)
    if (action == "pagerefresh") {
        pagerefresh = action
        action = "";
    }
    data = {
        'service': daemon,
        'action': action,
        'csrfmiddlewaretoken': csrf_token,
        'pagerefresh': pagerefresh,
    }
    $.ajax({
        type: 'post',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/Administration/daemon/',
        data: data,
        success: function (data) {
            if (data["msg"]) {
                errorAlert(data['title'],data["msg"])
                return;
            }
            custom_pagination_table.clear()
            custom_pagination_table.rows.add(data['status_daemon']); // Add new data
            custom_pagination_table.columns.adjust().draw(false);(data['']);
            if (pagerefresh != "pagerefresh") {
                showSwal("success-message-without-reload")
            }
        },
        error: function (data) { },
        complete: function(data) {
            custom_pagination_table.processing(false)
        }
    });
}
var create_edit_daemon_form = $("#create_edit_daemon_form");
create_edit_daemon_form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    onFinished: function (event, currentIndex) {
        if (create_edit_daemon_form.isValid() == true) {
            var type = 'post'
            var pk = $('#daemon_number_pk').val()
            if (pk) {
                type = 'put'
            }
            $.ajax({
                type: type,
                headers: {
                    "X-CSRFToken": csrf_token
                },
                url: '/Administration/daemon/create_edit/',
                data: create_edit_daemon_form.serialize(),
                success: function (data) {
                    showSwal('success-message', data['success'])
                },
                error: function (data) {
                    console.log(data)
                    showSwal('success-message', data['success'])

                    // if ("name" in data["responseJSON"]) {
                    //     $("#trunk_name_msg").addClass("has-error").html(
                    //         '<span class="help-block form-error">' + data["responseJSON"]["name"] + '</span>').removeClass("d-none")
                    //     setTimeout(function () {
                    //         $("#trunk_name_msg").addClass("d-none")
                    //     }, 3000);
                    // }
                }
            });
        };
    }
});


$("#holidays-submit-btn").click(function() {
    var holiday_form = $("#holidays-create-form")

    if ($("#holidays_id").val() != "") {
        var url = `/Administration/Holidays/edit/${$("#holidays_id").val()}/`
    }
    else {
        var url = '/Administration/Holidays/create/'
    }

    if (holiday_form.isValid() == true ) {
        $.ajax({
            type: 'POST',
            headers: {"X-CSRFToken": csrf_token},
            url: '',
            data: holiday_form.serialize(),
            success: function (data) {
                if("name" in data){
                    $("#name-error").html(`<span class="help-block form-error">${data["name"]}</span>`).addClass("has-error")
                    $("#name").removeClass("valid").addClass("error")
                }else if("holiday_date" in data ){
                    $("#holiday_date_error").html(`<span class="help-block form-error">${data["holiday_date"]}</span>`).addClass("has-error")
                    setTimeout(function(){ $("#holiday_date_error").addClass("d-none") }, 3000);
                }else{
                    if ($("#holidays_id").val() != "") {
                        showSwal('success-message', 'Holiday Successfully Updated', '/Administration/Holidays/')
                    }
                    else {
                        showSwal('success-message', 'Holiday Successfully Created', '/Administration/Holidays/')
                    }
                }
            },
            error: function (data) {
                if (data["responseJSON"]["name"]){
                    $("#name-error").html(`<span class="help-block form-error">${data["responseJSON"]["name"]}</span>`).addClass("has-error")
                    $("#name").removeClass("valid").addClass("error")
                }
                if ("name" in data["responseJSON"]) {
                    $("#name-error").addClass("has-error").removeClass("d-none").html(
                        '<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>')
                    setTimeout(function(){ $("#script-name-error").addClass("d-none") }, 3000);
                }
                
            }
        });
    }
})

$('#edit-third_party_user_campaign').click(function(){
    var form = $('#thirdparty-user-camp-edit-form')
    token_id = $('#token_id').val()
    if(form.isValid()){
       $.ajax({
            type: 'post',
            headers: {"X-CSRFToken": csrf_token},
            url: '/CampaignManagement/third-party-user-campaign/'+token_id+'/',
            data: form.serialize(),
            success: function (data) {
                 if("name" in data){
                    $("#user-error").html(`<span class="help-block form-error">${data["name"]}</span>`).addClass("has-error")
                    $("#user").removeClass("valid").addClass("error")
                }else if("mobile_no" in data){
                    $("#mobile_exists").html(`<span class="help-block form-error">${data["mobile_no"]}</span>`).addClass("has-error")
                    $("#mobile_exists").removeClass("valid").addClass("error")
                }else{
                    showSwal('success-message', 'Token User Successfully Updated', '/CampaignManagement/third-party-user-campaign/')
                }
            },
            error: function (data) {
            }
        });  
    }
 })
 $('#filter_pending_contacts').click(function() {
    $.ajax({
        type: 'get',
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: '/CallReports/pending-contacts/',
        data: {
            "phonebook": $('#contact_phonebook_select').val(),
            "campaign": $("#contact_campaign_select").val()
        },
        success: function(data) {
            var columns_list = []
            $.each(data['columns_list'], function(index, value) {
                var column_dict = {}
                if (value == 'created_date'){
                    column_dict['title'] = 'Flexydial Insert Date'
                }else{
                    column_dict['title'] = value.replace('_', ' ')    
                }
                column_dict['data'] = value
                column_dict['name'] = value
                column_dict['className'] = value
                columns_list.push(column_dict)
            })
            $.each(data['crm_fields'], function(index, value) {
                var column_dict = {}
                var data = value.replace(/  +/g, ' ').replace(/ /g, "_").replace(':', '.').toLowerCase();
                column_dict['data'] = 'contact_info.' + data
                column_dict['title'] = value
                columns_list.push(column_dict)
            })
            columns_list.push({
                'data': 'id',
                'title': 'Action'
            })
            if ($.fn.DataTable.isDataTable('#pending-contact-table')) {
                pending_contact_table.clear().destroy();
                $('#pending-contact-table').empty()
            }
            pending_contact_table = $('#pending-contact-table')
            if(data["report_visible_cols"].length > 0) {
                pending_contact_table = PendingContacts(table, columns_list, data["report_visible_cols"])
            }
            else {
                pending_contact_table = PendingContacts(table, columns_list)

            }

        }
    })
})
$('#pending-contact-table').on('processing.dt', function(e, settings, processing) {
    if (!processing) {
         if (pending_contact_table.data().any()) {
            $('#contact_info_download').removeClass('d-none')
        }
    }
})
/* pending contacts display js */
function PendingContacts(table, column_data, col_list=[]) {
    // var id = '#'+ table.attr('id');
    console.log(column_data,"dataaaaaaaa")
    var table_instance = table.DataTable({
        "scrollX": true,
        "serverSide": true,
        "processing": true,
        "searching": false,
        "ajax": {
            "url": '/CallReports/pending-contacts/',
            "headers": {
                "X-CSRFToken": csrf_token
            },
            "type": "POST",
            "data": function(d) {
                d.format = "datatables"
                d.campaign = $('#contact_campaign_select').val()
                d.phonebook = $('#contact_phonebook_select').val()
                d.numeric = $('#destination_extension').val()
                d.disposition = $('#disposition').val()
                d.start_date = $('#start-date input').val()
                d.end_date = $('#end-date input').val()
            },
        },
        "columns": column_data,
        columnDefs: [{
            "targets": '_all',
           "defaultContent": " ",
       }, {
           targets: [0],
            render: function(data, type, row) {
                return '<a class="name-el" href="/CallReports/pending-contacts/' + row.id + '/">' + data + '</a>'
            }

        }, {
            targets: [-1],
            orderable: false,
            data: 'id',
            render: function(data) {
                return `<div class="dropdown show">
                    <button class="btn btn-secondary dropdown-toggle table-dropdown" role="button" id="dropdownMenuLink"'
                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Choose Action</button>
                    <div class="dropdown-menu" aria-labelledby="dropdownMenuLink">
                    <a class="dropdown-item" href="/CallReports/pending-contacts/`+data+`/">Modify</a></div></div>`
                }
            },
        ],
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
           className: 'btn-outline-dark',
       },
       {
       text: 'Save column visibility',
       className: 'btn-outline-dark',
       action: function ( e, dt, node, config ) {
           var col_name = []
           var report_name = $("#report_name").val()
           $(".dataTables_scrollHeadInner th").each(function(index) {
               temp_name = $(this).attr("class").split(" ")
               if (temp_name) {
                   col_name.push(temp_name[0])
               }
           });
           console.log(col_name,"col nameeee")
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
        ]
        // pageLength: 2
    });
    if(col_list.length>0) {
        $(".dataTables_scrollHeadInner th").each(function(index) {
            temp_name = $(this).attr("class").split(" ")
            if (temp_name) {
                temp_name = temp_name[0]
                if ($.inArray(temp_name, col_list) == -1) {
                    // report_table.column(index).visible(true)
                   table_instance.column(index).visible(false)   
                }

            }
            
        });

    }
    return table_instance
}
$("#cancel-ndnc-upload, #cancel-priority-upload, #cancel-contact-upload").click(function() {
    showSwal('success-message', 'Upload Operation Cancelled')
    $(".dropify-clear").click()
})
