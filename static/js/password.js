// this js related to password functionality

// submit change password form
$('#submit_cpassword_form').click(function(){
	var form = $("#change_password_form")
	if(form.isValid()) {
    var confirm_password = Base64.encode($("#confirm_password").val());
    var new_password = Base64.encode($("#new_password").val());
    var old_password = Base64.encode($("#old_password").val());
    $("#confirm_password").val(confirm_password)
    $("#new_password").val(new_password)
    $("#old_password").val(old_password)
    var form = $("#change_password_form")
		$.ajax({
			type: 'post',
			headers: {"X-CSRFToken": csrf_token},
			url: '/change_password/',
			data: form.serialize(),
			success: function (data) {
				console.log(data)
				showSwal('success-message', 'Password Change Successfully', '/dashboard/')
			},
			error: function (data) {
        var confirm_password = Base64.decode($("#confirm_password").val());
        var new_password = Base64.decode($("#new_password").val());
        var old_password = Base64.decode($("#old_password").val());
        $("#confirm_password").val(confirm_password)
        $("#new_password").val(new_password)
        $("#old_password").val(old_password)
				if (data["responseJSON"]["error"]) {
					$("#old-password-msg").append('<span class="help-block form-error">'+data["responseJSON"]["error"]+'<span>')
					.removeClass("d-none").addClass('has-error').parent().find('input').addClass('error')
				}
			}
		});	
	}
})

function set_password_data_dict(){
  data = {}
  data['email_id'] = $('#email_address').val()
  data['email_password'] = $('#email_password').val()
  data['email_host'] = $('#email_host').val()
  data['port_number'] = $('#port_number').val()
  data['password_reminder'] = $("#password_reminder_days").val()
  data['message'] = tinyMCE.get('scriptEditor').getContent()
  if (tinyMCE.get('scriptEditor').getContent({format : 'text'}).length > 150){
        $("#script-err-msg").removeClass("d-none").text("Msg length should be less than 150 characters")
        setTimeout(function(){ $("#script-err-msg").addClass("d-none") }, 3000);
        return false
    }
  $('#password_data').val(JSON.stringify(data))

}
$('#password_management_btn').click(function(){
  set_password_data_dict()
   var form = $("#password_management_form")
    $.ajax({
      type: 'post',
      headers: {"X-CSRFToken": csrf_token},
      url: '/UserManagement/PasswordManagement/',
      data: form.serialize(),
      success: function (data) {
        console.log(data)
        showSwal('success-message', 'Changes Added Successfully', '/dashboard/')
      }
    })
})



/**
 * @author
 * @link https://github.com/elboletaire/password-strength-meter
 * @license GPL-3.0
 */
