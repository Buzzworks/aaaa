(function($) {
  showSwal = function(type, btn_text, redirect_url="", delete_type="") {
    
    if (type === 'basic') {
      swal({
        text: 'Any fool can use a computer',
        closeOnClickOutside:false,
        button: {
          text: "OK",
          value: true,
          visible: true,
          className: "btn btn-primary"
        }
      })

    } else if (type === 'title-and-text') {
      swal({
        title: 'Read the alert!',
        text: 'Click OK to close this alert',
        closeOnClickOutside:false,
        button: {
          text: "OK",
          value: true,
          visible: true,
          className: "btn btn-primary"
        }
      })

    } else if (type === 'success-message') {
      swal({
        title: 'Success!',
        text: btn_text,
        icon: 'success',
        button: {
          text: "OK",
          value: true,
          visible: true,
          className: "btn btn-primary reload",
        },
        closeOnClickOutside:false,
        closeOnConfirm: false
      }).then(
        function() {
          if (redirect_url) {
            $(".swal-button-container button").removeClass("reload")
            window.location.href = redirect_url
          }
        },
        )

    } else if (type === 'auto-close') {
      swal({
        title: 'Auto close alert!',
        text: 'I will close in 2 seconds.',
        timer: 2000,
        button: false,
        closeOnClickOutside:false
      }).then(
        function() {},
        // handling the promise rejection
        function(dismiss) {
          if (dismiss === 'timer') {
            console.log('I was closed by the timer')
          }
        }
      )
    } else if (type === 'warning-message-and-cancel') {
      swal({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3f51b5',
        cancelButtonColor: '#ff4081',
        confirmButtonText: 'Great ',
        closeOnClickOutside:false,
        buttons: {
          cancel: {
            text: "No, Cancel Please",
            value: null,
            visible: true,
            className: "btn btn-danger",
            closeModal: true,
          },
          confirm: {
            text: btn_text,
            value: true,
            visible: true,
            className: "btn btn-primary redirect",
            closeModal: true
          }
        }
      }).then(
        function(confirm) {
          if (confirm) {
            if (redirect_url && $(".swal-button-container button.redirect").text() == "OK") {
              window.location.href = redirect_url
            }
            if(delete_selected) {
              call_me("yami")
            }
            
          }
        },
        )

    } else if (type === 'custom-html') {
      swal({
        content: {
          element: "input",
          attributes: {
            placeholder: "Type your password",
            type: "password",
            class: 'form-control'
          },
        },
        button: {
          text: "OK",
          value: true,
          visible: true,
          className: "btn btn-primary",
          closeModal: true
        }
      })
    }
    else if (type === 'Confire-before-delete') {
      swal({
        content: {
          element: "input",
          attributes: {
            placeholder: "Type your password",
            type: "password",
            class: 'form-control'
          },
        },
        button: {
          text: "OK",
          value: true,
          visible: true,
          className: "btn btn-primary",
          closeModal: true
        }
      }).then(
        function(confirm) {
          if (confirm) {
            // if (redirect_url && $(".swal-button-container button.redirect").text() == "OK") {
            //   window.location.href = redirect_url
            // }
            if(delete_selected) {
              perform_delete(delete_type)
            }
            
          }
        },
        )

    }
  }
  confirmDelete = function(type, btn_text, delete_type="") {
    if (result.length > 0 || type == 'delete_one') {
       swal({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3f51b5',
        cancelButtonColor: '#ff4081',
        confirmButtonText: 'Great ',
        closeOnClickOutside:false,
        buttons: {
          cancel: {
            text: "No, Cancel Please",
            value: null,
            visible: true,
            className: "btn btn-danger",
            closeModal: true,
          },
          confirm: {
            text: btn_text,
            value: true,
            visible: true,
            className: "btn btn-primary redirect",
            closeModal: true
          }
        }
      }).then(
        function(confirm) {
          if (confirm) {
            if(delete_type) {
              $('.preloader').fadeIn('fast');
              perform_delete(delete_type)
            }
            
          }
        },
        )
    }
  }
  confirmAction = function(type, btn_text, action="", id="") {
       swal({
        title: 'Are you sure?',
        text: "You won't be able to revert "+action,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3f51b5',
        cancelButtonColor: '#ff4081',
        confirmButtonText: 'Great ',
        closeOnClickOutside:false,
        buttons: {
          cancel: {
            text: "No, Cancel Please",
            value: null,
            visible: true,
            className: "btn btn-danger",
            closeModal: true,
          },
          confirm: {
            text: btn_text,
            value: true,
            visible: true,
            className: "btn btn-primary redirect",
            closeModal: true
          }
        }
      }).then(
        function(confirm) {
          if (confirm) {
            if(action) {
              perform_download_action(action, id)
            }
            
          }
        },
        )
  }
  PermissionDeny = function(redirect_url="") {
      swal({
        title: 'You Are Not Allowed To View This Page!',
        text: 'Please Contact Administrator',
        closeOnClickOutside:false,
        button: {
          text: "OK",
          value: true,
          visible: true,
          className: "btn btn-primary"
        }
      }).then(
      function(){
        if (redirect_url){
          window.location.href = redirect_url
        }
        else{
          window.location.href = '/dashboard/'
        }
      })
    }
  confirmLogout = function(){
    swal({
        title: 'Are you sure?',
        text: "Are you sure you want to log out?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3f51b5',
        cancelButtonColor: '#ff4081',
        confirmButtonText: 'Great ',
        closeOnClickOutside:false,
        buttons: {
          cancel: {
            text: "No, Cancel Please",
            value: null,
            visible: true,
            className: "btn btn-danger",
            closeModal: true,
          },
          confirm: {
            text: "Log Me out",
            value: true,
            visible: true,
            className: "btn btn-primary redirect",
            closeModal: true
          }
        }
      }).then(
        function(confirm) {
          if (confirm) {
            if ($(".swal-button-container button.redirect").text() == "Log Me out") {
              app_logout = true
              var agent_activity_data = create_agent_activity_data()
              agent_activity_data["campaign_name"] = campaign_name
              agent_activity_data["break_type"] = ''
              agent_activity_data["break_time"] = '0:0:0'
              agent_activity_data["event"] = "LOGOUT"
              $.ajax({
                type:'post',
                headers: {"X-CSRFToken":csrf_token},
                url: '/CRM/save-agent-breaks/',
                data: agent_activity_data,
                success: function(data){
                  flush_agent_timer()
                  $('#app_timer, #idle_timer').countimer('start')
                  window.location.href = "/logout/"
                }
              })
            }
            else{
              app_logout = false
            }
          }
        },
        )
  }
  confirmBeforeChk = function(title, checkboxid){
    swal({
        title: 'Are you sure?',
        text: title,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3f51b5',
        cancelButtonColor: '#ff4081',
        confirmButtonText: 'Great ',
        closeOnClickOutside:false,
        buttons: {
          cancel: {
            text: "No, Cancel Please",
            value: null,
            visible: true,
            className: "btn btn-danger cancel",
            closeModal: true,
          },
          confirm: {
            text: "Ok",
            value: true,
            visible: true,
            className: "btn btn-primary",
            closeModal: true
          }
        }
      }).then(
        function(confirm) {
          if(confirm == null) {
            if ($(".swal-button-container button.cancel").text() == "No, Cancel Please") {
              $(checkboxid).prop("checked", false)
            }
          }
        },
        )
  }
   confirmCrmFieldBeforeChk = function(title, current_element, form){
    swal({
        title: 'Are you sure?',
        text: title,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3f51b5',
        cancelButtonColor: '#ff4081',
        confirmButtonText: 'Great ',
        closeOnClickOutside:false,
        buttons: {
          cancel: {
            text: "No, Cancel Please",
            value: null,
            visible: true,
            className: "btn btn-danger cancel",
            closeModal: true,
          },
          confirm: {
            text: "Ok",
            value: true,
            visible: true,
            className: "btn btn-primary",
            closeModal: true
          }
        }
      }).then(
        function(confirm) {
           if(confirm == true) {
              submit_crm(current_element, form)
          }
        },
        )
  }
   uniqueIdChange = function(title, checkboxid, field_value, inverse_check=false){
    swal({
        title: 'Are you sure?',
        text: title,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3f51b5',
        cancelButtonColor: '#ff4081',
        confirmButtonText: 'Great ',
        closeOnClickOutside:false,
        buttons: {
          cancel: {
            text: "No, Cancel Please",
            value: null,
            visible: true,
            className: "btn btn-danger cancel",
            closeModal: true,
          },
          confirm: {
            text: "Ok",
            value: true,
            visible: true,
            className: "btn btn-primary",
            closeModal: true
          }
        }
      }).then(
        function(confirm) {
          if(confirm == null) {
            if ($(".swal-button-container button.cancel").text() == "No, Cancel Please") {
              if(inverse_check ==false){
                $(checkboxid).prop("checked", false)
              }
              else{
              }
            }
          }
          if(confirm == true) {
            if(inverse_check==false){
              $(".unique_fields_check:checked").prop("checked",false)
              $("#"+checkboxid).prop("checked",true)
              $("#hidden_u_fields").val(field_value)
            }
          }
        },
        )
  }
  dispositionAlert = function(title){
     swal({
        title: 'Add Disposition!',
        text: 'Add '+title+' to selected disposition to save leads or delete the lead',
        closeOnClickOutside:false,
        button: {
          text: "OK",
          value: true,
          visible: true,
          className: "btn btn-primary"
        }
      })
  }
  errorAlert = function(text_msg){
    swal({
      title:  'OOPS!!! Something Went Wrong',
      text: text_msg,
      icon: 'error',
      closeOnClickOutside:false,
       button: {
        text: "OK",
        value: true,
        visible: true,
        className: "btn btn-primary"
      },
    });
  }
  dispoAlert = function(text_msg){
    swal({
      title:  'Disposition Is Required',
      text: text_msg,
      icon: 'error',
      closeOnClickOutside:false,
       button: {
        text: "OK",
        value: true,
        visible: true,
        className: "btn btn-primary"
      },
    });
  }
  autoDailAlert = function(text) {
    swal({
        title: 'Auto Dial!',
        text: text,
        timer: 2000,
        button: false,
        closeOnClickOutside:false
      }).then(
        function() {},
        // handling the promise rejection
        function(dismiss) {
          if (dismiss === 'timer') {
            console.log('I was closed by the timer')
          }
        }
      )

  }
  filenotfoundAlert = function(){
    swal({
      title:  'File Not Found (404 Error)',
      text: 'Requested file might be removed or corrupted',
      icon: 'error',
      closeOnClickOutside:false,
       button: {
        text: "OK",
        value: true,
        visible: true,
        className: "btn btn-primary"
      },
    });
  }
  sessionTerminatedAlert = function(){
    swal({
      title: 'Session Terminated',
      text: 'Your Login session is terminated by Administrator or Poor Connectivity',
      icon: 'error',
      timer: 3000,
      button: false,
      closeOnClickOutside: false,
    })
    .then(
      function(){
        app_logout = false
        window.location.href = "/"
      }
    )
  }

  confirmEmergencyLogout = function(extension, username, user_role, destination_role_name, redirect_url=''){
    swal({
        title: 'Are you sure?',
        text: "Are you sure you want to emergency log out for user extension "+extension+"?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3f51b5',
        cancelButtonColor: '#ff4081',
        confirmButtonText: 'Great ',
        closeOnClickOutside:false,
        buttons: {
          cancel: {
            text: "No, Cancel Please",
            value: null,
            visible: true,
            className: "btn btn-danger",
            closeModal: true,
          },
          confirm: {
            text: "Yes, sure",
            value: true,
            visible: true,
            className: "btn btn-primary redirect",
            closeModal: true
          }
        }
      }).then(
        function(confirm) {
          if (confirm) {
            $.ajax({
                type:'post',
                headers: {"X-CSRFToken":csrf_token},
                url: '/api/emergency_logout/',
                data: {'extension': extension, 'role_name':destination_role_name},
                success: function(data){
                  if ('success' in data){
                    if(extension) {
                      showSwal('success-message', 'Force logout for '+extension+' is successfull')
                    }
                    else {
                     showSwal('success-message', 'Force logout for '+username+' is successfull') 
                    }
                  }
                  else if ('error' in data) {
                    swal({
                      text: data['error'],
                      icon: 'error',
                      closeOnClickOutside: false,
                      button: {
                        text: "OK",
                        value: true,
                        visible: true,
                        className: "btn btn-primary"
                      }
                    })
                  }
                  else if(destination_role_name == "agent") {
                    socket.emit("emergency_logout", {"extension":extension, "username":username, "user_role":user_role})
                  }
                }
              })
          }
        },
        )
  }

  confirmEmergencyLogoutAll = function(){
    swal({
        title: 'Are you sure?',
        text: "Are you sure you want to emergency log out for all user?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3f51b5',
        cancelButtonColor: '#ff4081',
        confirmButtonText: 'Great ',
        closeOnClickOutside:false,
        buttons: {
          cancel: {
            text: "No, Cancel Please",
            value: null,
            visible: true,
            className: "btn btn-danger",
            closeModal: true,
          },
          confirm: {
            text: "Yes, sure",
            value: true,
            visible: true,
            className: "btn btn-primary redirect",
            closeModal: true
          }
        }
      }).then(
        function(confirm) {
          if (confirm) {
            $.ajax({
                type:'post',
                headers: {"X-CSRFToken":csrf_token},
                url: '/api/emergency_logout_all_user/',
                data: {},
                success: function(data){
                  if("user_list" in data) {
                    superuser_socket.emit("emergency_logout_all_users", {"user_list":data["user_list"],"username":user_name, "user_role":user_role})
                  }
                  showSwal('success-message', 'Force logout for all user is successful')
                }
              })
          }
        },
        )
  }

  cssDeleteNotAllowed = function(){
      swal({
        title: 'This CrmField can not be deleted!',
        text: 'This crm field is attched with css. You have to delete css first to delete crmfield',
        closeOnClickOutside:false,
        button: {
          text: "OK",
          value: true,
          visible: true,
          className: "btn btn-primary"
        }
      })
  }
  
})(jQuery);