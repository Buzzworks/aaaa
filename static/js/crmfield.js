var unique_field_count = 0
$("#add-section").click(function() {
	$("#crmf-accordion").find(".collapse-div").removeClass("show")
	$("#crmf-accordion").find(".clone-crm-heading").attr("aria-expanded",false)
	var cloned_element = $("#clone-crm-section").clone()
	var count = parseInt($("#get-count").val())+1
	$("#get-count").val(count)
	cloned_element.removeClass("d-none")
	cloned_element.find(".clone-crm-heading").text("Section").attr("href", "#section-collapse-"+count)
	cloned_element.find(".remove-section").attr("id", "remove-section-"+count)
	cloned_element.find(".section_name").attr("data-parent", "#section-"+count)
	cloned_element.find(".section-priority").attr("data-parent", "#section-"+count)
	cloned_element.find("#clone-section-collapse").attr({"id":"section-collapse-"+count})
	cloned_element.attr("id", "section-"+count)
	cloned_element.find(".add-crm-field").attr("id", "add-crm-field-"+count)
	cloned_element.find(".crmfield-div").attr("id", "crmfield-div-"+count)
	cloned_element.find(".section-priority").attr({"data-validation-error-msg-container":"#priority-error-msg-"+count})
	cloned_element.find(".priority-msg").attr("id", "priority-error-msg-"+count)
	$("#crmf-accordion").append(cloned_element)  
})
$(document).on('keydown', '.section_name', function(e) {
	if(e.key === ":") { // disallow semicolon
        return false;
    }
})

$(document).on('change', '.section_name', function(e) {
	var current_ele = $(this)
	var current_val = $(this).val()
	var add_section = true
	current_ele.addClass("current")

	$("#crmf-accordion").children('div').each(function (i,current_child) { 
		if (!$(this).find(".section_name").hasClass("current")) {
			if (current_val.trim() == $(this).find(".section_name").val().trim()) {
				add_section = false
				current_ele.next().text("Section with this name already exist").addClass("text-danger")
				setTimeout(function(){ 
					current_ele.next().removeClass("text-danger").text("")
				}, 3000);
				current_ele.val("")
				return false			
			}
		}
		
	})
	current_ele.removeClass("current")

	if(add_section == true)
	{
		var data_parent = $(this).attr("data-parent")
		var current_id = data_parent.split("-")[1]
		var priority = $(data_parent).find(".section-priority").val()
		if ($(this).val() != "") {
			if (priority) {
				$(data_parent).find("a[href$='#section-collapse-"+current_id+"']").text($(this).val()+"-"+priority)
			}
			else {
				$(data_parent).find("a[href$='#section-collapse-"+current_id+"']").text($(this).val())
			}
		}
		else {
			if (priority) {
				$(data_parent).find("a[href$='#section-collapse-"+current_id+"']").text("Section:"+priority)
			}
			else {
				$(data_parent).find("a[href$='#section-collapse-"+current_id+"']").text("Section")
			}
		}
    }
})

$(document).on('keyup mouseup', '.section-priority', function() {
	var data_parent = $(this).attr("data-parent")
	var previous_text = $(data_parent).find(".section_name").val()
	var current_id = data_parent.split("-")[1]
	var curr_block = $(this)
	if ($(this).val() != "") {
		if (/^0/.test(curr_block.val()) == false) {
			if (previous_text) {
				$(data_parent).find("a[href$='#section-collapse-"+current_id+"']").text(previous_text+":"+$(this).val())
			}
			else {
				$(data_parent).find("a[href$='#section-collapse-"+current_id+"']").text("Section:"+$(this).val())	
			}
		}
		else {
			curr_block.next().text("Priority should be minimum 1").addClass("text-danger")
			setTimeout(function(){ 
				curr_block.next().removeClass("text-danger").text("")
			 }, 3000);
			curr_block.val("")
		}
	}
	else {
		var section_name = $(data_parent).find(".section_name").val()
		if (section_name) {
			$(data_parent).find("a[href$='#section-collapse-"+current_id+"']").text(section_name)
		}
		else {
			$(data_parent).find("a[href$='#section-collapse-"+current_id+"']").text("Section")	
		}
	}
})

