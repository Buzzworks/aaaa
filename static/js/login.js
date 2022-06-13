// this js related to login form. all login page jquery goes here.

jQuery.validator.addMethod("notEqual", function(value, element, param) {
    return this.optional(element) || value != $(param).val();
}, "Please specify a different (non-default) value");
$(".form-control").attr('autocomplete', 'off');
$('.form-control').bind('input', function() {
    var c = this.selectionStart,
          r = /[^a-z./@#_%$*:;()+-0123456789 ]/gi,
       v = $(this).val();
    if(r.test(v)) {
      $(this).val(v.replace(r, ''));
      c--;
    }
    this.setSelectionRange(c, c);
});
$('#changePassword_link').click(function(e) {
    e.preventDefault()
    $('#loginForm_div').hide('slow');
    $('#forgotPassword_div').hide('slow');
    $('#changePassword_div').show('slow');
})
$('#downloadCertificate_link').click(function(e) {
    e.preventDefault()
    $('#loginForm_div').hide('slow');
    $('#forgotPassword_div').hide('slow');
    $('#changePassword_div').hide('slow');
    $('#downloadCertificate').show('slow');
})

$('.forgotPassword_link').click(function(e) {
    e.preventDefault()
    $('#loginForm_div').hide('slow');
    $('#changePassword_div').hide('slow');
    $('#downloadCertificate').hide('slow');
    $('#forgotPassword_div').show('slow');
})


$('.backtoSignIn_link').click(function(e) {
    e.preventDefault()
    $('#changePassword_div').hide('slow');
    $('#resetPassword_form')[0].reset();
    $('#forgotPassword_div,#downloadCertificate').hide('slow');
    $('#loginForm_div').show('slow');
})

$("#login_btn").click(function() {
    var now = new Date();
    var dateString = moment(now).format('YYYY-MM-DD HH:mm:ss');
    var encodedPassword = Base64.encode($("#password").val());
    $("#client_time").val(dateString);
    $("#password").val(encodedPassword);
    if ($('#loginForm').valid()) {
        $('#loginForm').get(0).submit()
    }
});


$('#forgotpassword_submit').click(function(){
    $('#email-loader').fadeIn('slow')
    $('#forgotpassword_submit').addClass('d-none')
    $.ajax({
            type: 'post',
            url: '/password-reset/',
            data: $('#forgotpassword_form').serialize(),
            success: function(data) {
                $('#email-loader').fadeOut('slow')
                if(data['error']){
                    $("#forgotPassword_error").removeClass("d-none").text(data['error'])
                     setTimeout(function() {
                            $("#forgotPassword_error").addClass('d-none')
                        }, 3000);
                }
                if(data['success']){
                    $("#forgotPassword_success").removeClass("d-none").text(data['success'])
                    setTimeout(function(){
                        $('#forgotPassword_success').addClass('d-none')
                    },7000)
                }
                $('#forgotpassword_submit').removeClass('d-none')
            },
            error:function(data){
                $('#email-loader').fadeOut('slow')
                $('#forgotpassword_submit').removeClass('d-none')
            } 
        })
})
$('#resetPassword_form').validate({
    rules: {
        cp_username: "required",
        old_password: "required",
        new_password: {
            required: true,
            minlength: 8,
            notEqual: "#old_password"
        },
        confirm_password: {
            required: true,
            minlength: 8,
            equalTo: "#new_password",
        },
    },
    messages: {
        cp_username: "Please provide your username",
        old_password: "Please provide your old password",
        new_password: {
            required: "Please provide a new password",
            minlength: "Your password must be at least 8 characters long",
            notEqual: "New password should not be same as old password"
        },
        confirm_password: {
            required: "Please confirm new password",
            minlength: "Your password must be at least 8 characters long",
            equalTo: "Please enter the same password as above",
        },
    },
    errorPlacement: function(label, element) {
        label.addClass('mt-2 text-danger');
        label.insertAfter(element.parent());
    },
    highlight: function(element, errorClass) {
        $(element).parent().parent().addClass('has-danger')
        $(element).parent().addClass('form-control-danger')
    }
});

$('#changePassword_submit').unbind('click').click(function() {
    var resetPassword_form = $('#resetPassword_form')
    if (resetPassword_form.valid()) {
        var confirm_password = Base64.encode($("#confirm_password").val());
        var new_password = Base64.encode($("#new_password").val());
        var old_password = Base64.encode($("#old_password").val());
        $("#confirm_password").val(confirm_password)
        $("#new_password").val(new_password)
        $("#old_password").val(old_password)
        var resetPassword_form = $("#resetPassword_form")
        $.ajax({
            type: 'post',
            url: '/change_password/',
            data: resetPassword_form.serialize(),
            success: function(data) {
                showSwal('success-message', 'Password Change Successfully', '/')
            },
            error: function(data) {
                var confirm_password = Base64.decode($("#confirm_password").val());
                var new_password = Base64.decode($("#new_password").val());
                var old_password = Base64.decode($("#old_password").val());
                $("#confirm_password").val(confirm_password)
                $("#new_password").val(new_password)
                $("#old_password").val(old_password)
                if (data["responseJSON"]["error"]) {
                    $("#changePassword_error").text(data["responseJSON"]["error"]).removeClass("d-none")
                    setTimeout(function() {
                        $("#changePassword_error").addClass("d-none")
                    }, 3000);
                }
            }
        })
    }
})

$(document).on('keypress', function(e) {
    if (e.which == 13) {
        if ($('#loginForm_div').css('display') !== 'none') {
            $("#login_btn").click()
        } else if ($('#changePassword_div').css('display') !== 'none') {
            $('#changePassword_submit').click()
        }
    }
});

$("#downloadCertificateForm").validate({
    rules: {
        download_username: "required",
        download_password: "required",
    },
    messages: {
        download_username: "Please provide your username",
        download_password: "Please provide your password",
    },
    errorPlacement: function(label, element) {
        label.addClass('mt-2 text-danger');
        label.insertAfter(element.parent());
    },
    highlight: function(element, errorClass) {
        $(element).parent().parent().addClass('has-danger')
        $(element).parent().addClass('form-control-danger')
    }
});

$('#download_certificate').unbind('click').click(function() {
    var downloadCertificateForm = $('#downloadCertificateForm')
    if (downloadCertificateForm.valid()) {
        var download_password = Base64.encode($("#download_password").val());
        $("#download_password").val(download_password)
        var downloadCertificateForm = $("#downloadCertificateForm")
        $.ajax({
            type: 'post',
            url: '/api/download-certificate/',
            xhrFields: {
                responseType: 'blob'
            },
            data: downloadCertificateForm.serialize(),
            success: function(data) {
                var a = document.createElement('a');
                var url = window.URL.createObjectURL(data);
                a.href = url;
                a.download = 'flexydial.crt';
                document.body.append(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                showSwal('success-message', 'Certificate Successfully Downloaded', '')
            },
            error: function(data) {
                var password = Base64.decode($("#download_password").val());
                $("#download_password").val(download_password)
                if (data.status == 400) {
                    $("#downloadCertificate_error").text('File Not found!').removeClass("d-none")
                } else {
                    $("#downloadCertificate_error").text('Username or Password is incorrect').removeClass("d-none")
                }
                setTimeout(function() {
                    $("#downloadCertificate_error").addClass("d-none")
                }, 3000);
            }
        })
    }
})