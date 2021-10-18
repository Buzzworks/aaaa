ingroup_campaign_vue = new Vue({
	el: '#add_ingroup_campaign_div',
	delimiters: ["${","}"],
	data: { 
		campaign_list: [],
        ingroup_camp_list : [],
        non_user_campaigns : []
	},
	methods: {
        add_campaign: function(index) {
            add_trunk_div = true
            vm =this
            if (vm.ingroup_camp_list[index]["campaign_id"] == ""){
                add_trunk_div = false
            }
            if(add_trunk_div){
                id_val = vm.ingroup_camp_list.length +1
                this.ingroup_camp_list.push({"campaign_id":"","priority":id_val})
            }
        },
        remove_campaign:function(index){
            this.ingroup_camp_list.splice(index, 1)
            var dummy_dict = []
            $.each( this.ingroup_camp_list, function( key, val ) {
                val["priority"] = key+1
                dummy_dict.push(val)
            });
            this.ingroup_camp_list = dummy_dict

        },
        saveInGroup:function(index){
            form = $("#ingroup_form")
            if(form.isValid()) {
                in_group_id = $("#in_group_id").val()
                if(in_group_id){
                    url = `/CampaignManagement/InGroupCampaign/${in_group_id}/`
                }
                else{
                     url ='/CampaignManagement/InGroupCampaign/create/' 
                }
                trunk_list = add_trunk_vue.group_trunk_list[0]
                if(trunk_list["did_type"] == "single") {
                    var did_val = [trunk_list["did"]]
                    trunk_list["did"] = did_val
                }
                delete trunk_list["options"]
                delete trunk_list["old_trunk"]
                $("#caller_id").val(JSON.stringify(trunk_list))
                $("#campaign_data").val(JSON.stringify(this.ingroup_camp_list))
                $.ajax({
                    type: "post",
                    headers: {
                        "X-CSRFToken": csrf_token
                    },
                    url: url,
                    data: form.serialize(),
                    success: function(data) {
                        if(in_group_id) {
                         showSwal('success-message', 'InGroup Campaign Successfully Updated', '/CampaignManagement/InGroupCampaign/')
                        }
                        else {
                         showSwal('success-message', 'InGroup Campaign Successfully Created', '/CampaignManagement/InGroupCampaign/')   
                        }
                    },
                    error: function(data) {
                        $("#name-error").html(`<span class="help-block form-error">InGroup with this name already exists</span>`).addClass('has-error')
                        $("#name").removeClass("valid").addClass("error")
                    }
                })
            }
        },
        checkCampaign:function(index,campaign_id){
            vm = this
            check_ingroup_exist = true
            var numOccurences = $.grep(vm.ingroup_camp_list, function (elem) {
                    return elem['campaign_id'].toString() === campaign_id.toString();
                }).length
            if (numOccurences >1){
                $("#"+index+"-exist_current_group").removeClass("d-none")
                check_ingroup_exist = false
                setTimeout(function(){
                            $("#"+index+"-exist_current_group").addClass("d-none")
                        },3000) 
                vm.ingroup_camp_list[index]['campaign_id'] =null   
            }
            if(check_ingroup_exist && campaign_id) {
                in_group_id = $("#in_group_id").val()
                $.ajax({
                    type: "put",
                    headers: {
                        "X-CSRFToken": csrf_token
                    },
                    url: '/CampaignManagement/InGroupCampaign/create/',
                    data: {"campaign_id":campaign_id,"in_group_id":in_group_id},
                    success: function(data) {
                        // var campaign_id=vm.ingroup_camp_list[index]['campaign_id'] 
                        if(data["exists"]){
                            $("#"+index+"-exist_group").removeClass("d-none")
                            vm.ingroup_camp_list[index]['campaign_id'] = ""
                            // $(index+"-camp_id").val("")
                            setTimeout(function(){
                                $("#"+index+"-exist_group").addClass("d-none")
                            },3000)         

                        }else{
                            $("#"+index+"-exist_group").addClass("d-none")
                        }
                    }
                })
            }

        }
	}})