$(document).on('keyup mouseup', '#field_size', function() {
	var curr_block = $(this)
	if (/^0/.test(curr_block.val()) == true) {
		curr_block.next().text("Size should no be 0").addClass("text-danger")
		setTimeout(function(){ 
			curr_block.next().removeClass("text-danger").text("")
		 }, 3000);
		curr_block.val("")
	}

})

// This function is used to add crm field to particular section
$(document).on('click','.add-crm-field',function(){
	var id = $(this).attr("id").split("-")[3]
	$("#section-collapse-"+id).find(".crmfield-div").find(".collapse-div").removeClass("show")
	$("#section-collapse-"+id).find(".crmfield-div").find('a[aria-expanded="true"]').click();
	var cloned_element = $("#clone-crmf-card").clone()
	var crm_field_count = parseInt($("#section-collapse-"+id).find(".crmfield-div #crmfield-count").val())+1
	$("#section-collapse-"+id).find(".crmfield-div #crmfield-count").val(crm_field_count)
	cloned_element.attr("id", `crmf-card-${id}-${crm_field_count}`)
	cloned_element.find('.card-header').attr("id", `crmf-heading-${id}-${crm_field_count}`);
	cloned_element.find('.card-header a').attr("href",'#crmf-collapse-'+id+"-"+crm_field_count).text("Field");
	cloned_element.find('.collapse').attr({
		"id":"crmf-collapse-"+id+"-"+crm_field_count,
		"aria-labelledby":`crmf-heading-${id}-${crm_field_count}`,
		"data-parent":"#crmfield-div-"+id
	});
	cloned_element.find('.crm-fields').attr("id","crm-field-"+crm_field_count);
	cloned_element.find('.field_name, .field_priority').attr({
		"data-parent":`#crmf-card-${id}-${crm_field_count}`,
		"data-master":`#crmfield-div-${id}`
	})
	cloned_element.find("#field_type").attr({
		"data-parent" : "#crmf-collapse-"+id+"-"+crm_field_count,
		"data-master" : "#crmfield-div-"+id
	})
	cloned_element.removeClass("d-none")
	cloned_element.find(".field_priority").attr({
		"data-validation-error-msg-container":"#field-priority-error-msg-"+id+"-"+crm_field_count
	})
	cloned_element.find(".field-priority-msg").attr("id", "field-priority-error-msg-"+id+"-"+crm_field_count)
	cloned_element.find(".remove-crmfield").attr("id", "remove-crmfield-"+id+"-"+crm_field_count)
	cloned_element.find(".crm-color-picker").asColorPicker();
	cloned_element.find(".unique_fields_check").attr("id","unique_field_"+id+"_"+crm_field_count)
	cloned_element.find(".unique_fields_check_error").attr("id","unique_field_"+id+"_"+crm_field_count+"_error")
	cloned_element.find(".required_fields_check").attr("id","required_field_"+id+"_"+crm_field_count)
	cloned_element.find(".editable_fields_check").attr("data-id","editable_field_"+id+"_"+crm_field_count)
	$("#section-collapse-"+id).find(".crmfield-div").append(cloned_element)
})

// on change of field name change heading of field
$(document).on('change', '.field_name', function() {

	var data_master = $(this).attr("data-master")
	var data_parent = $(this).attr("data-parent")
	current_ele = $(this)
	current_ele.addClass("current")
	current_val = $(this).val()
	add_field = true
	$(data_master).children('div').each(function (i,current_child) { 
		if (!$(this).find(".field_name").hasClass("current")) {
			if (current_val.trim() == $(this).find(".field_name").val().trim()) {
				add_field = false
				current_ele.next().text("Field with this name already exist in this section").addClass("text-danger")
				setTimeout(function(){ 
						current_ele.next().removeClass("text-danger").text("")
					 }, 3000);
				return false			
				current_ele.val("")
			}
		}
		
	})
	current_ele.removeClass("current")

})

