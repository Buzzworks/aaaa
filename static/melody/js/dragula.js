(function($) {
  'use strict';
  var iconTochange, selectedField;
  dragula([document.getElementById("dragula-left"), document.getElementById("dragula-right")]);
  dragula([document.getElementById("profile-list-left"), document.getElementById("profile-list-right")]);
  dragula([document.getElementById("dragula-event-left"), document.getElementById("dragula-event-right")]);
  dragula([document.getElementById("disposition-list-left"), document.getElementById("disposition-list-right")]);
  dragula([document.getElementById("relationtag-list-left"),document.getElementById("relationtag-list-right")]);
  dragula([document.getElementById("agent-breaks-left"), document.getElementById("agent-breaks-right")]);
  dragula([document.getElementById("admin-list-left"), document.getElementById("admin-list-right")])
    .on('drop', function(el) {
      iconTochange = $(el).find('.fa');
      if (iconTochange.hasClass('text-primary')) {
        iconTochange.removeClass('text-primary').addClass('text-success');
      } else if (iconTochange.hasClass('text-success')) {
        iconTochange.removeClass('text-success').addClass('text-primary');
      }
    })

  // script dragula 
  dragula([document.getElementById("nameSpacingField-left"), document.getElementById("nameSpacingField-right")])
    .on('drop', function(el){
       var element = $(el)
      selectedField = element.text()
      if(element.hasClass('selected')){
        element.removeClass('selected')
        $('#tinymce').find('#'+selectedField).remove()
      } else{
        element.addClass('selected')
        tinyMCE.activeEditor.insertContent('<strong class="mceNonEditable" id="'+selectedField+'"> ${'+selectedField+'}</strong>');
      }
    });
})(jQuery);