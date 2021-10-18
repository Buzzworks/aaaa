showSuccessToast = function(text, position) {
    'use strict';
    resetToastPosition();
    $.toast({
      heading: 'Success',
      text: text,
      showHideTransition: 'slide',
      icon: 'success',
      loaderBg: '#f96868',
      position: position
    })
};

showInfoToast = function(text, position,mill_sec=2000) {
  resetToastPosition();
  $.toast({
    heading: 'Info',
    text: text,
    showHideTransition: 'slide',
    icon: 'info',
    loaderBg: '#46c35f',
    position: position,
    hideAfter:mill_sec,
  })
};
showWarningToast = function(text, position,mill_sec=2000) {

  resetToastPosition();
  $.toast({
    heading: 'Warning',
    text: String(text),
    position: String(position),
    showHideTransition: 'slide',
    icon: 'warning',
    loaderBg: '#57c7d4',
    hideAfter:mill_sec
  })
};
showDangerToast = function(title, text,position,mill_sec=2000) {
  resetToastPosition();
  $.toast({
    heading: String(title),
    text: String(text),
    position: String(position),
    showHideTransition: 'slide',
    icon: 'error',
    loaderBg: '#f2a654',
    position: position,
    hideAfter:mill_sec
  })
};

resetToastPosition = function() {
  $('.jq-toast-wrap').removeClass('bottom-left bottom-right top-left top-right mid-center'); // to remove previous position class
  $(".jq-toast-wrap").css({
    "top": "",
    "left": "",
    "bottom": "",
    "right": ""
  }); //to remove previous position style
}

showSuccessStickyToast = function(title,text, position,mill_sec=2000) {
    resetToastPosition();
    $.toast({
      heading: title,
      text: text,
      showHideTransition: 'slide',
      icon: 'success',
      loaderBg: '#f96868',
      position: position,
      hideAfter:mill_sec
    })
};