$(document).on('keyup mouseup keydown', '.field_name', function(e) {
	if(e.key === ":") { // disallow semicolon
        return false;
    }
    else {
    	var data_master = $(this).attr("data-master")
		var data_parent = $(this).attr("data-parent")
		var priority = $(data_master).find(data_parent).find(".field_priority").val()
		if ($(this).val() != "") {
			if (priority) {
				$(data_master).find(data_parent).find("a").text($(this).val()+"-"+priority)
			}
			else {
				$(data_master).find(data_parent).find("a").text($(this).val())
			}
		}
		else {
			if (priority) {
				$(data_master).find(data_parent).find("a").text("Field:"+priority)
			}
			else {
				$(data_master).find(data_parent).find("a").text("Field")
			}
		}
    		
    }
})

// on change of priority append it to heading of field
$(document).on('keyup mouseup', '.field_priority', function() {
	var data_parent = $(this).attr("data-parent")
	var data_master = $(this).attr("data-master")
	var previous_text = $(data_master).find(data_parent).find(".field_name").val()
	var current_block = $(this)
	if ($(this).val() != "") {
		if (/^0/.test(current_block.val()) == false) {
			if (previous_text) {
				$(data_master).find(data_parent).find("a").text(previous_text+":"+$(this).val())
			}
			else {
				$(data_master).find(data_parent).find("a").text("Field:"+$(this).val())	
			}
		}
		else {
			current_block.next().text("Priority should be minimum 1").addClass("text-danger")
			setTimeout(function(){ 
				current_block.next().removeClass("text-danger").text("")
			 }, 3000);
			current_block.val("")
		}
	}
	else {
		var field_name = $(data_master).find(data_parent).find(".field_name").val()
		var section_name = $(data_parent).find(".section_name").val()
		if (field_name) {
			$(data_master).find(data_parent).find("a").text(field_name)
		}
		else {
			$(data_master).find(data_parent).find("a").text("Field")	
		}


	}
})
// Onchange functionality on field type
data_types = {"text":["textarea"],"textarea":["text"],"integer":["text","textarea","float"],"float":["text","textarea"],
"datetimefield":["text","textarea","datefield","timefield"],"datefield":["text","textarea","datetimefield","timefield"],
"timefield":["text","textarea"],"dropdown":["multiselect","radio","multicheckbox"], "multiselect":["dropdown","radio","multicheckbox"],
"radio":["dropdown","multiselect", "multicheckbox"],
"checkbox":[],"multicheckbox":["multiselect","radio","dropdown"],
}
$(document).on('change','#field_type', function(){
	var parent_div = $(this).attr("data-parent");
	var current_type = $(this).find("option:selected").val();
	var old_value = $(this).attr("data-old_value");
	var span_id = $(this).attr("data-span_id");
	if ($.inArray(current_type,data_types[old_value]) ==-1 && current_type!=old_value && is_editable && old_value!=undefined){
		$(span_id).text("You can not select this type").addClass("text-danger")
		setTimeout(function(){ 
			$(span_id).removeClass("d-none").text("") 
		}, 3000);
		$(this).val(old_value)
		current_type = old_value
	}
	else {
		if (['dropdown','radio', 'multiselect', 'multicheckbox'].includes(current_type)){
			$(parent_div).find("#field_options_div").removeClass("d-none");
			$(parent_div).find("#field_size_div").addClass("d-none");
			$(parent_div).find("#field_options").val("");
			$(parent_div).find("#field_size").val("0");
			if (current_type) {
				$(parent_div).find("#field_options").tooltip();  
			}
		}
		else if(['text','textarea','integer','float'].includes(current_type)){
			$(parent_div).find("#field_size_div").removeClass("d-none");
			$(parent_div).find("#field_options_div").addClass("d-none");
			$(parent_div).find("#field_size, #field_options").val("");
		}
		else{
			$(parent_div).find("#field_size_div, #field_options_div").addClass("d-none");
			$(parent_div).find("#field_options").val("");
			$(parent_div).find("#field_size").val("0");
		}
	}
})
var section_priority = []
function validate_priority(){
	// section_priority = []
	var flag = false
	var count = parseInt($("#get-count").val())
	$("#crmf-accordion").children('div').each(function (i,current_child) { 
		var er_id = $(this).find(".section-priority").attr("data-validation-error-msg-container")
		console.log(er_id, "id")
		if($.inArray($(this).find(".section-priority").val(), section_priority) == -1){
			var priority = $(this).find(".section-priority").val()
			if (priority < count) {
				section_priority.push(priority)
				$(er_id).text("").removeClass("form-error")
			}
		}
	})
}
// $(document).on('blur','.section-priority', function(){
// 	var error_msg_id = $(this).attr("data-validation-error-msg-container")
// 	var id = error_msg_id.split("-")[3]
// 	var current_val = $(this).val()
// 	var flag = false
// 	$("#crmf-accordion").children('div').not("#section-"+id).each(function (i,current_child) { 
// 		if($(this).find(".section-priority").val() == current_val ) {
// 			flag = true
// 			// break;
// 			return false
// 		}
// 		else {
// 			flag = false
// 		}
// 	})
// 	if (flag) {
// 		$(error_msg_id).addClass("help-block form-error").text("Section with this priority already present")
// 	}
// 	else {
// 		$(error_msg_id).removeClass("help-block form-error").text("")
// 	}
// })

