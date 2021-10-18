// this js for initialize and functionality for tinymce editior on script page.

function addScriptEditior(data,height=500){
	if ($("#scriptEditor").length) {
		tinymce.PluginManager.add('field_btn', function (editor, url) {
			editor.addButton('field_btn', {
				text: 'Add FIelds',
				type: 'menubutton',
				icon: false,
				menu: data,
				onselect: function(e) {
					editor.insertContent('<strong class="non-editable" data-id="'+e.target.settings.value+'">${'+e.target.settings.value+'}</strong>');
				}
			});
		});
		tinymce.init({
			selector: '#scriptEditor',
			height: height,
			theme: 'modern',
			plugins: [
				'advlist autolink lists link image charmap print preview hr anchor pagebreak',
				'searchreplace wordcount visualblocks visualchars code',
				'insertdatetime media nonbreaking save table contextmenu directionality',
				'emoticons template paste textcolor colorpicker textpattern imagetools codesample toc help noneditable field_btn'
			],
			noneditable_noneditable_class: "non-editable",
			toolbar1: 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
			toolbar2: 'print preview media | forecolor backcolor emoticons | codesample help | template | field_btn',
			image_advtab: true,
			templates: [{
					title: 'Test template 1',
					content: 'Test 1'
				},
				{
					title: 'Test template 2',
					content: 'Test 2'
				}
			],
			content_css: []
		});
		
	}
}

function addTTSEditior(data){
	$(".hint2mention").summernote({
		height: 100,
		toolbar: false,
		placeholder: 'Enter voice blaster speech',
		hint: {
			mentions: data,
			match: /\B\$(\w*)$/,
			search: function (keyword, callback) {
				callback($.grep(this.mentions, function (item) {
					return item.indexOf(keyword) == 0;
				}));
			},
			content: function (item) {
				if(vb_crm_fields.indexOf(item) == -1){
					vb_crm_fields.push(item)
				}
				return '${' + item + '}';
			}
		}
	});
}