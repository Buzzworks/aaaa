//jquery to check restrict sidebar menu by permissions


// jquery for datatables with select option
result = []
delete_highp = false
function selective_datatable(table){
	var id = '#'+ table.attr('id');
	$(table).DataTable( {
		responsive: {
			details: {
				display: $.fn.dataTable.Responsive.display.modal( {
					header: function ( row ) {
						var data = row.data();
						return 'Details for '+data[1];
					}
				} ),
				renderer: $.fn.dataTable.Responsive.renderer.tableAll( {
					tableClass: 'table'
				} )
			}
		},
		columnDefs: [ 
		// {
		// 	targets: [-2],
		// 	searchable: false,
		// 	orderable: false,
		// 	render: function (data, type, full, meta){
		// 		return '<div class="form-check"><label class="form-check-label"><input type="checkbox" class="form-check-input"><i class="input-helper"></i></label></div>';
		// 	}
		// },
		{
			targets: [0, -2],
			orderable: false,
			width:"1%"
		},
		{
			targets: [ -1 ],
			orderable: false,
			width:"16%"
		},
		{
			responsivePriority: 1, targets: 0
		},
		{
			responsivePriority: 2, targets: 1
		},
		{
			responsivePriority: 3, targets: -2
		},
		{
			responsivePriority: 4, targets: -1
		}
		],
		order: [[ 0, 'asc' ]],
		// pageLength: 2
	} );
	// Handle click on checkbox
	
	$(id+' tbody').on('click', 'input[type="checkbox"]', function(e){
		var $row = $(this).closest('tr');
		if(this.checked){
			result.push($row.attr("id"))
			$row.addClass('selected');
		} else {
			result = jQuery.grep(result, function(value) {
				return value != $row.attr("id");
			});
			$row.removeClass('selected');
		}
      // Prevent click event from propagating to parent
      e.stopPropagation();
  });

   // Handle click on "Select all" control
   $(id).on('click','thead input[name="select_all"]', function(e){
   	
   	if(this.checked){
   		$(id+' tbody input[type="checkbox"]:not(:checked)').trigger('click');
   		// delete_highp = true
   		result = []
   		result = query_set_list
   	} else {
   		$(id +' tbody input[type="checkbox"]:checked').trigger('click');
   	}

      // Prevent click event from propagating to parent
      e.stopPropagation();
  });
   $(id).on('draw.dt', function () {
   	// if($('thead input[name="select_all"]').is(':checked')){
   	// 	$(id+" tbody input[type='checkbox']:not(:checked)").trigger('click');
   	// }
   	if (result) {
   		$.each(result, function( index, value ) {
   			$(id+" tbody tr[id="+value+"] input[type='checkbox']").prop("checked", true)
   		});
   	}
   	else {
   		$(id+" tbody input[type='checkbox']:checked").trigger('click');    
   	}

   });
}
$("#user_access_level").change(function() {
	if($("#user_access_level option:selected").text() == "admin" && $("#superuser_div").hasClass("d-none")) {
		$("#superuser_div").removeClass("d-none")
	}
	else {
		$("#superuser_div").addClass("d-none")
		$("#superuser_chkbox").prop("checked", false)
	}
})
var validationForm = $("#user-form");
var csrf_token = $("input[name='csrfmiddlewaretoken']").val()
move =false
ajaxOptions = {
	type: 'post',
	headers: {"X-CSRFToken": csrf_token},
	url: '/UserManagement/check-user/',
	async: false,
	success: function (response_data) {
		if ($.isEmptyObject(response_data) == false) {
			if ("username" in response_data) {
				$("#username-msg").addClass("has-error")
				$("#username-msg").html("<span class='help-block form-error'>"+response_data["username"]+"</span>")
			}
			if ("extension" in response_data) {
				$("#extension-msg").addClass("has-error")
				$("#extension-msg").html("<span class='help-block form-error'>"+response_data["extension"]+"</span>")
			}
			if ("email" in response_data) {
				$("#email-msg").addClass("has-error")
				$("#email-msg").html("<span class='help-block form-error'>"+response_data["email"]+"</span>")
			}
			move = false
			return false
		}
		else {
			move =true
			$("#extension-msg").html("")
			$("#email-msg").html("")
			$("#username-msg").html("")
		}
	},
	error: function (data) {

	  // setTimeout(function(){ $("#login-error-msg").addClass("d-none") }, 3000);
	}
}
$("#create-user-btn").click(function() {
	var form = $("#user-create-form")
	if($("#caller_id").val() != "") {
		$("#caller_id").attr("data-validation", "length")
	}
	if($("#email").val() != "") {
		$("#email").attr("data-validation", "email")
	}
	if(form.isValid()) {
		$.ajax({
			type: 'post',
			headers: {"X-CSRFToken": csrf_token},
			url: '/UserManagement/Users/create/',
			data: form.serialize(),
			success: function (data) {
				showSwal('success-message', 'User Successfully Created', '/UserManagement/Users/')
			},
			error: function (data) {
				if (data["responseJSON"]["errors"]) {
					$("#user-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
					setTimeout(function(){ $("#user-err-msg").addClass("d-none") }, 3000);
				}
			}
		});	
	}
})
// $('#user-form  #datepicker-popup, #user-edit-form #datepicker-popup').datepicker({
// 	endDate: '+0d',
//   	enableOnReadonly: true,
//   	todayHighlight: true,
//   	format: 'yyyy-mm-dd',
// });

// $('body').on('focus',".start-date, .end-date", function(){
//     $(this).datepicker({
//   	enableOnReadonly: true,
//   	todayHighlight: true,
//   	format: 'yyyy-mm-dd',
//   	orientation: 'bottom auto',
// 	autoclose: true,
// 	})
// })

$("#user_role").change(function() {
	var current_val = $('option:selected', this).attr('data-level');
	if(current_val != "Admin") {
		if (current_val == "Agent") {
			access_level = "Manager"
		}
		else if(current_val == "Manager") {
			access_level = "Admin"	
		}
		$("#reporting-row").removeClass("d-none")
		$("#reporting-row option:first").attr("selected", "selected")
		$('#user_access_level option[data-access="'+access_level+'"]').removeClass("d-none")
		$('#user_access_level option[data-access!="'+access_level+'"]').addClass("d-none")
	}
	else {
		$("#reporting-row").addClass("d-none")
	}
})
//Add phone block started
var AddPhoneForm = $("#add-phone-form");
AddPhoneForm.children("div").steps({
	headerTag: "h3",
	bodyTag: "section",
	transitionEffect: "slideLeft",
	onStepChanging: function(event, currentIndex, newIndex) {
		AddPhoneForm.val({
			ignore: [":disabled", ":hidden"]
		})
		
		return AddPhoneForm.val();
	},
	onFinishing: function(event, currentIndex) {
		
		return AddPhoneForm.val();
	},
	onFinished: function(event, currentIndex) {
		$.ajax({
			type: 'post',
			headers: {"X-CSRFToken": csrf_token},
			url: '/UserManagement/add-phone/',
			data: AddPhoneForm.serialize(),
			success: function (data) {
				showSwal('success-message', 'Add Phone Successfully Created')
			},
			error: function (data) {
			}
		});
		
	}
});
$("#starting_extension").keyup(function(){
	$(".phone_extension").val($(this).val())
})
$(".phone_extension").keyup(function(){
	$("#starting_extension").val($(this).val())
})
// Add phone block ends
$(document).on('click','.reload, #refresh-page',function(){
	location.reload();
});

/*this function is related to the department form validation and submission */
$(document).on('click','.group-modify',function(){
	$(".dtr-bs-modal").modal('hide');
	var pk =  parseInt($(this).attr("data-groupid"));
	$.ajax({
		type: 'post',
		headers: {"X-CSRFToken": csrf_token},
		url: '/UserManagement/get-group/'+pk+'/',
		success: function (data) {
			$('#update_group_name').val(data.querysets['name'])
			$('form').find('#update_group_status').val(data.querysets['status'])
			$('#group_pk').val(pk)
			$('#modal_update_group').modal('show');
		},
		error: function (data) {
		}
	});
});	

var group_update_form = $("#update-group-form");
group_update_form.children("div").steps({
	headerTag: "h3",
	bodyTag: "section",
	transitionEffect: "slideLeft",
	onFinished: function(event, currentIndex) {
		var pk = $('#group_pk').val()
		if (group_update_form.isValid()==true){
			$.ajax({
				type: 'put',
				headers: {"X-CSRFToken": csrf_token},
				url: '/UserManagement/get-group/'+pk+'/',
				data: group_update_form.serialize(),
				success: function (data) {
					showSwal('success-message', 'Department Successfully Created')
				},
				error: function (data) {
					if ("name" in data["responseJSON"]) {
						$("#group-msg").addClass("has-error").html(
							'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>').removeClass("d-none")
						setTimeout(function(){ $("#group-msg").addClass("d-none") }, 3000);
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
		if (group_validation_form.isValid()==true){
			$.ajax({
				type: 'post',
				headers: {"X-CSRFToken": csrf_token},
				url: '/UserManagement/Groups/',
				data: group_validation_form.serialize(),
				success: function (data) {
					showSwal('success-message', 'Group Successfully Created')
				},
				error: function (data) {
					if ("name" in data["responseJSON"]) {
						$("#group-name-msg").addClass("has-error").html(
							'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>').removeClass("d-none")
						setTimeout(function(){ $("#group-name-msg").addClass("d-none") }, 3000);
					}
				}
			});
		};
	}
});
/* department form validation function ends here */

/*this function is related to the Switch form validation and submission */
$(document).on('click','#switch-modify',function(){
	var pk =  parseInt($(this).attr("data-switchid")); 
	$.ajax({
		type: 'post',
		headers: {"X-CSRFToken": csrf_token},
		url: '/CampaignManagement/get-switch/'+pk+'/',
		success: function (data) {
			$('#update_switch_name').val(data.querysets['name'])
			$('#update_ip_address').val(data.querysets['ip_address'])
			$('#update_status').val(data.querysets['status'])
			$('#update_switch_pk').val(pk)
			$('#modal_update_switch').modal('show');
		//showSwal('success-message', 'User Group Successfully Created')
	},
	error: function (data) {
		
	}
});
});	

var switch_update_form = $("#update-switch-form");
switch_update_form.children("div").steps({
	headerTag: "h3",
	bodyTag: "section",
	transitionEffect: "slideLeft",
	onFinished: function(event, currentIndex) {
		var pk = $('#update_switch_pk').val()
		if (switch_update_form.isValid()==true){
			$.ajax({
				type: 'put',
				headers: {"X-CSRFToken": csrf_token},
				url: '/CampaignManagement/get-switch/'+pk+'/',
				data: switch_update_form.serialize(),
				success: function (data) {
					showSwal('success-message', 'Switch Successfully Updated')
				},
				error: function (data) {
					if ("name" in data["responseJSON"]) {
						$("#update_switch_name").removeClass('valid').addClass('error');
						$("#update_switch_name_msg").addClass("has-error").html(
							'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>').removeClass("d-none")
						setTimeout(function(){ $("#update_switch_name_msg").addClass("d-none") }, 3000);
					}
					if ("ip_address" in data["responseJSON"]) {
						$("#update_ip_address").removeClass('valid').addClass('error');
						$("#update_ip_address_msg").addClass("has-error").html(
							'<span class="help-block form-error">'+data["responseJSON"]["ip_address"]+'</span>').removeClass("d-none")
						setTimeout(function(){ $("#update_ip_address_msg").addClass("d-none") }, 3000);
					}
				}
			});
		};
	}
});

var switch_validation_form = $("#switch-form");
switch_validation_form.children("div").steps({
	headerTag: "h3",
	bodyTag: "section",
	transitionEffect: "slideLeft",
	onFinished: function(event, currentIndex) {
		if (switch_validation_form.isValid()==true){
			$.ajax({
				type: 'post',
				headers: {"X-CSRFToken": csrf_token},
				url: '/CampaignManagement/Switch/',
				data: switch_validation_form.serialize(),
				success: function (data) {
					showSwal('success-message', 'Switch Successfully Created')
				},
				error: function (data) {
					if ("name" in data["responseJSON"]) {
						$("#switch_name").removeClass('valid').addClass('error');
						$("#switch_name_msg").addClass("has-error").html(
							'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>').removeClass("d-none")
						setTimeout(function(){ $("#switch_name_msg").addClass("d-none") }, 3000);
					}
					if ("ip_address" in data["responseJSON"]) {
						$("#ip_address").removeClass('valid').addClass('error');
						$("#switch_ip_address_msg").addClass("has-error").html(
							'<span class="help-block form-error">'+data["responseJSON"]["ip_address"]+'</span>').removeClass("d-none")
						setTimeout(function(){ $("#switch_ip_address_msg").addClass("d-none") }, 3000);
					}
				}
			});
		};
	}
});
/* server form validation function ends here */

/*this function is related to the Dial Trunk form validation and submission */
$(document).on('click','.trunk-modify',function(){
	$(".dtr-bs-modal").modal('hide');
	var pk = $(this).attr("data-trunk")
	$.ajax({
		type: 'post',
		headers: {"X-CSRFToken": csrf_token},
		url: '/CampaignManagement/get-dialtrunk/'+pk+'/',
		success: function (data) {
			$('#update_trunk_name').val(data.querysets['name'])
			$('#update_dial_string').val(data.querysets['dial_string'])
			$('#update_channel_count').val(data.querysets['channel_count'])
			$('#update_trunk_type').val(data.querysets['trunk_type'])
			$('#update_trunk_switch').val(data.querysets['switch'])
			$('#update_status').val(data.querysets['status'])
			$('#update_trunk_pk').val(pk)
			$('#modal_update_trunk').modal('show');
		//showSwal('success-message', 'User Group Successfully Created')
	},
	error: function (data) {
		
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
		if (dialtrunk_update_form.isValid()==true){
			$.ajax({
				type: 'put',
				headers: {"X-CSRFToken": csrf_token},
				url: '/CampaignManagement/get-dialtrunk/'+pk+'/',
				data: dialtrunk_update_form.serialize(),
				success: function (data) {
					showSwal('success-message', 'Dial Trunk Successfully Updated')
				},
				error: function (data) {
					if ("name" in data["responseJSON"]) {
						$("#update_trunk_name_msg").addClass("has-error").html(
							'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>').removeClass("d-none")
						setTimeout(function(){ $("#update_trunk_name_msg").addClass("d-none") }, 3000);
					}
				}
			});
		};
	}
});

var dialtrunk_validation_form = $("#trunk-form");
dialtrunk_validation_form.children("div").steps({
	headerTag: "h3",
	bodyTag: "section",
	transitionEffect: "slideLeft",
	onFinished: function(event, currentIndex) {
		if (dialtrunk_validation_form.isValid()==true){
			$.ajax({
				type: 'post',
				headers: {"X-CSRFToken": csrf_token},
				url: '/CampaignManagement/DialTrunk/',
				data: dialtrunk_validation_form.serialize(),
				success: function (data) {
					showSwal('success-message', 'Dial Trunk Successfully Created')
				},
				error: function (data) {
					if ("name" in data["responseJSON"]) {
						$("#trunk_name_msg").addClass("has-error").html(
							'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>').removeClass("d-none")
						setTimeout(function(){ $("#trunk_name_msg").addClass("d-none") }, 3000);
					}
				}
			});
		};
	}
});
/* Dial trunk form validation function ends here */

$("#modal_update_disposition").on('hidden.bs.modal', function () {
	$("#update-disposition-form")[0].reset();
	$('.dispo-tags').next('.tagsinput').remove();
	$('.dispo-tags').val('');
	$('.dispo-tags').removeAttr('data-tagsinput-init');
	$('.dispo-tags').attr('id','update_dispo_tag')
    // $('.dispo-tags').show();
});
/*this function is related to the disposition form validation and submission */
$(document).on('click','#dispo-modify',function(){
	var pk =  parseInt($(this).attr("data-dispoid"));
	 // $("#update-disposition-form")[0].reset();
	 $.ajax({
	 	type: 'post',
	 	headers: {"X-CSRFToken": csrf_token},
	 	url: '/CampaignManagement/get-disposition/'+pk+'/',
	 	success: function (data) {
	 		$('#update_dispo_name').val(data.querysets['name'])
	 		console.log(data.querysets['sub_dispos'])
	 		$('#update_dispo_tag').val(data.querysets['sub_dispos'])
	 		$('#update_status').val(data.querysets['status'])
	 		$('#update_dispo_pk').val(pk)
	 		$('#update_dispo_tag').tagsInput({
	 			'width': '100%',
	 			'height': '75%',
	 			'interactive': true,
	 			'defaultText': 'Add More',
	 			'removeWithBackspace': true,
	 			'minChars': 0,
    			'maxChars': 0, // if not provided there is no limit
    			'placeholderColor': '#666666',
    		});
	 		$('#modal_update_disposition').modal('show');
	 	},
	 	error: function (data) {
	 	}
	 });
	});	

var dispo_update_form = $("#update-disposition-form");
dispo_update_form.children("div").steps({
	headerTag: "h3",
	bodyTag: "section",
	transitionEffect: "slideLeft",
	onFinished: function(event, currentIndex) {
		var pk = $('#update_dispo_pk').val()
		if (dispo_update_form.isValid()==true){
			$.ajax({
				type: 'put',
				headers: {"X-CSRFToken": csrf_token},
				url: '/CampaignManagement/get-disposition/'+pk+'/',
				data: dispo_update_form.serialize(),
				success: function (data) {
					showSwal('success-message', 'Department Successfully Created')
				},
				error: function (data) {
					if ("name" in data["responseJSON"]) {
						$("#dispo-name-msg").addClass("has-error").html(
							'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>').removeClass(
							"d-none")
							setTimeout(function(){ $("#dispo-name-msg").addClass("d-none") }, 3000);
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
		if($("#tags").val() != "") {
			tags = true
		}
		else {
			tags = false
			$("#subdispo-msg").addClass("has-error").html(
				'<span class="help-block form-error">This is a required field</span>')
			setTimeout(function(){ $("#primarydispo-msg").addClass("d-none") }, 3000);
		}
		if (dispo_validation_form.isValid()==true && tags==true){
			$.ajax({
				type: 'post',
				headers: {"X-CSRFToken": csrf_token},
				url: '/CampaignManagement/Dispositions/',
				data: dispo_validation_form.serialize(),
				success: function (data) {
					showSwal('success-message', 'Dispositions Successfully Created')
				},
				error: function (data) {
					if ("name" in data["responseJSON"]) {
						$("#primarydispo-msg").addClass("has-error").html(
							'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>').removeClass(
							"d-none")
							setTimeout(function(){ $("#primarydispo-msg").addClass("d-none") }, 3000);
						}
					}
				});
		};
	}
});
/* disposition form validation function ends here */

/*this function is related to the pausebreaks form validation and submission */
$(document).on('click','#pausebreak-modify',function(){
	var pk =  parseInt($(this).attr("data-pbid")); 
	$.ajax({
		type: 'post',
		headers: {"X-CSRFToken": csrf_token},
		url: '/CampaignManagement/get-pausebreak/'+pk+'/',
		success: function (data) {
			$('#update_pausebreak_name').val(data.querysets['name'])
			$('#update_status').val(data.querysets['status'])
			$('#update_pausebreak_pk').val(pk)
    		$("#update_pausebreak-time input").val(data.querysets['break_time'])
    		$("#update_pausebreak-time").datetimepicker({
					format: 'HH:mm',
					pickerPosition:'top-right'
				});
			$('#modal_update_pausebreak').modal('show');
		},
		error: function (data) {
			if ("name" in data["responseJSON"]) {
				$("#primarydispo-msg").addClass("has-error").html(
					'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>').removeClass(
					"d-none")
					setTimeout(function(){ $("#primarydispo-msg").addClass("d-none") }, 3000);
				}
			}
		});
});
// pause break update model hide
$("#modal_update_pausebreak, #modal_add_pausebreak").on('hidden.bs.modal', function () {
	$("#update-pausebreak-form, #pausebreak-form")[0].reset();
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
		if (pausebreak_update_form.isValid()==true){
			$.ajax({
				type: 'put',
				headers: {"X-CSRFToken": csrf_token},
				url: '/CampaignManagement/get-pausebreak/'+pk+'/',
				data: pausebreak_update_form.serialize(),
				success: function (data) {
					showSwal('success-message', 'Pausebreak Successfully Updated')
				},
				error: function (data) {
					if ("name" in data["responseJSON"]) {
						$("#update_pausebreak_name").removeClass('valid').addClass('error');
						$("#pausebreak-msg").addClass("has-error").html(
							'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>').removeClass(
							"d-none")
							setTimeout(function(){ $("#pausebreak-msg").addClass("d-none") }, 3000);
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
		if (pausebreak_validation_form.isValid()==true){
			$.ajax({
				type: 'post',
				headers: {"X-CSRFToken": csrf_token},
				url: '/CampaignManagement/Pausebreaks/',
				data: pausebreak_validation_form.serialize(),
				success: function (data) {
					showSwal('success-message', 'Pausebreaks Successfully Created')
				},
				error: function (data) {
					if ("name" in data["responseJSON"]) {
						$("#pausebreak_name").removeClass('valid').addClass('error');
						$("#pausebreak-name-msg").addClass("has-error").html(
							'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>').removeClass(
							"d-none")
							setTimeout(function(){ $("#pausebreak-name-msg").addClass("d-none") }, 3000);
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
// 	headerTag: "h3",
// 	bodyTag: "section",
// 	transitionEffect: "slideLeft",
// 	onFinished: function(event, currentIndex) {
// 		if (usergroup_validation_form.isValid()==true){
// 			$.ajax({
// 				type: 'post',
// 				headers: {"X-CSRFToken": csrf_token},
// 				url: '/UserManagement/UserRoles/',
// 				data: usergroup_validation_form.serialize(),
// 				success: function (data) {
// 					showSwal('success-message', 'User Group Successfully Created')
// 				},
// 				error: function (data) {
// 				}
// 			});
// 		};
// 	}
// });

$('#create-role-btn').click(function(){
	var permissions = {}
	if ($('#ur_create_form').isValid()==true){
		$.each($('.permission_check'),function(){
			var curr_element = $(this).attr("data-id");
			var access_array = new Array();
			var checked_input = $('#'+curr_element+'_module input:checked')
			$.each(checked_input, function(){
				access_array.push(($(this).attr("id")));
			});
			permissions[curr_element] = access_array
		});
		permissions = JSON.stringify(permissions)
		$('#permissions_input').val(permissions);
		$.ajax({
			type: 'post',
			headers: {"X-CSRFToken": csrf_token},
			data: $('#ur_create_form').serialize(),
			success: function (data) {
				showSwal('success-message', 'User Role Successfully Created', '/UserManagement/UserRoles/')
			},
			error: function (data) {
				if ("name" in data["responseJSON"]) {
					$('#role_name').removeClass('valid').addClass('error');
					$("#name-msg").addClass("has-error").html(
						'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>').removeClass(
						"d-none")
						setTimeout(function(){ $("#name-msg").addClass("d-none") }, 3000);
					}
				}
			});
	}
})

$(document).on('click','#update-role-btn',function(){
	var update_permissions = {} 
	if ($('#ur_update_form').isValid()==true){
		$.each($('.permission_check'),function(){
			var curr_element = $(this).attr("data-id");
			var access_array = new Array();
			var checked_input = $('#'+curr_element+'_module input:checked')
			$.each(checked_input, function(){
				access_array.push(($(this).attr("id")));
			});
			update_permissions[curr_element] = access_array
		});
		update_permissions = JSON.stringify(update_permissions)
		$('#permissions_input').val(update_permissions);
		$.ajax({
			type: 'put',
			headers: {"X-CSRFToken": csrf_token},
			data: $('#ur_update_form').serialize(),
			success: function (data) {
				showSwal('success-message', 'User Role Successfully Updated', '/UserManagement/UserRoles/')
			},
			error: function (data) {
				if ("name" in data["responseJSON"]) {
					$('#role_name').removeClass('valid').addClass('error');
					$("#name-msg").addClass("has-error").html(
						'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>').removeClass(
						"d-none")
					setTimeout(function(){ $("#name-msg").addClass("d-none") }, 3000);
				}
			}
		});
	}
})



function wizardvalidation(validationForm){
	validationForm.children("div").steps({
		headerTag: "h3",
		bodyTag: "section",
		transitionEffect: "slideLeft",
		onStepChanging: function(event, currentIndex, newIndex) {
			validationForm.val({
				ignore: [":disabled", ":hidden"]
			})
			validationForm.isValid();
			if (validationForm.isValid()==true){
				return validationForm.val();
			}
		},
		onFinishing: function(event, currentIndex) {
			validationForm.val({
				ignore: [':disabled']
			})
			validationForm.isValid();
			if (validationForm.isValid()==true){;
				return validationForm.val();
			}
		},
		onFinished: function(event, currentIndex) {
			showSwal('success-message', 'User Successfully Created')
		}
	});
}
$("#user-wizard-modal").on('hidden.bs.modal', function () {
	$("#user-form")[0].reset();
});

$("#uploaded-file").click(function(e) {
	$("#uploaded-file").val("")
	$(".dropify-clear").click()
	$("#validate-phonebook-file").removeClass("d-none")
	// $("#uploaded-file").change()
})
$("#uploaded-file").change(function(e) {
	var fileName = e.target.files[0].name;
	$(".proper_data_div, .improper_data_div").addClass("d-none")
	if (fileName) {
		$(".validate-uploaded-file").removeClass("d-none")
		$(".dropify-render").text("").addClass("csv-download")
	}
})
$(".phonebook-upload-file").change(function(e) {
	var fileName = e.target.files[0].name;
	if (fileName) {
		$(".confirm-edit-phone, .cancel-uploaded-file").addClass("d-none")
	}
})
uploadOptions = {
	cache: false,
	processData: false,
	contentType: false,
	success: function(data) {
		if ("column_err_msg" in data) {
			$(data["column_id"]).text(data["column_err_msg"]).removeClass("d-none")
			if ($("#upload-file-error").length == 0) {
				error_id = "#phonebook-err-msg"
			}
			else {
				error_id = "#upload-file-error"
			}
			setTimeout(function(){ $(error_id).addClass("d-none") }, 5000);
		}
		else {
			$(".cancel-uploaded-file").removeClass("d-none")
			$(".validate-uploaded-file").addClass("d-none")
			if ("correct_file" in data) {
				$("#proper-data").attr("href", data["correct_file"]).removeClass("d-none")
				$(".confirm-user-upload").removeClass("d-none")
				$("#proper-data span.msg").text("Proper Data: "+data["correct_count"])
				$(".proper_data_div").removeClass("d-none")
			}
			if ("incorrect_file" in data) {
				$(".improper_data_div").removeClass("d-none")
				$("#improper-data").attr("href", data["incorrect_file"]).removeClass("d-none")
				$("#improper-data span.msg").text("Improper Data: "+data["incorrect_count"])
			}
		}
	}
}
// This Function is used to validate user uploaded file
$("#validate-uploaded-file").click(function(){
	var data = new FormData($('#user-upload-form').get(0));
	uploadOptions["data"] = data
	uploadOptions["url"] = $('#user-upload-form').attr('action')
	uploadOptions["type"] =  $('#user-upload-form').attr('method')
	var fileExtension = ['csv'];
	if ($(".dropify-filename-inner").text()) {
		if ($.inArray($(".dropify-filename-inner").text().split('.').pop().toLowerCase(), fileExtension) == -1) {
			$("#upload-file-error").text("File format must be csv").removeClass("d-none")
			setTimeout(function(){ $("#upload-file-error").addClass("d-none") }, 3000);
		}
		else {
			$.ajax(uploadOptions);
		}
	}
	else {
		$("#upload-file-error").text("Upload File To Validate").removeClass("d-none")
		setTimeout(function(){ $("#upload-file-error").addClass("d-none") }, 3000);
	}
	
});
// This Function is used to validate phonebook uploaded file
$("#validate-phonebook-file").click(function(){
	var data = new FormData($('#phonebook-form').get(0));
	uploadOptions["data"] = data
	uploadOptions["url"] = $('#phonebook-form').attr('action')
	uploadOptions["type"] =  $('#phonebook-form').attr('method')
	var fileExtension = ['csv'];
	if ($(".dropify-filename-inner").text()) {
		if ($.inArray($(".dropify-filename-inner").text().split('.').pop().toLowerCase(), fileExtension) == -1) {
			$("#phonebook-err-msg").text("File format must be csv").removeClass("d-none")
			setTimeout(function(){ $("#phonebook-err-msg").addClass("d-none") }, 3000);
		}
		else {
			$.ajax(uploadOptions);
		}
	}
	else {
		$("#phonebook-err-msg").text("Upload File To Validate").removeClass("d-none")
		setTimeout(function(){ $("#phonebook-err-msg").addClass("d-none") }, 3000);
	}
});


$("#cancel-uploaded-file, #confirm-upload-file").click(function() {
	data = {}
	current_element = $(this)
	if ($(this).hasClass("confirm-user-upload")) {
		data["perform_upload"] = true
	}
	var proper_file =$("#proper-data").attr("href")
	var improper_file =$("#improper-data").attr("href") 
	data["proper_file"] = proper_file
	data["improper_file"] = improper_file
	$.ajax({
		type: 'post',
		headers: {"X-CSRFToken": csrf_token},
		url: '/UserManagement/Users/upload-operation/',
		data: data,
		success: function (data) {
			if (current_element.hasClass("confirm-user-upload")) { 
				showSwal('success-message', 'User Uploaded Successfully')
			}
			else {
				showSwal('success-message', 'Upload Operation Cancelled')
			}
			$(".dropify-clear").click()
			$("#proper-data, #improper-data, #confirm-upload-file, #cancel-uploaded-file").addClass("d-none")
			$("#validate-uploaded-file").removeClass("d-none")
		},
		error: function (data) {
		}
	});
})
$(".dropify-clear").click(function() {
	$("#validate-uploaded-file").addClass("d-none")
	$(".proper_data_div, .improper_data_div").addClass("d-none")
	$(".dropify-filename-inner").text("")
})
// code related to create phonebook
$(".create-phonebook, #cancel-phonebook-upload").click(function() {
	var proper_file = $("#proper-data").attr("href")
	var improper_file = $("#improper-data").attr("href")
	var current_element = $(this)
	var url = '/CRM/create-phonebook/'
	$("#upload-proper-file").val(proper_file)
	$("#upload-improper-file").val(improper_file)
	$("#phonebook-form").attr("href", "")
	if($(this).hasClass("cancel-uploaded-file")) {
		$("#confirm_file_upload").val(false)
	}
	if (!$(this).hasClass("cancel-uploaded-file")) {
		var form_valid = $("#phonebook-form").isValid()
	}
	if ($(this).hasClass("confirm-edit-phone")) {
		url = '/CRM/phonebook/edit/'+phonebook_id+'/'
	}
	if ($(this).hasClass("cancel-uploaded-file")) {
		var form_valid = true
	}
	if ( form_valid == true ) {
		$.ajax({
			type: 'post',
			headers: {"X-CSRFToken": csrf_token},
			url: url,
			data: $("#phonebook-form").serialize(),
			success: function (data) {
				if (current_element.hasClass("cancel-uploaded-file")) {
					showSwal('success-message', 'Phonebook creation operation cancelled', "/CRM/phonebook/")
				}
				else if (current_element.hasClass("confirm-edit-phone")) {
					showSwal('success-message', 'Phonebook updated Successfully', "/CRM/phonebook/")
				}
				else {
					showSwal('success-message', 'Phonebook created Successfully', "/CRM/phonebook/")
				}
			},
			error: function (data) {
				if (data["responseJSON"]["errors"]) { 
					$("#phonebook-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
					setTimeout(function(){ $("#phonebook-err-msg").addClass("d-none") }, 3000);
				}
				
			}
		});
	}
})
$("#phonebook_name").keyup(function(){
	$("#phonebook_slug").val($(this).val())
})

// Code related to campaign
$(document).on('change','#campaign-server',function(){
	if($(this).val() != "") {
		$('form').find("#carrier-div").removeClass("d-none")
		$('form').find("#carrier_list").val("")
		$('form').find('#carrier_list option[data-server="'+$(this).val()+'"]').removeClass("d-none")
		$('form').find('#carrier_list option[data-server!="'+$(this).val()+'"]').addClass("d-none")
	}
	else {
		$('form').find("#carrier-div").addClass("d-none")
	}
})
function campaign_pre_save_validation (form) {
	$(".selected-departments .badge-pill").each(function(){ 
		$(form).append("<input type='hidden' name='group' value='"+$(this).attr("data-id")+"'>")
	})
	$(".selected-disposition .badge-pill").each(function(){ 
		$(form).append("<input type='hidden' name='disposition' value='"+$(this).attr("data-id")+"'>")
	})
	$(".selected-agents-status .badge-pill").each(function(){ 
		$(form).append("<input type='hidden' name='breaks' value='"+$(this).attr("data-id")+"'>")
	})
	var dial_method =  {}
	dial_method["mannual"] = $("#campaign_mannual").prop("checked")
	dial_method["inbound"] = $("#campaign_inbound").prop("checked")
	if ($("#camp_outbound_check").prop("checked") == false) {
		dial_method["outbound"] = false
	}
	else {
		dial_method["outbound"] = $("#camp_outbound").val()
	}
	var dial_method_flag = true
	if (dial_method["mannual"] == false && dial_method["inbound"] == false && $("#camp_outbound_check").prop("checked") == false) {
		$("#dial_method_msg").removeClass("d-none")
		$(".dial_method_div").addClass("border_color")
		dial_method_flag = false
	}
	else {
		$("#dial_method_msg").addClass("d-none")
		$(".dial_method_div").removeClass("border_color")
	}
	$("#dial_method").val(JSON.stringify(dial_method))
	var lead_recycle_dict = []
	valid =true
	$('#accordion').children('div').each(function (i,current_child) {
		var lead_name = $(this).find(".lead_name").val()
		var lead_count = $(this).find("#count").val()
		var schedule_type = $(this).find("#schedule_type").val()
		flag = empty_lead  = false
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
				if (lead_count || schedule_type) {
					child_dict = {}
					child_dict["name"] = lead_name
					child_dict["count"] = lead_count
					date_dict = {"start_time": $(this).find("#lr_start_time").val(), "end_time": $(this).find("#lr_end_time").val()}

					child_dict["schedule_period"] = JSON.stringify(date_dict)
					child_dict["recycle_time"] = $(this).find("#lead_time").val()
					child_dict["status"] = $(this).find("#lead-status").val()
					if (schedule_type) {
						child_dict["schedule_type"] = schedule_type
					}
					lead_recycle_dict.push(child_dict)
				}
			}
			else {
				empty_lead = true
			}
		}
		else {
			valid =false
			return dispositionAlert(lead_name)

		}
	})
	$("#lead_recycle_dict").val(JSON.stringify(lead_recycle_dict))
	return [dial_method_flag, valid, empty_lead]

}
$(".create-campaign-btn").click(function() {
	response_data = campaign_pre_save_validation('#campaign-create-form')
	dial_method_flag = response_data[0]
	valid = response_data[1]
	if ($("#campaign-create-form").isValid() == true && dial_method_flag && valid) {
		$.ajax({
			type: 'post',
			headers: {"X-CSRFToken": csrf_token},
			url: '/CampaignManagement/Campaign/create/',
			data: $('#campaign-create-form').serialize(),
			success: function (data) {
				showSwal('success-message', 'Campaign Created Successfully', '/CampaignManagement/Campaigns/')
			},
			error: function (data) {
				if (data["responseJSON"]["errors"]) {
					$("#campaign-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
					setTimeout(function(){ $("#campaign-err-msg").addClass("d-none") }, 3000);
				}			
			}
		});
	}
})
$("#campaign-name").keyup(function(){
	var current_val = $(this).val()
	$(this).val(current_val.trim())
	$("#campaign-slug").val($(this).val().trim())
})

$(".edit-campaign-btn, #edit-campaign-settings-btn").click(function() {
	response_data = campaign_pre_save_validation("#campaign-edit-form")
	dial_method_flag = response_data[0]
	var valid = response_data[1]
	var empty_lead = response_data[2]
	if (empty_lead) {
		$("#lead-err-msg").text("Select lead name").removeClass("d-none")
		setTimeout(function(){ $("#lead-err-msg").addClass("d-none") }, 3000);
	}
	else {
		if ($("#campaign-edit-form").isValid() == true && dial_method_flag && valid) {
			$.ajax({
				type: 'put',
				headers: {"X-CSRFToken": csrf_token},
				url: '/CampaignManagement/Campaign/'+campaign_id+'/',
				data: $('#campaign-edit-form').serialize(),
				success: function (data) {
					showSwal('success-message', 'Campaign Updated Successfully', "/CampaignManagement/Campaigns/")
				},
				error: function (data) {
					if (data["responseJSON"]["errors"]) {
						$("#campaign-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
						setTimeout(function(){ $("#campaign-err-msg").addClass("d-none") }, 3000);
					}	
				}
			});
		}
	}
})
$(document).on('change','.lead_name',function(e){
	if($(".lead_name option:selected[value='"+$(this).val()+"']").length > 1) {
		  $(this).val("Select Disposition")
	}
	var current_element = $(this).attr("id").split("-")[1]
	if($(this).val() != "Select Disposition") {
		$("#lead-heading-"+current_element).find('a').text("Lead Recycle-"+$(this).val())
	}
	else {
		$("#lead-heading-"+current_element).find('a').text("Lead Recycle")	
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
		if (start_time!='' && stop_time!=''){
			timings = {}
			timings['start_time'] = start_time
			timings['stop_time'] = stop_time
			timings['audio_file_name'] = audio_file_name
			calltimes_form_data[value] = timings
		}else if(start_time != '' && stop_time == ''){
			$('#'+value+'_stop_err_msg').html("Stop time is need...").removeClass("d-none");
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
	});
	if (stop_ajax == false) {
		calltimes_form_data=JSON.stringify(calltimes_form_data)
		$('#schedule_time').val(calltimes_form_data);
		var pk = $('#calltime_id').val()
		if(pk){
			type = "put"
			url = '/CampaignManagement/CampaignSchedule/'+pk+'/'
		}else{
			type = 'post'
			url = '/CampaignManagement/CampaignSchedule/create/'
		}
		if ($("#calltime-create-form").isValid() == true ) {
			$.ajax({
				type: type,
				headers: {"X-CSRFToken": csrf_token},
				url: url,
				data: $('#calltime-create-form').serialize(),
				success: function (data) {
					if ("msg" in data) {
						$("#calltime-err-msg").text(data["msg"]).removeClass("d-none")
						setTimeout(function(){ $("#calltime-err-msg").addClass("d-none") }, 3000);
					}
					else {
						showSwal('success-message', data["success"],"/CampaignManagement/CampaignSchedule/")
					}
				},
				error: function (data) {
					$("#calltime-name").removeClass("valid").addClass("error")
					$("#calltime-name-error").removeClass("has-success").addClass("has-error")
					$("#calltime-name-error").html("<span class='help-block form-error'>"+data["responseJSON"]["name"]+"</span>")
				// $("#calltime-name-error").text(data["responseJSON"]["errors"]["name"])
			}
		});
		}
	}
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
			success: function (data) {
				showSwal('success-message', 'User Updated Successfully', '/UserManagement/Users/')
			},
			error: function (data) {
				if (data["responseJSON"]["errors"]) {
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
	if ($("#phone-edit-form").isValid() == true ) {
		$.ajax({
			type: 'put',
			headers: {"X-CSRFToken": csrf_token},
			url: '/UserManagement/edit-phone/'+phone_id+'/',
			data: $('#phone-edit-form').serialize(),
			success: function (data) {
				showSwal('success-message', 'Phone Updated Successfully', '/UserManagement/Users/')
			},
			error: function (data) {
				if (data["responseJSON"]["errors"]) {
					$("#phone-err-msg").text(data["responseJSON"]["errors"]).removeClass("d-none")
					setTimeout(function(){ $("#phone-err-msg").addClass("d-none") }, 3000);
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
		if($('#audio-upload-form').hasClass("edit-audio")) {
		var current_id = $("#audio-id").val()
		url = '/CampaignManagement/edit-audio/'+current_id+'/'
	}
	else {
		url = '/CampaignManagement/upload-audio-file/'
	}
	var formData = new FormData($("#audio-upload-form")[0]);
	var valid = true
	var fileExtension = ['MP3', 'mp3', 'OGG', 'ogg'];
	if ($(".dropify-filename-inner").text() != "") {
		if ($.inArray($(".dropify-filename-inner").text().split('.').pop().toLowerCase(), fileExtension) == -1) {
			$("#file-extension-msg").removeClass("d-none").text("File formats must be mp3, ogg")
			setTimeout(function(){ $("#file-extension-msg").addClass("d-none") }, 3000);
			valid = false
		}
	}
	if ($("#audio-upload-form").isValid() == true && valid == true ) {
		$.ajax({
			url : url,
			type : 'POST',
			data : formData,
			processData: false, 
			contentType: false,
			success : function(data) {
				showSwal('success-message', 'Audio File Uploaded Successfully')
			},
			error: function (data) {
				if (data["responseJSON"]["name"]) {
					$("#name-error").addClass("has-error").html(
						'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>')
					setTimeout(function(){ $("#name-error").addClass("d-none") }, 3000);
				}
			}

		});
	}
}
});
// This function is used to save audio files
$("#create-audio-file, .edit-audio").click(function() {
	if($(this).hasClass("edit-udio")) {
		var current_id = $("#audio-id").val()
		url = '/CampaignManagement/edit-audio/'+current_id+'/'
	}
	else {
		url = '/CampaignManagement/upload-audio-file/'
	}
	var formData = new FormData($("#audio-upload-form")[0]);
	var valid = true
	var fileExtension = ['MP3', 'mp3', 'OGG', 'ogg'];
	if ($(".dropify-filename-inner").text() != "") {
		if ($.inArray($(".dropify-filename-inner").text().split('.').pop().toLowerCase(), fileExtension) == -1) {
			$("#file-extension-msg").removeClass("d-none").text("File formats must be mp3, ogg")
			setTimeout(function(){ $("#file-extension-msg").addClass("d-none") }, 3000);
			valid = false
		}
	}
	if ($("#audio-upload-form").isValid() == true && valid == true ) {
		$.ajax({
			url : url,
			type : 'POST',
			data : formData,
			processData: false, 
			contentType: false,
			success : function(data) {
				showSwal('success-message', 'Audio File Uploaded Successfully')
			},
			error: function (data) {
				if (data["responseJSON"]["name"]) {
					$("#name-error").addClass("has-error").html(
						'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>')
					setTimeout(function(){ $("#name-error").addClass("d-none") }, 3000);
				}
			}

		});
	}
})
$(document).on('click','.modify-audio-file',function(){
	$(".dtr-bs-modal").modal('hide');
	var current_id = $(this).attr("id").split("-")[2]
	$.ajax({
		type: 'GET',
		headers: {"X-CSRFToken": csrf_token},
		url: '/CampaignManagement/edit-audio/'+current_id+'/',
		data: {},
		success: function (data) {
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
		error: function (data) {
			if (data["responseJSON"]["name"]) {
				$("#name-error").addClass("has-error").html(
					'<span class="help-block form-error">'+data["responseJSON"]["name"]+'</span>').removeClass(
					"d-none")
					setTimeout(function(){ $("#name-error").addClass("d-none") }, 3000);
				}	
			}
		});

})
$("#audio-wizard-modal").on('hidden.bs.modal', function () {
	$("#audio-upload-form")[0].reset();
	$(".dropify-clear").click()
});

$("#fileupload-wizard-modal").on('hidden.bs.modal', function () {
	$("#user-upload-form")[0].reset();
	$(".dropify-clear").click()
});

$("#audio-wizard-modal").on('hidden.bs.modal', function () {
	$("#audio-upload-form")[0].reset();
	$("#uploaded_file").addClass("d-none")
	$(".dropify-clear").click()
});
// script block starts here
$("#script-submit-btn").click(function() {
	$(".selected-departments .badge-pill").each(function(){ 
		$('#script-create-form').append("<input type='hidden' name='dept' value='"+$(this).attr("data-id")+"'>")
	})
	// var script_data = $("#summernoteExample").summernote('code');
	var script_data = tinyMCE.get('tinyMceExample').getContent();
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

// This function is used to perform delete operation for all activities
function perform_delete(delete_type) {
	data = {}
	data["perform_operation"] = delete_type	
	if (delete_highp == true) {
		data["select_all"] = true
	}
	else if (delete_type.indexOf("particular_entry") != -1) {
		data["perform_operation"] = "delete"
		var id = delete_type.split("-")[1]
		result.push(id)
	}
	data["model_name"] = $("#model_name").val()
	data["app_name"] = $("#app_name").val()
	data["selected_entry"] = result
	$.ajax({
		type: 'POST',
		headers: {"X-CSRFToken": csrf_token},
		url: '/api/delete-selected-entry/',
		data: data,
		success: function (data) {
			if (delete_type == "enable") {
				showSwal('success-message', 'Selected Entries Are Enabled')
			}
			else if (delete_type == "disable") {
				showSwal('success-message', 'Selected Entries Are Disabled')
			}
			else {
				showSwal('success-message', 'Selected Entries Are Deleted')
			}
		},
		error: function (data) {
			
		}
	});
}
// ends delete block

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

// to checked read permission if other permission are checked in user role
$(document).on('click','.permission_input',function(){
	if($(this).prop("checked")) {
			$(this).closest("div").siblings().find("#R").prop( "checked", true )
	}else{
		if($(this).prop("id")== "R"){
			$(this).closest("div").siblings().find("#C,#U,#D").prop( "checked", false )
		}
	}
});
$("#additional_settings").change(function(){
	if ($(this).val() == 'custom'){
		$("#select_range_div").removeClass("d-none")
	}
	else {
		$("#select_range_div").addClass("d-none")	
		$("#custom-range").val("")
	}
})
$.fn.select2.amd.require(['select2/selection/search'], function (Search) {
	var oldRemoveChoice = Search.prototype.searchRemoveChoice;

	Search.prototype.searchRemoveChoice = function () {
		oldRemoveChoice.apply(this, arguments);
		this.$search.val('');
	};
	$('#users, #phone_extensions, #call_mode, #user-group, #group, #user_timezone, .select2-class, #transfer_call, #contact_phonebook_select, #contact_campaign_select, #contact_campaign_select, #crm_field_campaign, #contact_column_select').select2();
});
$("#modal_add_group, #modal_update_group").on('hidden.bs.modal', function () {
	$("form")[0].reset();
});
$(document).on('change','#schedule_type',function(){
	var parent = $(this).attr("data-parent")
	if ($(this).val() == "schedule_time") {
		$("#lead-card-"+parent).find("#lead-start-time, #lead-end-time").removeClass("d-none")
		$("#lead-card-"+parent).find("#lead-time-div").addClass("d-none").val("0")
		$("#lead-card-"+parent).find("#lead_time").val("0")
		
	}
	else if ($(this).val() == "recycle_time") {
		$("#lead-card-"+parent).find("#lead-start-time, #lead-end-time").addClass("d-none")	
		$("#lead-card-"+parent).find("#lr_start_time, #lr_end_time").val("")
		$("#lead-card-"+parent).find("#lead-time-div").removeClass("d-none")
	}
	else {
		$("#lead-card-"+parent).find("#lead-start-time, #lead-end-time, #lead-time-div").addClass("d-none")	
		$("#lead-card-"+parent).find("#lr_start_time, #lr_end_time").val("")
		$("#lead-card-"+parent).find("#lead_time").val("0")
	}
})
// this function is used to set lead section name
$(document).on('blur', '#lr_start_time', function() {
	var parent = $(this).attr("data-parent").split("-")[2]
	var lead_name = $(parent).find(".lead_name").val()
	$(parent).find(".lr_start_time").val("")
	var frequency = $(parent).find("#count").val()
	$(parent).find("a").text(lead_name+"-"+"from "+$(this).val()+ "recycle frequency-"+frequency)
})

$(document).on('blur', '#lr_end_time', function() {
	var parent = $(this).attr("data-parent").split("-")[2]
	var lead_name = $(parent).find(".lead_name").val()
	var start_time = $(parent).find(".lr_start_time").val()
	var frequency = $(parent).find("#count").val()
	$(parent).find("a").text(lead_name+"-"+"start from "+start_time+" end to "+$(this).val())
})

$("#add-lead-btn").click(function() {
	$("#accordion").find(".lead-heading").attr("aria-expanded",false)
	$("#accordion").find(".collapse-div").removeClass("show")
	var cloned_div = $("#lead-card-1").clone()
	var count = parseInt($("#get-count").val())+1
	$("#get-count").val(count)
	cloned_div.find('.schedule_type').val('Select Time'); 
	cloned_div.find('.lead_name').val('Select Disposition').attr("id", "lead_name-"+count); 
	cloned_div.find("#lead-heading-1").attr("id", "lead-heading-"+count)
	cloned_div.find(".remove-lead").removeClass("d-none").attr("id", "remove-lead-"+count)
	// cloned_div.find(".lead-heading").attr({"href":"#lead-collaps-"+count, "aria-expanded":true}).text("Recycle Lead-"+count)
	cloned_div.find(".lead-heading").attr({"href":"#lead-collaps-"+count, "aria-expanded":true}).text("Lead Recycle")
	cloned_div.find("#lead-collaps-1").attr({"aria-labelledby":"lead-heading-"+count, "id":"lead-collaps-"+count}).addClass("show")
	cloned_div.find("#schedule_type").attr("data-parent",count)
	cloned_div.find("#start_timepicker_1 div").find('input').attr("data-target","#start_timepicker_"+count).val("").attr("data-parent", "#lead-card-"+count)
	cloned_div.find("#start_timepicker_1 div").attr("data-target","#start_timepicker_"+count)
	cloned_div.find("#start_timepicker_1").attr("id","start_timepicker_"+count)
	cloned_div.find("#end_timepicker_1 div").find('input').attr("data-target","#end_timepicker_"+count).val("").attr("data-parent", "#lead-card-"+count)
	cloned_div.find("#end_timepicker_1 div").attr("data-target","#end_timepicker_"+count)
	cloned_div.find("#end_timepicker_1").attr("id","end_timepicker_"+count)
	cloned_div.find("#lead-start-time, #lead-end-time, #lead-time-div").addClass("d-none")
	cloned_div.find("#lead_time, #count").val(0)
	cloned_div.attr("id", "lead-card-"+count)
	$("#accordion").append(cloned_div)
	$(".lr-start-time, .lr-end-time").datetimepicker({
		format: 'HH:mm'
	});
})
$(document).on('click','.remove-lead',function(){
	var current_element = $(this).attr("id")
	var parent_id = current_element.split("-")[2]
	var delete_lead_id = $(this).attr("data-lead_id")
	if(delete_lead_id) {
		$("#campaign-edit-form").append("<input type='hidden' name='delete_lead_id' value='"+delete_lead_id+"'>")
	}
	if($('#accordion').children('div').length > 1 ) {
		var count = parseInt($("#get-count").val())-1
		$("#get-count").val(count)
		$("#start_timepicker_"+parent_id+", #end_timepicker_"+parent_id).data("datetimepicker").destroy();
		$("#lead-card-"+parent_id).remove()
		$('#accordion').children('div').each(function (i,current_child) {
			var child_id = $(this).attr("id").split("-")[2]
			i = i +1
			var lead_name = $(this).find(".lead_name").val()
			if (lead_name == "Select Disposition") {
				lead_name = ""
			}
			$(this).find(".card-header").attr("id", "lead-heading-"+i)
			$(this).find(".remove-lead").removeClass("d-none").attr("id", "remove-lead-"+i)
			if (lead_name) {
				$(this).find(".lead-heading").attr({"href":"#lead-collaps-"+i, "aria-expanded":true}).text("Lead Recycle-"+lead_name)
			}
			else {
				$(this).find(".lead-heading").attr({"href":"#lead-collaps-"+i, "aria-expanded":true}).text("Lead Recycle")	
			}
			$(this).find(".collapse-div").attr({"aria-labelledby":"lead-heading-"+i, "id":"lead-collaps-"+i}).addClass("show")
			$(this).attr("id", "lead-card-"+i)
			$(this).find("#schedule_type").attr("data-parent", i)
			$(this).find(".lead_name").attr("id", "lead_name-"+i)
			$(this).find(".lr-start-time").attr("id","start_timepicker_"+i)
			$(this).find(".lr-start-time div").attr("data-target","#start_timepicker_"+i)
			$(this).find(".lr-start-time div").find('input').attr("data-target","#start_timepicker_"+i)
			$(this).find(".lr-end-time").attr("id","end_timepicker_"+i)
			$(this).find(".lr-end-time div").attr("data-target","#end_timepicker_"+i)
			$(this).find(".lr-end-time div").find('input').attr("data-target","#end_timepicker_"+i)
			$("#start_timepicker_"+i+", #end_timepicker_"+i).datetimepicker({
				format: 'HH:mm'
			});
		});
		$("#accordion").find(".lead-heading").attr("aria-expanded",false)
		$("#accordion").find(".collapse-div").removeClass("show")
	}
	else {
		$("#lead-card-"+parent_id).find('#schedule_type').val('Select Time'); 
		$("#lead-card-"+parent_id).find('.lead_name').val('Select Disposition'); 
		$("#lead-heading-"+parent_id).find("a").text("Lead Recycle")
		$("#lead-card-"+parent_id).find('input:text').val('');
		$("#lead-collaps-"+parent_id).addClass("show")
		$("#lead-card-"+parent_id).find('#count').val(0)
		$("#lead-collaps-"+parent_id).find("#lead-start-time, #lead-end-time, #lead-time-div").addClass("d-none")
	}

});
var avail_dispo_list = []
$("#lead-settings-tab").click(function() {
	required_dispo = true
	if ($(".selected-disposition .badge-pill").length == 0){
		required_dispo =false
	}
	var dial_method = false
	if ($("#campaign_inbound").prop("checked") == true || $("#campaign_mannual").prop("checked") == true || $("#camp_outbound").val() !="false") {
		dial_method = true
	}
	else {
		$("#dial_method_msg").removeClass("d-none")
	}
	if ($("#campaign-create-form").isValid() && required_dispo && dial_method) {
		avail_dispo_list = []
		$(".lead_name option").remove();
		$(".lead_name").append("<option value='Select Disposition'>Select Disposition</option>")
		$(".selected-disposition .badge-pill").each(function(){ 
			avail_dispo_list.push($(this).text())
			$(".lead_name").append("<option value='"+$(this).text()+"'>"+$(this).text()+"</option>")
		})
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
		$("#dispo-err-msg").removeClass("d-none")
	}
})

$("#camp_outbound_check").click(function() {
	if($(this).prop("checked")) {
		$("#camp_outbound").removeClass("d-none")
	}
	else {
		$("#camp_outbound").addClass("d-none")	
		$("#camp_outbound").val("false")
	}
})
$("#campaign-settings-tab").click(function() {
	if ($("#campaign-edit-form").isValid()) {
		$(this).attr("href", "#campaign-additional-settings")
		$(".tab-pane").removeClass("show active")
		$("#campaign-additional-settings").addClass("show active")
	}
})

$(".crm-fields-modify").click(function() {
	var id = $(this).attr("id").split("-")[2]
	$.ajax({
		type: 'POST',
		headers: {"X-CSRFToken": csrf_token},
		url: '/Administration/CrmField/edit/'+id+'/',
		success: function (data) {
			if (['dropdown','radio'].includes(data["field_type"])){
				$("#edit-crm-field-modal").find("#field_options_div").removeClass("d-none");
				$("#edit-crm-field-modal").find("#field_options").val(data["options"]);
			}
			else if(['text','textarea','integer'].includes(data["field_type"])){
				$("#edit-crm-field-modal").find("#field_size_div").removeClass("d-none");
				$("#edit-crm-field-modal").find("#field_size").val(data["size"]);
			}
			$("#edit-crm-field-modal").find("#field").val(data["field"]);
			$("#edit-crm-field-modal").find("#field_type").val(data["field_type"]);
			$("#edit-crm-field-modal").find("#editable").prop("checked", data["editable"]);
			$("#edit-crm-field-modal").find("#field_priority").val(data["priority"]);
			$("#edit-crm-field-modal").find("#field_status").val(data["status"]);
			$("#edit-crm-field-modal").modal('show');
			$("#edit-crm-field-modal").find(".update-crm-fields").attr("id", "update-crm-fields-"+id)
		},
		error: function (data) {
		}
	});
})
$("#edit-crm-field-modal").on('hidden.bs.modal', function () {
	$("#update-crm-fields-form")[0].reset();
	$(this).find("#field_size_div, #field_options_div").addClass("d-none");
	});
var CrmFieldWizard = $("#update-crm-fields-form");
CrmFieldWizard.children("div").steps({
	headerTag: "h3",
	bodyTag: "section",
	transitionEffect: "slideLeft",
	onFinished: function(event, currentIndex) {
	}
});
$(document).on('click','.update-crm-fields',function(){
	var current_element = $(this).attr("id").split("-")[3]
	var form = $("#update-crm-fields-form").serialize()
	$.ajax({
		type: 'put',
		headers: {"X-CSRFToken": csrf_token},
		url: '/Administration/CrmField/edit/'+current_element+'/',
		data: form,
		success: function (data) {
			showSwal('success-message', 'CRM fields updated successfully')
		},
		error: function (data) {
			if ("field" in data["responseJSON"]) {
				$("#field-msg").addClass("has-error").html(
					'<span class="help-block form-error">'+data["responseJSON"]["field"]+'</span>').removeClass("d-none")
				setTimeout(function(){ $("#field-msg").addClass("d-none") }, 3000);
			}
		}
	});

})

$("#sample_phonebook").click(function() {
	var campaign_name = $("#phonebook-campaign :selected").attr("data-name")
	if(campaign_name){
		var url = '/CRM/get-sample-phonebook/'+campaign_name+'/'
		$(this).attr("href", url)
	}
	else{
		$('#phonebook-err-msg').text("Please select campaign first").removeClass('d-none')
		setTimeout(function(){ $('#phonebook-err-msg').addClass("d-none") }, 5000);
	}

})

function dynamic_phonebook(selected_phonebook) {
	var campaign = $("#contact_campaign_select").val()
	$("#contact_phonebook_select").find("option").remove()
	if (selected_phonebook){
		$("#contact_phonebook_select").append(new Option("Select Phonebook", "", true, true))	
	}
	else {
		$("#contact_phonebook_select").append(new Option("Select Phonebook", "", false, false))
	}
	$.each(phonebook_list, function( index, value ) {
		if(value.campaign == campaign) {
			if (selected_phonebook == value.id) {
				var new_op = new Option(value.name, value.id, true, true)
			}
			else {
				var new_op = new Option(value.name, value.id, false, false)
			}
			$("#contact_phonebook_select").append(new_op).trigger('change');
		}
	});

	$("#phonebook-div").removeClass("d-none")
}
$("#contact_campaign_select").change(function() {
	if ($(this).val() != "") {
		dynamic_phonebook("")
		if($(this).hasClass("call_contact_status")) {
			$.ajax({
				type: 'post',
				headers: {"X-CSRFToken": csrf_token},
				url: '/Contacts/get-contact-columns/',
				data: {"campaign": $(this).val()},
				success: function (data) {
					$("#column-div").removeClass("d-none")
					$("#filter_contacts_info").removeClass("d-none")
					$.each(data["columns"], function( index, value ) {
						var new_op = new Option(value, value, false, false)
						$("#column-div").find("#contact_column_select").append(new_op).trigger('change');
					});
				},
				error: function (data) {
					
				}
			});
		}
		else {
			$("#column-div").removeClass("d-none")
			$("#filter_contacts_info").removeClass("d-none")
		}
	}
	else {
		$("#phonebook-div, #column-div, #filter_contacts_info").addClass("d-none")
	}
})

$("#update-contact-btn").click(function() {
	var id = $(this).attr("data-contact-id")
	custom_raw_data = {}
	$(".section_div").each(function(){
		var section_name = $(this).attr("id")
		$(this).find("input").each(function(){
			custom_raw_data[$(this).attr("id")] = $(this).val() 
		})
	})
	$("#customer_raw_data").val(JSON.stringify(custom_raw_data))
	var form = $("#edit-contact-info").serialize()
	if( $("#edit-contact-info").isValid()) {
		$.ajax({
			type: 'post',
			headers: {"X-CSRFToken": csrf_token},
			url: '/CRM/ContactInfo/'+id+'/',
			data: form,
			success: function (data) {
				showSwal('success-message', 'Contact Detail Updated', '/CRM/ContactInfo/')
			},
			error: function (data) {
				
			}
		});
	}
})

$("#upload-ndnc").click(function() {
	var data = new FormData($('#ndnc-upload-form').get(0));
	var fileExtension = ['csv'];
	if ($(".dropify-filename-inner").text()) {
		if ($.inArray($(".dropify-filename-inner").text().split('.').pop().toLowerCase(), fileExtension) == -1) {
			$("#upload-file-error").text("File format must be csv").removeClass("d-none")
			setTimeout(function(){ $("#upload-file-error").addClass("d-none") }, 3000);
		}
		else {
			$.ajax({
				type: 'post',
				headers: {"X-CSRFToken": csrf_token},
				url: $('#ndnc-upload-form').attr('action'),
				cache: false,
				processData: false,
				contentType: false,
				data: data,
				success: function (data) {
					showSwal('success-message', 'NDNC uploaded successfully')
				},
				error: function (data) {
					
				}	
			});
		}
	}
	else {
		$("#upload-file-error").text("Upload File").removeClass("d-none")
		setTimeout(function(){ $("#upload-file-error").addClass("d-none") }, 3000);
	}
})

$("#cancel-ndnc-upload").click(function() {
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

$("#filter-report").click(function() {
	var start_date = moment($("#start-date input").val())
	var end_date = moment($("#end-date input").val())
	if (end_date<start_date) {
		$("#end-date-error").removeClass("d-none")
	}
	else {
		$("#call_details_flag").val("true")
		$("#report_form").submit()
		$("#end-date-error").addClass("d-none")
	}
})
$("#agent_report_campaign").change(function() {
	var campaign = $(this).val()
	$.ajax({
		type: 'post',
		headers: {"X-CSRFToken": csrf_token},
		url: '/api/get-campaign-users/',
		data: {"campaign": campaign},
		success: function (data) {
			$('#agent_activity_users').find('option').remove()
			$("#agent_activity_users").append(new Option("Select User", "", false, false))
				$.each(data["users"], function( index, value ) {
					$("#agent_activity_users").append(new Option(value["username"], value["id"], false, false))
				
				});
		},
		error: function (data) {
			
		}	
	});
})