var field_priority = []
// $(document).on('blur','.field_priority', function(){
// 	var error_msg_id = $(this).attr("data-validation-error-msg-container")
// 	var parent_id = $(this).attr("data-validation-error-msg-container").split("-")[4]
// 	field_priority = []
// 	$("#section-collapse-"+parent_id).find(".crmfield-div").children('div').each(function (i,current_child) {
// 		if($.inArray($(this).find(".field_priority").val(), field_priority) == -1){
// 			field_priority.push($(this).find(".field_priority").val())
// 			$(error_msg_id).removeClass("help-block form-error").text("")
// 		}
// 		else {
// 			$(error_msg_id).addClass("help-block form-error").text("Section with this priority already present")
// 			return false
// 		}
// 	})
	
// })
// to remove crm-field-create div from particular section
$(document).on('click','.remove-crmfield',function(){
	var parent_id = $(this).attr("id").split("-")[2]
	var current_count = $(this).attr("id").split("-")[3]
	var current_element = $(`#crmf-card-${parent_id}-${current_count}`);
	if(current_element.find('.unique_fields_check').prop('checked') && unique_field_count > 0){
		unique_field_count -= 1
	}
	var next_elements = current_element.nextAll();
	jQuery.each(next_elements,function(){
		$(this).attr("id",`crmf-card-${parent_id}-${current_count}`)
		$(this).find('.card-header').attr("id", `crmf-heading-${parent_id}-${current_count}`);
		var field_name = ""
		var field_priority = $(this).find(".field_priority").val()
		if ($(this).find(".field_name").val() != "") {
			field_name = $(this).find(".field_name").val()
			if (field_priority) {
				field_name = field_name+":"+field_priority
			}
		}
		else {
			field_name = "Field:" + field_priority
		}
		$(this).find('.card-header a').attr("href",'#crmf-collapse-'+parent_id+"-"+current_count).text(field_name);
		$(this).find('.collapse-div').attr({
			"id":"crmf-collapse-"+parent_id+"-"+current_count,
			"aria-labelledby":`crmf-heading-${parent_id}-${current_count}`,
		});
		$(this).find('.crm-fields').attr("id","crm-field-"+current_count);
		$(this).find(".remove-crmfield").attr("id", "remove-crmfield-"+parent_id+"-"+current_count)

		$(this).find("#field_type").attr("data-parent","#crmf-collapse-"+parent_id+"-"+current_count)
		$(this).find(".field_name, .field_priority").attr("data-parent", `#crmf-card-${parent_id}-${current_count}`)
		$(this).find(".unique_fields_check").attr("id","unique_field_"+parent_id+"_"+current_count)
		$(this).find(".required_fields_check").attr("id","required_field_"+parent_id+"_"+current_count)
		$(this).find(".editable_fields_check").attr("data-id","editable_field_"+parent_id+"_"+current_count)
		$(this).find(".unique_fields_check_error").attr("id","unique_field_"+parent_id+"_"+current_count+"_error")
		// $(this).find(".field_priority").tooltip('dispose');
		// $(this).find(".field_priority").attr({"title":"Priority should be between 1-"+current_count,
		// "data-parent":"crmf-card-"+current_count }).tooltip();  
		current_count++;
	});
	current_element.hide('slow',function(){current_element.remove();});
	$("#crmfield-count").val(current_count-1)
})