// eslint-disable-next-line
;(function($) {
  'use strict';

  var Password = function ($object, options) {
    var defaults = {
      shortPass: 'The password is too short',
      badPass: 'Weak: try combining letters & numbers',
      goodPass: 'Medium: try using special characters',
      strongPass: '',
      containsField: 'The password contains your username',
      enterPass: '',
      showPercent: false,
      showText: true,
      animate: true,
      animateSpeed: 'fast',
      field: false,
      fieldPartialMatch: true,
      minimumLength: 8,
      closestSelector: 'div',
    };

    options = $.extend({}, defaults, options);

    /**
     * Returns strings based on the score given.
     *
     * @param int score Score base.
     * @return string
     */
    function scoreText(score) {
      if (score === -1) {
        return options.shortPass;
      }
      if (score === -2) {
        return options.containsField;
      }

      score = score < 0 ? 0 : score;

      if (score < 34) {
        return options.badPass;
      }
      if (score < 68) {
        return options.goodPass;
      }

      return options.strongPass;
    }

    /**
     * Returns a value between -2 and 100 to score
     * the user's password.
     *
     * @param  string password The password to be checked.
     * @param  string field The field set (if options.field).
     * @return int
     */
    function calculateScore(password, field) {
      var score = 0;

      // password < options.minimumLength
      if (password.length < options.minimumLength) {
        return -1;
      }

      if (options.field) {
        // password === field
        if (password.toLowerCase() === field.toLowerCase()) {
          return -2;
        }
        // password contains field (and fieldPartialMatch is set to true)
        if (options.fieldPartialMatch && field.length) {
          var user = new RegExp(field.toLowerCase());
          if (password.toLowerCase().match(user)) {
            return -2;
          }
        }
      }

      // password length
      score += password.length * 4;
      score += checkRepetition(1, password).length - password.length;
      score += checkRepetition(2, password).length - password.length;
      score += checkRepetition(3, password).length - password.length;
      score += checkRepetition(4, password).length - password.length;

      // password has 3 numbers
      if (password.match(/(.*[0-9].*[0-9].*[0-9])/)) {
        score += 5;
      }

      // password has at least 2 sybols
      var symbols = '.*[!,@,#,$,%,^,&,*,?,_,~]';
      symbols = new RegExp('(' + symbols + symbols + ')');
      if (password.match(symbols)) {
        score += 5;
      }

      // password has Upper and Lower chars
      if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) {
        score += 10;
      }

      // password has number and chars
      if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/)) {
        score += 15;
      }

      // password has number and symbol
      if (password.match(/([!,@,#,$,%,^,&,*,?,_,~])/) && password.match(/([0-9])/)) {
        score += 15;
      }

      // password has char and symbol
      if (password.match(/([!,@,#,$,%,^,&,*,?,_,~])/) && password.match(/([a-zA-Z])/)) {
        score += 15;
      }

      // password is just numbers or chars
      if (password.match(/^\w+$/) || password.match(/^\d+$/)) {
        score -= 10;
      }

      if (score > 100) {
        score = 100;
      }

      if (score < 0) {
        score = 0;
      }

      return score;
    }

    /**
     * Checks for repetition of characters in
     * a string
     *
     * @param int rLen Repetition length.
     * @param string str The string to be checked.
     * @return string
     */
    function checkRepetition(rLen, str) {
      var res = "", repeated = false;
      for (var i = 0; i < str.length; i++) {
        repeated = true;
        for (var j = 0; j < rLen && (j + i + rLen) < str.length; j++) {
          repeated = repeated && (str.charAt(j + i) === str.charAt(j + i + rLen));
        }
        if (j < rLen) {
          repeated = false;
        }
        if (repeated) {
          i += rLen - 1;
          repeated = false;
        }
        else {
          res += str.charAt(i);
        }
      }
      return res;
    }

    /**
     * Initializes the plugin creating and binding the
     * required layers and events.
     *
     * @return void
     */
    function init() {
      var shown = true;
      var $text = options.showText;
      var $percentage = options.showPercent;
      var $graybar = $('<div>').addClass('pass-graybar');
      var $colorbar = $('<div>').addClass('pass-colorbar');
      var $insert = $('<div>').addClass('pass-wrapper').append(
        $graybar.append($colorbar)
      );

      $object.closest(options.closestSelector).addClass('pass-strength-visible');
      if (options.animate) {
        $insert.css('display', 'none');
        shown = false;
        $object.closest(options.closestSelector).removeClass('pass-strength-visible');
      }

      if (options.showPercent) {
        $percentage = $('<span>').addClass('pass-percent').text('0%');
        $insert.append($percentage);
      }

      if (options.showText) {
        $text = $('<span>').addClass('pass-text').html(options.enterPass);
        $insert.append($text);
      }

      $object.closest(options.closestSelector).append($insert);

      $object.keyup(function() {
        var field = options.field || '';
        if (field) {
          field = $(field).val();
        }

        var score = calculateScore($object.val(), field);
        $object.trigger('password.score', [score]);
        var perc = score < 0 ? 0 : score;
        $colorbar.css({
          backgroundPosition: "0px -" + perc + "px",
          width: perc + '%'
        });

        if (options.showPercent) {
          $percentage.html(perc + '%');
        }

        if (options.showText) {
          var text = scoreText(score);
          if (!$object.val().length && score <= 0) {
            text = options.enterPass;
          }

          if ($text.html() !== $('<div>').html(text).html()) {
            $text.html(text);
            $object.trigger('password.text', [text, score]);
          }
        }
      });

      if (options.animate) {
        $object.focus(function() {
          if (!shown) {
            $insert.slideDown(options.animateSpeed, function () {
              shown = true;
              $object.closest(options.closestSelector).addClass('pass-strength-visible');
            });
          }
        });

        $object.blur(function() {
          if (!$object.val().length && shown) {
            $insert.slideUp(options.animateSpeed, function () {
              shown = false;
              $object.closest(options.closestSelector).removeClass('pass-strength-visible')
            });
          }
        });
      }

      return this;
    }

    return init.call(this);
  }

  // Bind to jquery
  $.fn.password = function(options) {
    return this.each(function() {
      new Password($(this), options);
    });
  };
})(jQuery);




/*
 * jQuery Minimun Password Requirements 1.1
 * http://elationbase.com
 * Copyright 2014, elationbase
 * Check Minimun Password Requirements
 * Free to use under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
*/
var strong = false; 
  
(function($){
    $.fn.extend({
        passwordRequirements: function(options) {
       
          var lower = false
          var number = false
          var special = false
          var upper = false
            // options for the plugin
            var defaults = {
        numCharacters: 8,
        useLowercase: true,
        useUppercase: true,
        useNumbers: true,
        useSpecial: true,
        infoMessage: '',
        style: "light", // Style Options light or dark
        fadeTime:300 // FadeIn / FadeOut in milliseconds
            };

            options =  $.extend(defaults, options);

            return this.each(function() {
        
        var o = options;
        
                o.infoMessage = 'The minimum password length is ' + o.numCharacters + ' characters and must contain at least 1 lowercase letter, 1 capital letter, 1 number, and 1 special character.';
        // Add Variables for the li elements
        var numCharactersUI = '<li class="pr-numCharacters"><span></span># of characters</li>',
          useLowercaseUI = '',
          useUppercaseUI = '',
          useNumbersUI   = '',
          useSpecialUI   = '';
        // Check if the options are checked
        if (o.useLowercase === true) {
          useLowercaseUI = '<li class="pr-useLowercase"><span></span>Lowercase letter</li>';
  
        }
        if (o.useUppercase === true) {
          useUppercaseUI = '<li class="pr-useUppercase"><span></span>Capital letter</li>';
    
        }
        if (o.useNumbers === true) {
          useNumbersUI = '<li class="pr-useNumbers"><span></span>Number</li>';

        }
        if (o.useSpecial === true) {
          useSpecialUI = '<li class="pr-useSpecial"><span></span>Special character</li>';

        }
        // Append password hint div
        var messageDiv = '<div id="pr-box"><i></i><div id="pr-box-inner"><p>' + o.infoMessage + '</p><ul>' + numCharactersUI + useLowercaseUI + useUppercaseUI + useNumbersUI + useSpecialUI + '</ul></div></div>';
        
        // Set campletion vatiables
        var numCharactersDone = true,
          useLowercaseDone = true,
          useUppercaseDone = true,
          useNumbersDone   = true,
          useSpecialDone   = true;
                
        // Show Message reusable function 
        var showMessage = function () {
          if (numCharactersDone === false || useLowercaseDone === false || useUppercaseDone === false || useNumbersDone === false || useSpecialDone === false) {
            $(".pr-password").each(function() {
              // Find the position of element
              var posH = $(this).offset().top,
                itemH = $(this).innerHeight(),
                totalH = posH+itemH,
                itemL = $(this).offset().left;
              // Append info box tho the body
              $("body")     .append(messageDiv);
              $("#pr-box")  .addClass(o.style)
                      .fadeIn(o.fadeTime)
                      .css({top:totalH, left:itemL});
            });
          }
        };
        
        // Show password hint 
        $(this).on("focus",function (){
          showMessage();
        });
        
        // Delete Message reusable function 
        var deleteMessage = function () {
          var targetMessage = $("#pr-box");
          targetMessage.fadeOut(o.fadeTime, function(){
            $(this).remove();
          });
        };
        
        // Show / Delete Message when completed requirements function 
        var checkCompleted = function () {
          if (numCharactersDone === true && useLowercaseDone === true && useUppercaseDone === true && useNumbersDone === true && useSpecialDone === true) {
            deleteMessage();
            strong = true
          } else {
            strong = false
            showMessage();
          }
        };
        
        // Show password hint 
        $(this).on("blur",function (){
          deleteMessage();
        });
        
        
        // Show or Hide password hint based on user's event
        // Set variables
        var lowerCase       = new RegExp('[a-z]'),
          upperCase       = new RegExp('[A-Z]'),
          numbers         = new RegExp('[0-9]'),
          specialCharacter     = new RegExp('[!,%,&,@,#,$,^,*,?,_,~]');
        
        // Show or Hide password hint based on keyup
        $(this).on("keyup focus", function (){
          var thisVal = $(this).val();  
          
          checkCompleted();
          
          // Check # of characters
          if ( thisVal.length >= o.numCharacters ) {
            // console.log("good numCharacters");
            $(".pr-numCharacters span").addClass("pr-ok");
            numCharactersDone = true;
          } else {
            // console.log("bad numCharacters");
            $(".pr-numCharacters span").removeClass("pr-ok");
            numCharactersDone = false;
          }
          // lowerCase meet requirements
          if (o.useLowercase === true) {
            if ( thisVal.match(lowerCase) ) {
              // console.log("good lowerCase");
              $(".pr-useLowercase span").addClass("pr-ok");
              useLowercaseDone = true;
            } else {
              // console.log("bad lowerCase");
              $(".pr-useLowercase span").removeClass("pr-ok");
              useLowercaseDone = false;
            }
          }
          // upperCase meet requirements
          if (o.useUppercase === true) {
            if ( thisVal.match(upperCase) ) {
              // console.log("good upperCase");
              $(".pr-useUppercase span").addClass("pr-ok");
              useUppercaseDone = true;
            } else {
              // console.log("bad upperCase");
              $(".pr-useUppercase span").removeClass("pr-ok");
              useUppercaseDone = false;
            }
          }
          // upperCase meet requirements
          if (o.useNumbers === true) {
            if ( thisVal.match(numbers) ) {
              // console.log("good numbers");
              $(".pr-useNumbers span").addClass("pr-ok");
              useNumbersDone = true;
            } else {
              // console.log("bad numbers");
              $(".pr-useNumbers span").removeClass("pr-ok");
              useNumbersDone = false;
            }
          }
          // upperCase meet requirements
          if (o.useSpecial === true) {
            if ( thisVal.match(specialCharacter) ) {
              // console.log("good specialCharacter");
              $(".pr-useSpecial span").addClass("pr-ok");
              useSpecialDone = true;
            } else {
              // console.log("bad specialCharacter");
              $(".pr-useSpecial span").removeClass("pr-ok");
              useSpecialDone = false;
            }
          }
        });
            });
        }
    });
})(jQuery);

$('.pr-password').on('focusout', () => {
  if(strong == false){
    $('.pr-password').focus()
  }
})