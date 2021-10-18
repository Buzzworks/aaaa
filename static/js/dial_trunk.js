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
Vue.component('select2', {
    props: ['options', 'value'],
    template: '<select v-bind:name="name" class="form-control"></select>',
    mounted: function () {
        var vm = this
        $(this.$el)
      // init select2
      .select2({ data: this.options })
      .val(this.value)
      .trigger('change')
      // emit event on change.
      .on('change', function () {
        vm.$emit('input', $(this).val())
        vm.$emit('where-change')
      })
      },
      watch: {
        value: function (value) {
          // update value
          if ([...value].sort().join(",") !== [...$(this.$el).val()].sort().join(",")){
              $(this.$el)
              .val(value)
              .trigger('change')
          }
        },
        options: function (options) {
          // update options
          $(this.$el).select2({ data: options })
        }
    },
    destroyed: function () {
        $(this.$el).off().select2('destroy')
    }
})

trunk_flag=false
delete_trunk = false
add_trunk_vue = new Vue({
	el: '#add_trunk_div',
	delimiters: ["${","}"],
	data: { 
		
		group_trunk_list: [],
		camp_trunk_dict:[],
		trunk_list:[],
        did_type:[],
        componentKey: 0,
        did_list:[],
        camp_page:false,
        hide_single_trunk:false,
        used_did:[],
        skill_ingroup:false
	
	},
	methods: {
        changeDidRnageValue: function(start, end, type, index){
            if(start>end && start !='' && start !=null && end !='' && end !=null){
                this.group_trunk_list[index]['did_end'] = null
                $("#"+index+"-end_greater_error").removeClass("d-none")
                        setTimeout(function(){
                            $("#"+index+"-end_greater_error").addClass("d-none")
                        },3000) 
            }
            if(start>end && start !='' && start !=null && end !='' && end !=null){
                this.group_trunk_list[index]['did_start'] = null
                $("#"+index+"-start_less_error").removeClass("d-none")
                setTimeout(function(){
                    $("#"+index+"-start_less_error").addClass("d-none")
                },3000) 
            }
        },
		add_dial_trunk: function(index) {
			add_trunk_div = true
			vm =this
            if (vm.group_trunk_list[index]["trunk_id"] == ""){
                add_trunk_div = false
            }
			if(add_trunk_div && vm.group_trunk_list.length <4){
				id_val = vm.group_trunk_list.length +1
                if(vm.skill_ingroup){
                    this.group_trunk_list.push({"trunk_priority":id_val, "trunk_id":"","did_type":"","did":[],"old_trunk":""})
                }
                else {
                    this.group_trunk_list.push({"trunk_priority":id_val, "trunk_id":"","did_type":"","did":[],"did_start":"","did_end":"","old_trunk":""})
                }
			}
		},
		remove_trunk:function(index){
            this.group_trunk_list.splice(index, 1)
            var dummy_dict = []
            $.each( this.group_trunk_list, function( key, val ) {
                val["trunk_priority"] = key+1
                dummy_dict.push(val)
            });
            this.group_trunk_list = dummy_dict

		},
		saveTrunkGroup:function(){
            vm =this
            form = $("#trunk_group_form")
            if(form.isValid()) {
            jQuery.each( vm.group_trunk_list, function( key, val ) {
                if(val!=undefined){
                    if (val["trunk_id"] == ""){
                        delete vm.group_trunk_list[key]         
                    }
                }
            });
            trunk_group_id = $("#trunk_group_id").val()
            if(trunk_group_id){
                url = `/Modules/DialTrunkGroup/${trunk_group_id}/`
            }
            else{
			     url ='/Modules/DialTrunkGroup/create/' 
            }
			$("#trunk_details").val(JSON.stringify(vm.group_trunk_list))
			  $.ajax({
                        type: "post",
                        headers: {
                            "X-CSRFToken": csrf_token
                        },
                        url: url,
                        data: form.serialize(),
                        success: function(data) {
                            if(trunk_group_id) {
                        	 showSwal('success-message', 'Dial Trunk Group Successfully Updated', '/Modules/DialTrunkGroup/')
                            }
                            else {
                             showSwal('success-message', 'Dial Trunk Group Successfully Created', '/Modules/DialTrunkGroup/')   
                            }
                        },
                        error: function(data) {
                            $("#name-error").html(`<span class="help-block form-error">Trunk group with this name already exists</span>`).addClass('has-error')
                            $("#name").removeClass("valid").addClass("error")
                        }
                    })
            }
		},
        calculateChannelCount:function(trunk_id,key,index, old_trunk) {
            vm = this
            if(trunk_id!=old_trunk){
                vm.group_trunk_list[index]['did_type'] ='';
                vm.group_trunk_list[index]['old_trunk'] = trunk_id
            }
            if(vm.camp_page==false && trunk_id !=""){
                var channel_count = this.trunk_channel_count[trunk_id]
                var abc = true
                var temp_index = index;
                var target = trunk_id
                var selected_did = vm.group_trunk_list[temp_index]['did'];
                var selected_start = vm.group_trunk_list[temp_index]['did_start'];
                var selected_end = vm.group_trunk_list[temp_index]['did_end'];
                var numOccurences = $.grep(vm.group_trunk_list, function (elem) {
                    return elem['trunk_id'].toString() === target.toString();
                }).length
                if (numOccurences>1) {
                    vm.group_trunk_list[temp_index]['options'] = [];
                    $("#"+index+"-exist_current_error").removeClass("d-none")
                    // vm.group_trunk_list[index]['trunk_id'] = ""
                    // $("#"+index+"-trunk_id").val("")
                    abc = false
                    setTimeout(function(){
                                $("#"+index+"-exist_current_error").addClass("d-none")
                            },1000) 
                    vm.group_trunk_list[temp_index]['trunk_id'] =null
                    // vm.remove_trunk(index)
                }
                
                if (abc) {
                $.ajax({
                    type: "post",
                    headers: {
                        "X-CSRFToken": csrf_token
                    },
                    url: '/Modules/DialTrunkGroup/check-dial-trunk/',
                    data: {"trunk_id":trunk_id,"trunk_group_id":$("#trunk_group_id").val()},
                    success: function(data) {
                        var trunk_id=vm.group_trunk_list[index]['trunk_id']
                        var range_array = []    
                        if(data["exists"]){
                            $("#"+index+"-exist_error").removeClass("d-none")
                            vm.group_trunk_list[index]['trunk_id'] = ""
                            $(index+"-trunk_id").val("")
                            setTimeout(function(){
                                $("#"+index+"-exist_error").addClass("d-none")
                            },3000)         

                        }else{
                            $("#"+index+"-exist_error").addClass("d-none")
                             var total_channel_count = 0
                            $.each(vm.trunk_channel_count, function(index,val){
                                $.each(vm.group_trunk_list, function(index,value) {
                                    if (val["id"] == value["trunk_id"]) {
                                        total_channel_count = total_channel_count + val["channel_count"]

                                    }
                                })
                            })
                            $.each(vm.trunk_list, function(index,trunk_val){
                                if( trunk_val["id"] == trunk_id){
                                    var temp_range = trunk_val["did_range"].split(",")
                                    var start_end = temp_range[0]
                                    if (temp_range[1] == undefined) {
                                        end_node = start_end
                                    }
                                    else {
                                        end_node = temp_range[1]
                                    }
                                    let is_leading_zero = false
                                    let start_end_length = start_end.length
                                    if (start_end.match(/^0+/)) {
                                        is_leading_zero = true
                                    }
                                    for (i = start_end; i <= end_node; i++) {
                                        let did_value = (is_leading_zero) ? i.toString().padStart(start_end_length,"0") : i.toString()
                                        select_options = {
                                            "id":i,
                                            "text":did_value,
                                            "disabled":false,
                                        }
                                        range_array.push(select_options)
                                    }
                                    vm.group_trunk_list[temp_index]['did'] = selected_did;
                                    vm.group_trunk_list[temp_index]['did_start'] = selected_start;
                                    vm.group_trunk_list[temp_index]['did_end'] = selected_end;
                                    vm.group_trunk_list[temp_index]['options'] = [...range_array]
                                    vm.componentKey += 1;       
                                }
                            })
                            $("#total_channel_count").val(total_channel_count)
                        }
                    },
                    error: function(data) {

                    }
                })
                }
            }
            else{
                var range_array = []    
                $.each(vm.trunk_list, function(index,trunk_val){
                    if( trunk_val["id"] == trunk_id){
                        var temp_range = trunk_val["did_range"].split(",")
                        var start_end = temp_range[0]
                        if (temp_range[1] == undefined) {
                            end_node = start_end
                        }
                        else {
                            end_node = temp_range[1]
                        }
                        let is_leading_zero = false
                        let start_end_length = start_end.length
                        if (start_end.match(/^0+/)) {
                            is_leading_zero = true
                        }
                        for (i = start_end; i <= end_node; i++) {
                            let did_value = (is_leading_zero) ? i.toString().padStart(start_end_length,"0") : i.toString()
                            // range_array.push(did_value)
                            if(vm.used_did.indexOf(did_value.toString()) === -1){
                                select_options = {
                                    "id":i,
                                    "text":did_value,
                                    "disabled":false,
                                }
                            }else{
                                select_options = {
                                    "id":i,
                                    "text":did_value,
                                    "disabled":true,  
                                } 
                            } 
                            range_array.push(select_options)
                        }
                        vm.group_trunk_list[0]['did'] = selected_did;
                        vm.group_trunk_list[0]['options'] = range_array
                    }
                })
            }
           
        },
        checkDidType:function(index, did_type){
            this.group_trunk_list[index]["did"]=""
            if(!this.skill_ingroup){
                this.group_trunk_list[index]["did_start"]=""
                this.group_trunk_list[index]["did_end"]=""
            }
            if(did_type =="select_all") {
                select_all_did = []
                // console.log(this.group_trunk_list[index]['options'])
               $.each(this.group_trunk_list[index]['options'],function(key,val){
                    console.log(val['disabled'],val)
                    if(val['disabled'] != true){
                        select_all_did.push(val['text'])
                    }
               })
                this.group_trunk_list[index]['did'] = select_all_did
            }
        }
	}})