$(document).on('click','.remove-section',function(){
	var current_count = $(this).attr("id").split("-")[2]
	var current_element = $("#section-"+current_count);
	jQuery.each(current_element.find('.unique_fields_check'), function(){
		if($(this).prop('checked') && unique_field_count > 0){
			unique_field_count -= 1
		}
	})
	var next_elements = current_element.nextAll();
	var count = parseInt($("#get-count").val()-1)
	$("#get-count").val(count)
	jQuery.each(next_elements,function(){
		$(this).attr("id","section-"+current_count)
		var section_name = "Section"
		if($(this).find(".section_name").val() != "") {
			section_name = $(this).find(".section_name").val()
			if($(this).find(".section-priority") != "") {
				var section_priority = $(this).find(".section-priority").val()
				section_name = section_name+":"+section_priority
			}
		}
		else {
			section_name = "Section"
			if($(this).find(".section-priority") != "") {
				var section_priority = $(this).find(".section-priority").val()
				if(section_priority) {
					section_name = section_name+":"+section_priority
				}
			}
		}

		$(this).find(".clone-crm-heading").text(section_name).attr("href", "#section-collapse-"+current_count)
		$(this).find(".remove-section").attr("id", "remove-section-"+current_count)
		$(this).find(".collapse-div").attr("id", "section-collapse-"+current_count)
		$(this).find("#clone-section-collapse").attr({"id":"section-collapse-"+current_count})
		$(this).find(".add-crm-field").attr("id", "add-crm-field-"+current_count)
		$(this).find(".crmfield-div").attr("id", "crmfield-div-"+current_count)
		// $(this).find(".section-priority").tooltip('dispose');
		// if($(this).find(".section-priority").val() > count) {
		// 	var er_id = $(this).find(".section-priority").attr("data-validation-error-msg-container")
		// 	$(er_id).addClass("help-block form-error").text("This priority is not valid")
		// }
		$(this).find(".section-priority").attr({
			"data-parent":"#section-"+current_count,
			"data-validation-error-msg-container":"#priority-error-msg-"+current_count
		})
		$(this).find(".priority-msg").attr("id", "priority-error-msg-"+current_count)
		$(this).find(".crmfield-div").children('div').each(function (i,current_child) {
			var i = i +1
			$(this).attr("id",`crmf-card-${current_count}-${i}`)
			$(this).find('.card-header').attr("id", `crmf-heading-${current_count}-${i}`);
			var field_name = "Field"
			var field_priority = ""
			if ($(this).find(".field_name").val() != "") {
				field_name = $(this).find(".field_name").val()
				if($(this).find(".field_priority").val() != "") {
					field_priority = $(this).find(".field_priority").val()
					field_name = field_name + ":"+field_priority
				}
			}
			else {
				field_name = "Field"
				if($(this).find(".field_priority").val() != "") {
					field_priority = $(this).find(".field_priority").val()
					field_name = field_name + ":"+field_priority
				}
			}
			$(this).find('.card-header a').attr("href",'#crmf-collapse-'+current_count+"-"+i).text(field_name);
			$(this).find('.collapse-div').attr({
										"id":"crmf-collapse-"+current_count+"-"+i,
										"aria-labelledby":`crmf-heading-${current_count}-${i}`,
										});
			$(this).find('.crm-fields').attr("id","crm-field-"+i);
			$(this).find(".remove-crmfield").attr("id", "remove-crmfield-"+current_count+"-"+i)
			$(this).find("#field_type").attr({
				"data-parent":"#crmf-collapse-"+current_count+"-"+i,
				"data-master":"#crmfield-div-"+current_count
			})
			$(this).find(".field_name, .field_priority").attr({
				"data-parent":`#crmf-card-${current_count}-${i}`,
				"data-master":"#crmfield-div-"+current_count
			})
			$(this).find(".unique_fields_check").attr("id","unique_field_"+current_count+"_"+i)
			$(this).find(".required_fields_check").attr("id","required_field_"+current_count+"_"+i)
			$(this).find(".editable_fields_check").attr("data-id","editable_field_"+current_count+"_"+i)
			$(this).find(".unique_fields_check_error").attr("id","unique_field_"+current_count+"_"+i+"_error")
			// $(this).find(".field_priority").tooltip('dispose');
			// $(this).find(".field_priority").attr("title", "Priority should be between 1-"+i).tooltip();  
			i++;
		})
		current_count++;


	});
	current_element.hide('slow',function(){current_element.remove();});
	
})
function submit_crm(current_element,form) {
	$.ajax({
			type: 'POST',
			headers: {"X-CSRFToken": csrf_token},
			url: form_url,
			data: form,
			beforeSend: function() {
                $('.preloader').fadeIn('fast');
            },
			success: function (data) {
				$('.preloader').fadeOut('fast');
				if(current_element.attr("data-operation")) {
					showSwal('success-message', 'CRM fields updated successfully', '/CRM/crm-fields/')
				}
				else {
					showSwal('success-message', 'CRM fields created successfully', '/CRM/crm-fields/')
				}
			},
			error: function (data) {
				$('.preloader').fadeOut('fast');
				if ("name" in data["responseJSON"]) {
					$("#field-msg").addClass("has-error").html(
						'<span class="help-block form-error m-0">'+data["responseJSON"]["name"]+'</span>').removeClass("d-none")
					setTimeout(function(){ $("#field-msg").addClass("d-none") }, 3000);
				}
			}
		});
}

