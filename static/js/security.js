
!function(a,b){"function"==typeof define&&define.amd?define(["jquery"],function(a){return b(a)}):"object"==typeof module&&module.exports?module.exports=b(require("jquery")):b(a.jQuery)}(this,function(a){!function(a,b){"use strict";a.formUtils.registerLoadedModule("security"),a.formUtils.addValidator({name:"spamcheck",validatorFunction:function(a,b){var c=b.valAttr("captcha");return c===a},errorMessage:"",errorMessageKey:"badSecurityAnswer"}),a.formUtils.addValidator({name:"confirmation",validatorFunction:function(b,c,d,e,f){var g,h=c.valAttr("confirm")||c.attr("name")+"_confirmation",i=f.find('[name="'+h+'"]');if(!i.length)return a.formUtils.warn('Password confirmation validator: could not find an input with name "'+h+'"',!0),!1;if(g=i.val(),d.validateOnBlur&&!i[0].hasValidationCallback){i[0].hasValidationCallback=!0;var j=function(){c.validate()};i.on("keyup",j),f.one("formValidationSetup",function(){i[0].hasValidationCallback=!1,i.off("keyup",j)})}return b===g},errorMessage:"",errorMessageKey:"notConfirmed"});var c={amex:[15,15],diners_club:[14,14],cjb:[16,16],laser:[16,19],visa:[16,16],mastercard:[16,16],maestro:[12,19],discover:[16,16]},d=!1,e=!1;a.formUtils.addValidator({name:"creditcard",validatorFunction:function(b,f){var g=a.split(f.valAttr("allowing")||"");if(e=a.inArray("amex",g)>-1,d=e&&1===g.length,g.length>0){var h=!1;if(a.each(g,function(d,e){if(e in c){if(b.length>=c[e][0]&&b.length<=c[e][1])return h=!0,!1}else a.formUtils.warn('Use of unknown credit card "'+e+'"',!0)}),!h)return!1}if(""!==b.replace(new RegExp("[0-9]","g"),""))return!1;var i=0;return a.each(b.split("").reverse(),function(a,b){b=parseInt(b,10),a%2===0?i+=b:(b*=2,i+=b<10?b:b-9)}),i%10===0},errorMessage:"",errorMessageKey:"badCreditCard"}),a.formUtils.addValidator({name:"cvv",validatorFunction:function(a){return""===a.replace(/[0-9]/g,"")&&(a+="",d?4===a.length:e?3===a.length||4===a.length:3===a.length)},errorMessage:"",errorMessageKey:"badCVV"}),a.formUtils.addValidator({name:"strength",validatorFunction:function(b,c){var d=c.valAttr("strength")||2;return d&&d>3&&(d=3),a.formUtils.validators.validate_strength.calculatePasswordStrength(b)>=d},errorMessage:"",errorMessageKey:"badStrength",calculatePasswordStrength:function(a){if(a.length<4)return 0;var b=0,c=function(a,b){for(var c="",d=0;d<b.length;d++){for(var e=!0,f=0;f<a&&f+d+a<b.length;f++)e=e&&b.charAt(f+d)===b.charAt(f+d+a);f<a&&(e=!1),e?(d+=a-1,e=!1):c+=b.charAt(d)}return c};return b+=4*a.length,b+=1*(c(1,a).length-a.length),b+=1*(c(2,a).length-a.length),b+=1*(c(3,a).length-a.length),b+=1*(c(4,a).length-a.length),a.match(/(.*[0-9].*[0-9].*[0-9])/)&&(b+=5),a.match(/(.*[!,@,#,$,%,^,&,*,?,_,~].*[!,@,#,$,%,^,&,*,?,_,~])/)&&(b+=5),a.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)&&(b+=10),a.match(/([a-zA-Z])/)&&a.match(/([0-9])/)&&(b+=15),a.match(/([!,@,#,$,%,^,&,*,?,_,~])/)&&a.match(/([0-9])/)&&(b+=15),a.match(/([!,@,#,$,%,^,&,*,?,_,~])/)&&a.match(/([a-zA-Z])/)&&(b+=15),(a.match(/^\w+$/)||a.match(/^\d+$/))&&(b-=10),b<0&&(b=0),b>100&&(b=100),b<20?0:b<40?1:b<=60?2:3},strengthDisplay:function(b,c){var d={fontSize:"12pt",padding:"4px",bad:"Very bad",weak:"Weak",good:"Good",strong:"Strong"};c&&a.extend(d,c),b.bind("keyup",function(){var b=a(this).val(),c="undefined"==typeof d.parent?a(this).parent():a(d.parent),e=c.find(".strength-meter"),f=a.formUtils.validators.validate_strength.calculatePasswordStrength(b),g={background:"pink",color:"#FF0000",fontWeight:"bold",border:"red solid 1px",borderWidth:"0px 0px 4px",display:"inline-block",fontSize:d.fontSize,padding:d.padding},h=d.bad;0===e.length&&(e=a("<span></span>"),e.addClass("strength-meter").appendTo(c)),b?e.show():e.hide(),1===f?h=d.weak:2===f?(g.background="lightyellow",g.borderColor="yellow",g.color="goldenrod",h=d.good):f>=3&&(g.background="lightgreen",g.borderColor="darkgreen",g.color="darkgreen",h=d.strong),e.css(g).text(h)})}});var f=function(b,c,d,e,f){var g=c.valAttr("req-params")||c.data("validation-req-params")||{},h=c.valAttr("param-name")||c.attr("name"),i=function(a,b){b(a)};if(!h)throw new Error("Missing input name used for http requests made by server validator");g||(g={}),"string"==typeof g&&(g=a.parseJSON(g)),g[h]=d,a.ajax({url:b,type:"POST",cache:!1,data:g,dataType:"json",error:function(a){return i({valid:!1,message:"Connection failed with status: "+a.statusText},f),!1},success:function(a){i(a,f)}})};a.formUtils.addAsyncValidator({name:"server",validatorFunction:function(a,b,c,d,e,g){var h=c.valAttr("url")||d.backendUrl||document.location.href;g.addClass("validating-server-side"),c.addClass("validating-server-side"),f(h,c,b,d,function(b){g.removeClass("validating-server-side"),c.removeClass("validating-server-side"),b.message&&c.attr(d.validationErrorMsgAttribute,b.message),a(b.valid)})},errorMessage:"",errorMessageKey:"badBackend"}),a.formUtils.addValidator({name:"letternumeric",validatorFunction:function(b,c,d,e){var f="^([a-zA-Z0-9ÂªÂµÂºÃ€-Ã–Ã˜-Ã¶Ã¸-ËË†-Ë‘Ë -Ë¤Ë¬Ë®Í°-Í´Í¶Í·Íº-Í½Î†Îˆ-ÎŠÎŒÎŽ-Î¡Î£-ÏµÏ·-ÒÒŠ-Ô§Ô±-Õ–Õ™Õ¡-Ö‡×-×ª×°-×²Ø -ÙŠÙ®Ù¯Ù±-Û“Û•Û¥Û¦Û®Û¯Ûº-Û¼Û¿ÜÜ’-Ü¯Ý-Þ¥Þ±ßŠ-ßªß´ßµßºà €-à •à šà ¤à ¨à¡€-à¡˜à¢ à¢¢-à¢¬à¤„-à¤¹à¤½à¥à¥˜-à¥¡à¥±-à¥·à¥¹-à¥¿à¦…-à¦Œà¦à¦à¦“-à¦¨à¦ª-à¦°à¦²à¦¶-à¦¹à¦½à§Žà§œà§à§Ÿ-à§¡à§°à§±à¨…-à¨Šà¨à¨à¨“-à¨¨à¨ª-à¨°à¨²à¨³à¨µà¨¶à¨¸à¨¹à©™-à©œà©žà©²-à©´àª…-àªàª-àª‘àª“-àª¨àªª-àª°àª²àª³àªµ-àª¹àª½à«à« à«¡à¬…-à¬Œà¬à¬à¬“-à¬¨à¬ª-à¬°à¬²à¬³à¬µ-à¬¹à¬½à­œà­à­Ÿ-à­¡à­±à®ƒà®…-à®Šà®Ž-à®à®’-à®•à®™à®šà®œà®žà®Ÿà®£à®¤à®¨-à®ªà®®-à®¹à¯à°…-à°Œà°Ž-à°à°’-à°¨à°ª-à°³à°µ-à°¹à°½à±˜à±™à± à±¡à²…-à²Œà²Ž-à²à²’-à²¨à²ª-à²³à²µ-à²¹à²½à³žà³ à³¡à³±à³²à´…-à´Œà´Ž-à´à´’-à´ºà´½àµŽàµ àµ¡àµº-àµ¿à¶…-à¶–à¶š-à¶±à¶³-à¶»à¶½à·€-à·†à¸-à¸°à¸²à¸³à¹€-à¹†àºàº‚àº„àº‡àºˆàºŠàºàº”-àº—àº™-àºŸàº¡-àº£àº¥àº§àºªàº«àº­-àº°àº²àº³àº½à»€-à»„à»†à»œ-à»Ÿà¼€à½€-à½‡à½‰-à½¬à¾ˆ-à¾Œá€€-á€ªá€¿á-á•áš-áá¡á¥á¦á®-á°áµ-á‚á‚Žá‚ -áƒ…áƒ‡áƒáƒ-áƒºáƒ¼-á‰ˆá‰Š-á‰á‰-á‰–á‰˜á‰š-á‰á‰ -áŠˆáŠŠ-áŠáŠ-áŠ°áŠ²-áŠµáŠ¸-áŠ¾á‹€á‹‚-á‹…á‹ˆ-á‹–á‹˜-áŒáŒ’-áŒ•áŒ˜-ášáŽ€-áŽáŽ -á´á-á™¬á™¯-á™¿áš-áššáš -á›ªáœ€-áœŒáœŽ-áœ‘áœ -áœ±á€-á‘á -á¬á®-á°áž€-áž³áŸ—áŸœá  -á¡·á¢€-á¢¨á¢ªá¢°-á£µá¤€-á¤œá¥-á¥­á¥°-á¥´á¦€-á¦«á§-á§‡á¨€-á¨–á¨ -á©”áª§á¬…-á¬³á­…-á­‹á®ƒ-á® á®®á®¯á®º-á¯¥á°€-á°£á±-á±á±š-á±½á³©-á³¬á³®-á³±á³µá³¶á´€-á¶¿á¸€-á¼•á¼˜-á¼á¼ -á½…á½ˆ-á½á½-á½—á½™á½›á½á½Ÿ-á½½á¾€-á¾´á¾¶-á¾¼á¾¾á¿‚-á¿„á¿†-á¿Œá¿-á¿“á¿–-á¿›á¿ -á¿¬á¿²-á¿´á¿¶-á¿¼â±â¿â‚-â‚œâ„‚â„‡â„Š-â„“â„•â„™-â„â„¤â„¦â„¨â„ª-â„­â„¯-â„¹â„¼-â„¿â……-â…‰â…Žâ†ƒâ†„â°€-â°®â°°-â±žâ± -â³¤â³«-â³®â³²â³³â´€-â´¥â´§â´­â´°-âµ§âµ¯â¶€-â¶–â¶ -â¶¦â¶¨-â¶®â¶°-â¶¶â¶¸-â¶¾â·€-â·†â·ˆ-â·Žâ·-â·–â·˜-â·žâ¸¯ã€…ã€†ã€±-ã€µã€»ã€¼ã-ã‚–ã‚-ã‚Ÿã‚¡-ãƒºãƒ¼-ãƒ¿ã„…-ã„­ã„±-ã†Žã† -ã†ºã‡°-ã‡¿ã€-ä¶µä¸€-é¿Œê€€-ê’Œê“-ê“½ê”€-ê˜Œê˜-ê˜Ÿê˜ªê˜«ê™€-ê™®ê™¿-êš—êš -ê›¥êœ—-êœŸêœ¢-êžˆêž‹-êžŽêž-êž“êž -êžªêŸ¸-ê ê ƒ-ê …ê ‡-ê Šê Œ-ê ¢ê¡€-ê¡³ê¢‚-ê¢³ê£²-ê£·ê£»ê¤Š-ê¤¥ê¤°-ê¥†ê¥ -ê¥¼ê¦„-ê¦²ê§ê¨€-ê¨¨ê©€-ê©‚ê©„-ê©‹ê© -ê©¶ê©ºêª€-êª¯êª±êªµêª¶êª¹-êª½ê«€ê«‚ê«›-ê«ê« -ê«ªê«²-ê«´ê¬-ê¬†ê¬‰-ê¬Žê¬‘-ê¬–ê¬ -ê¬¦ê¬¨-ê¬®ê¯€-ê¯¢ê°€-íž£íž°-íŸ†íŸ‹-íŸ»ï¤€-ï©­ï©°-ï«™ï¬€-ï¬†ï¬“-ï¬—ï¬ï¬Ÿ-ï¬¨ï¬ª-ï¬¶ï¬¸-ï¬¼ï¬¾ï­€ï­ï­ƒï­„ï­†-ï®±ï¯“-ï´½ïµ-ï¶ï¶’-ï·‡ï·°-ï·»ï¹°-ï¹´ï¹¶-ï»¼ï¼¡-ï¼ºï½-ï½šï½¦-ï¾¾ï¿‚-ï¿‡ï¿Š-ï¿ï¿’-ï¿—ï¿š-ï¿œ",g="]+)$",h=c.valAttr("allowing"),i="";if(h){i=f+h+g;var j=h.replace(/\\/g,"");j.indexOf(" ")>-1&&(j=j.replace(" ",""),j+=e.andSpaces||a.formUtils.LANG.andSpaces),this.errorMessage=e.badAlphaNumeric+e.badAlphaNumericExtra+j}else i=f+g,this.errorMessage=e.badAlphaNumeric;return new RegExp(i).test(b)},errorMessage:"",errorMessageKey:"requiredFields"}),a.formUtils.addValidator({name:"complexity",validatorFunction:function(b,c,d,e){var f=c.valAttr("require-uc-letter")||"0",g=c.valAttr("require-lc-letter")||"0",h=c.valAttr("require-special-char")||"0",i=c.valAttr("require-numeral")||"0",j=c.valAttr("require-length")||"0",k={"uc-letter":{pattern:"^(?=(?:.*[A-Z]){"+f+",}).+",numRequired:f,dialogEnd:e.passwordComplexityUppercaseInfo},"lc-letter":{pattern:"^(?=(?:.*[a-z]){"+g+",}).+",numRequired:g,dialogEnd:e.passwordComplexityLowercaseInfo},"special-char":{pattern:"^(?=(?:.*(_|[!\"#$%&'()*+\\\\,-./:;<=>?@[\\]^_`{|}~])){"+h+",}).+",numRequired:h,dialogEnd:e.passwordComplexitySpecialCharsInfo},numeral:{pattern:"^(?=(?:.*\\d){"+i+",}).+",numRequired:i,dialogEnd:e.passwordComplexityNumericCharsInfo},length:{callback:function(a){return a.length>=j},numRequired:j,dialogEnd:e.lengthBadEnd}},l="";return a.each(k,function(a,d){var f=parseInt(d.numRequired,10);if(f){var g=new RegExp(d.pattern),h=!1;h=d.callback?d.callback(b):g.test(b),h?c.trigger("complexityRequirementValidation",[!0,a]):(""===l&&(l=e.passwordComplexityStart),l+=e.passwordComplexitySeparator+f+d.dialogEnd,c.trigger("complexityRequirementValidation",[!1,a]))}}),!l||(this.errorMessage=l+e.passwordComplexityEnd,!1)},errorMessage:"",errorMessageKey:""}),a.formUtils.addValidator({name:"recaptcha",validatorFunction:function(a,b){return""!==grecaptcha.getResponse(b.valAttr("recaptcha-widget-id"))},errorMessage:"",errorMessageKey:"badreCaptcha"}),a.fn.displayPasswordStrength=function(b){return new a.formUtils.validators.validate_strength.strengthDisplay(this,b),this};var g=function(b,c,d){if(c||(c=a("form")),"undefined"!=typeof grecaptcha&&!a.formUtils.hasLoadedGrecaptcha)throw new Error("reCaptcha API can not be loaded by hand, delete reCaptcha API snippet.");if(!a.formUtils.hasLoadedGrecaptcha&&a('[data-validation~="recaptcha"]',c).length){a.formUtils.hasLoadedGrecaptcha=!0;var e="//www.google.com/recaptcha/api.js?onload=reCaptchaLoaded&render=explicit"+(d.lang?"&hl="+d.lang:""),f=document.createElement("script");f.type="text/javascript",f.async=!0,f.defer=!0,f.src=e,document.getElementsByTagName("body")[0].appendChild(f)}};b.reCaptchaLoaded=function(b){b&&"object"==typeof b&&b.length||(b=a("form")),b.each(function(){var b=a(this),c=b.get(0).validationConfig||b.context.validationConfig||!1;c&&a('[data-validation~="recaptcha"]',b).each(function(){var d=a(this),e=document.createElement("DIV"),f=c.reCaptchaSiteKey||d.valAttr("recaptcha-sitekey"),g=c.reCaptchaTheme||d.valAttr("recaptcha-theme")||"light",h=c.reCaptchaSize||d.valAttr("recaptcha-size")||"normal",i=c.reCaptchaType||d.valAttr("recaptcha-type")||"image";if(!f)throw new Error("Google reCaptcha site key is required.");var j=grecaptcha.render(e,{sitekey:f,theme:g,size:h,type:i,callback:function(a){b.find('[data-validation~="recaptcha"]').trigger("validation",a&&""!==a)},"expired-callback":function(){b.find('[data-validation~="recaptcha"]').trigger("validation",!1)}});d.valAttr("recaptcha-widget-id",j).hide().on("beforeValidation",function(a){a.stopImmediatePropagation()}).parent().append(e)})})},a(b).on("validatorsLoaded formValidationSetup",g)}(a,window)});