$(".create-crm-field, .edit-crm-field").click(function() {
	var current_element = $(this)
	if($(this).attr("data-operation")) {
		form_url = '/CRM/CrmField/'+current_element.attr("data-operation")+'/'
	}
	else {
		form_url = '/CRM/CrmField/create/' 
	}
	// validate_priority()
	$('#crm-field-form').isValid()
	var crm_field_list = []
	crm_field_valid = false
	valid_field_priority = true
	valid_priority = true
	unique_list = []
	$('#crmf-accordion').children('div').each(function (i,current_child) {
		section_dict = {}
		db_section_name = ''
		db_field = ''
		if($(this).find(".section_name").val() != "" && !$(this).find(".priority-msg").hasClass("form-error")) {
			var current_section = $(this)
			section_dict["section_name"] = $(this).find(".section_name").val().trim()
			db_section_name = $(this).find(".section_name").val().trim().replace(/  +/g,' ').replace(/ /g,"_").toLowerCase()
			section_dict["db_section_name"] = db_section_name
			section_dict["section_priority"] = parseInt($(this).find(".section-priority").val())
			section_dict["section_fields"] = []
			$(this).find(".crmfield-div").children('div').each(function(i, child){
				crm_field_dict = {}
				if($(this).find("#field_name").val() !="" && !$(this).find(".field-priority-msg").hasClass("form-error") && $(this).find("#field_priority").val() != ""){
					crm_field_dict["field"] = $(this).find("#field_name").val().trim();
					db_field = $(this).find("#field_name").val().trim().replace(/  +/g,' ').replace(/ /g,"_").toLowerCase()
					crm_field_dict["db_field"] = db_field
					crm_field_dict["field_type"] = $(this).find("#field_type").val();
					crm_field_dict["size"] = $(this).find("#field_size").val();
					crm_field_dict["options"] = $(this).find("#field_options").val();
					crm_field_dict["editable"] = $(this).find("#field_editable").prop("checked");
					crm_field_dict["unique"] = $(this).find(".unique_fields_check").prop("checked");
					crm_field_dict["priority"] = parseInt($(this).find("#field_priority").val());
					crm_field_dict["column_span"] = $(this).find("#column-span").val()
					crm_field_dict["field_status"] = $(this).find("#field_status").val();
					crm_field_dict["crm_color"] = $(this).find(".crm-color-picker").val();
					crm_field_dict["required"] = $(this).find(".required_fields_check").prop("checked");
					if($(this).find(".unique_fields_check").prop("checked")){
						unique_list.push(db_section_name + ':' + db_field)
					}
					crm_field_valid = true
					section_dict["section_fields"].push(crm_field_dict)
				}
				else {
					current_section.find('div[data-parent="#crmf-accordion"]').addClass("show")
					$(this).find(".collapse-div").addClass("show")
					$('#crm-field-form').isValid()
					valid_field_priority = false
				}
			})
			crm_field_list.push(section_dict)
		}
		else {
			$(this).find('div[data-parent="#crmf-accordion"]').addClass("show")
			$('#crm-field-form').isValid()
			valid_priority=false
			return false
		}
	})
	var crm_fields = JSON.stringify(crm_field_list)
	$("#hidden_crm_fileds").val(crm_fields)
	var unique_fields =  JSON.stringify(unique_list)
	$("#hidden_unique_fields").val(unique_fields)
	var form = $('#crm-field-form').serialize()
	if(crm_field_list.length > 0 && crm_field_valid == true && valid_priority == true && valid_field_priority == true  && $('#crm-field-form').isValid() == true && unique_list.length >0) {
		confirmCrmFieldBeforeChk('Are you sure you want to save this crm fields. You can not change field name and data type once contacts data get uploaded', current_element,form)
		
	}
	else if (crm_field_list.length == 0){
		$("#field-msg").addClass("has-error").html(
				'<span class="help-block form-error m-0">Add atleast one section and Its fields</span>').removeClass("d-none")
					setTimeout(function(){ $("#field-msg").addClass("d-none") }, 3000);
	}
	else if(unique_list.length==0){
		$("#field-msg").addClass("has-error").html(
				'<span class="help-block form-error m-0">Add atleast one unique field</span>').removeClass("d-none")
					setTimeout(function(){ $("#field-msg").addClass("d-none") }, 3000);

	}
	else if(valid_priority == false) {
		$('div[data-parent="#crmf-accordion"]').addClass("show")
	}
	else if(valid_field_priority == false) {
		$("#crmf-accordion").find(".collapse-div").addClass("show")
	}
	
})

$(document).on("change",".unique_fields_check", function() {
	var unique_field = $("#hidden_u_fields").val()
	var old_value = $("#old_u_fields").val()
	var sec_id = $(this).attr("id").split("_")[2]
	var field_id = $(this).attr("id").split("_")[3]
	$(".editable_fields_check").prop("disabled",false)
	$(".field_size").prop("disabled",false)
	var field_value = $(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_name").val()
	var field_editable = $(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_editable").val()
	if(unique_field !="" && unique_field !="[]"){
		if (this.checked && unique_field_exist) {
			if (old_value == field_value) {
				$(".unique_fields_check:checked").prop("checked",false)
				$(this).prop("checked",true)
				$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_editable").prop("checked",false)
				$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_editable").prop("disabled",true)
				$(`#crmf-collapse-${sec_id}-${field_id}`).find(".required_fields_check").prop("checked",false)
				$(`#crmf-collapse-${sec_id}-${field_id}`).find("#required_field_div").addClass('d-none')
				$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_size").prop("disabled",true)
				$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_size").val(30)
				$("#hidden_u_fields").val(field_value)
			}
			else if(unique_field_exist==true){
				uniqueIdChange("Previous data is uploaded with other unique_field so your changes will only reflected to newly uploaded data",$(this).attr("id"), field_value)
			}
			else{
				$(this).prop("checked",true)
				$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_editable").prop("checked",false)
				$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_editable").prop("disabled",true)
				$(`#crmf-collapse-${sec_id}-${field_id}`).find(".required_fields_check").prop("checked",false)
				$(`#crmf-collapse-${sec_id}-${field_id}`).find("#required_field_div").addClass('d-none')
				$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_size").prop("disabled",true)
				$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_size").val(30)
				$("#hidden_u_fields").val(field_value)
			}
			// $(".unique_fields_check:checked").prop("checked",false)
			// var error_id = $(this).parents().find('#'+$(this).attr("id")+'_error')
			// error_id.removeClass('d-none')
			// setTimeout(function(){
			// 	error_id.addClass('d-none')
			// }, 3000);
			// $(this).prop("checked",true)
		}
		else if (this.checked && unique_field_exist==false) {
			$(".unique_fields_check:checked").prop("checked",false)
			$(this).prop("checked",true)
			$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_editable").prop("checked",false)
			$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_editable").prop("disabled",true)
			$(`#crmf-collapse-${sec_id}-${field_id}`).find(".required_fields_check").prop("checked",false)
			$(`#crmf-collapse-${sec_id}-${field_id}`).find("#required_field_div").addClass('d-none')
			$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_size").prop("disabled",true)
			$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_size").val(30)
			$("#hidden_u_fields").val(field_value)
		}
	}
	else {
		if(this.checked) {
			if(field_value) {
				$("#hidden_u_fields").val(field_value)
				$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_editable").prop("checked",false)
				$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_editable").prop("disabled",true)
				$(`#crmf-collapse-${sec_id}-${field_id}`).find(".required_fields_check").prop("checked",false)
				$(`#crmf-collapse-${sec_id}-${field_id}`).find("#required_field_div").addClass('d-none')
				$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_size").prop("disabled",true)
				$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_size").val(30)
			}
			else {
				$(this).prop("checked",false)
			}
		}
	}
	if(!this.checked) {
		
		if (field_value == unique_field){
			$(this).prop("checked",true)
			$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_editable").prop("checked",false)
			$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_editable").prop("disabled",true)
			$(`#crmf-collapse-${sec_id}-${field_id}`).find(".required_fields_check").prop("checked",false)
			$(`#crmf-collapse-${sec_id}-${field_id}`).find("#required_field_div").addClass('d-none')
			$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_size").prop("disabled",true)
			$(`#crmf-collapse-${sec_id}-${field_id}`).find("#field_size").val(30)
			$("#hidden_u_fields").val(field_value)
		}
		else if(field_value == unique_field){
			$("#hidden_u_fields").val("")
		} 
	}
})

$(document).on("change",".required_enable", function() {
	$("#field_editable").prop("disabled",false)
	var sec_id = $(this).attr("data-id").split("_")[2]
	var field_id = $(this).attr("data-id").split("_")[3]
	if(this.checked){
		$(`#crmf-collapse-${sec_id}-${field_id}`).find("#required_field_div").removeClass('d-none')
	}else{
		$(`#crmf-collapse-${sec_id}-${field_id}`).find("#required_field_div").addClass('d-none')
		$(`#crmf-collapse-${sec_id}-${field_id}`).find('.required_fields_check').prop('checked',false)
	}
})