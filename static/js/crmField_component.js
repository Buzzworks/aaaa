Vue.filter('replace',function(name){
	return name.replace(/ /g,"_");
});
Vue.component('crm-fields',{
	props:['field_schema','field_data'],
	template: `<div class="accordion accordion-solid-header" id="cust_info_accordion" role="tablist">
				<div v-for="item, key in field_schema" class="card" >
					<div class="card-header p-0" role="tab">
						<h6 class="mb-0">
							<a data-toggle="collapse" :href="'#section_collaps_'+key" aria-expanded="false"
								aria-controls="collapse-1" class="sub-dispo-heading text-capitalize collapsed p-3">
								{{item.section_name}}
							</a>
						</h6>
					</div>
					<div :id="'section_collaps_'+key" class="collapse collapse-div" role="tabpanel"
						aria-labelledby="lead-heading" data-parent="#cust_info_accordion">
						<div class="card-body">
							<div class="row">
							<template v-for="field in item.section_fields">
								<div class="col-md-6">
									<div v-if="field.field_type != 'checkbox'" class="form-group row">
										<label :for="field.field|replace" class="text-capitalize col-form-label col-sm-4">
											{{field.field}} :
										</label>
										<div class="col-sm-8">
											<!-- text field -->
											<input v-if="field.field_type == 'text'" type="text"
													class="form-control crm-form-control"
													:readonly=!field.editable 
													v-model="field_data[item.db_section_name][field.db_field]">

											<!-- textarea -->
											<textarea v-else-if="field.field_type == 'textarea'"
														class="form-control crm-form-control"  type="text" 
														:readonly=!field.editable
														v-model="field_data[item.db_section_name][field.db_field]"
											></textarea>

											<!-- radio group -->
											<div v-else-if="field.field_type == 'radio'" :id="field.field" class="form-inline">
												<div class="form-check mr-sm-3" v-for="option in split_string(field.options)">
													<label class="form-check-label">
														<input class="form-check-input"
																type="radio" :value="option" 
																:id="option" :disabled="!field.editable"
																v-model="field_data[item.db_section_name][field.db_field]">
																{{option}}
													</label>
												</div>
											</div>

											<!-- date field -->
											<datepicker v-else-if="field.field_type == 'datefield'" 
														:value=field_data[item.db_section_name][field.db_field]
														:readonly=field.editable
														v-on:set-date="field_data[item.db_section_name][field.db_field] = $event"
											></datepicker>

											<!-- Dropdowns -->
											<select v-else-if="field.field_type == 'dropdown'" 
													:id="field.field|replace" 
													class="form-control crm-form-control"
													:disabled=!field.editable 
													v-model="field_data[item.db_section_name][field.db_field]">
													<option v-for="option in split_string(field.options)" 
															:id="option" :value="option">{{option}}
													</option>
											</select>

											<!-- multiselect dropdown -->
											<select2 v-else-if="field.field_type == 'multiselect'" 
													:options="split_string(field.options)" 
													:id="field.field|replace" 
													class="form-control crm-form-control"
													:disabled=!field.editable multiple="true" 
													v-model="field_data[item.db_section_name][field.db_field]"
											></select2>

											<!-- integer field -->
											<input v-else-if="field.field_type == 'integer'"
													type="text"
													class="form-control crm-form-control" 
													:id="field.field|replace"
													onkeypress="return isNumber(event)"
													:maxlength="field.size" :readonly=!field.editable
													v-model="field_data[item.db_section_name][field.db_field]">

											<!-- timefield -->
											<timepicker v-else-if="field.field_type == 'timefield'" 
														:id = "field.field|replace"
														:target="'#'+field.field|replace"
														:readonly=field.editable
														v-bind:value="this.field_data[item.db_section_name][field.db_field]"
														v-on:set-time="field_data[item.db_section_name][field.db_field] = $event"
											></timepicker>

											<!-- datetimefield -->
											<datetimepicker v-else-if="field.field_type == 'datetimefield'" 
															:id="field.field|replace" :target="'#'+field.field|replace" 
															v-on:set-datetime="field_data[item.db_section_name][field.db_field] = $event" 
															:value=field_data[item.db_section_name][field.db_field]
															:readonly=field.editable
											></datetimepicker>

											<!-- multiple checkbox -->
											<div class="form-inline" v-else-if="field.field_type == 'multicheckbox'">
												<div class="form-check mr-sm-3" v-for="option in split_string(field.options)">
													<label class="form-check-label">
														<input class="form-check-input" 
																type="checkbox" :value="option" 
																:id="option" :disabled=!field.editable
																v-model="field_data[item.db_section_name][field.db_field]">
																{{option}}
													</label>
												</div>
											</div>
										</div>
									</div>
									<div v-else class="form-group row pt-md-3">
										<label :for="field.field" class="col-6 col-form-label text-capitalize">
											{{field.field}}:
										</label>
										<!-- checkbox -->
										<div class="col-6 form-inline">
											<div v-if="field.field_type == 'checkbox'" class="form-check">
												<label class="form-check-label">
													<input type="checkbox" class="form-check-input"
															:id="field.field|replace"
															:disabled=!field.editable 
															v-model="field_data[item.db_section_name][field.db_field]" >
												</label>
											</div>
										</div>
									</div>
								</div>
							</template>
						</div>
					</div>
				</div>
			</div>
		</div>
	`,
	methods:{
		col_span(span_val){
			return{
				'col-sm-12': span_val === "3",
				'col-sm-8' : span_val === "2",
				'col-sm-4' : span_val === "1",
			}
		},
		// to split string of option tag in dropdown
		split_string: function(string_option){
			if ( string_option !== '') {
				return string_option.split(',')
			}
		},
		// to sort section priority wise in custom crm fields
		ordered_section: function (schema) {
			return _.sortBy(schema, 'section_priority')
		},
		// to sort fields priority wise in custom crm fields
		ordered_field: function(schema){
			return _.sortBy(schema, 'priority')
		}
	},
	watch: {
		field_schema(value){
			console.log(value)
		}
	}

})

// select2 multiple select component in vue
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

// bootstrap timepicker component in vue
Vue.component('timepicker',{
	props: ['name','target','value','readonly'],
	template: '<div class="input-group date timefield" data-target-input="nearest">'+
				'<div class="input-group" :data-target=this.target data-toggle="datetimepicker">'+
				'<input type="text" :name=this.name placeholder="HH:mm" :data-target="this.target"'+ 
				'class="form-control crm-form-control datetimepicker-input" :disabled="!readonly"/>'+ 
				'<div class="input-group-addon input-group-append">'+
			'</div></div></div>',
	mounted: function(){
		var vm = this
		vm.$nextTick(function () {
			$(vm.$el).datetimepicker({
				format:'hh:mm A'
			});
			$(vm.$el).data("datetimepicker").date(this.value);
			$(vm.$el).on('change.datetimepicker' ,function(e){
				vm.$emit('set-time', e.date.format("hh:mm A"))
			})
		})
	},
	watch:{
		value: function (value){
			// update value
			this.$nextTick(function(){
				$(this.$el).data("datetimepicker")
				.date(value)
			})
		}
	},
})
// bootstrap datetimepicker component in vue
Vue.component('datetimepicker',{
	props: ['name','target','value','readonly'],
	template: '<div class="input-group date" data-target-input="nearest">'+
				'<div class="input-group" :data-target=this.target data-toggle="datetimepicker">'+
				'<input type="text" :name="this.name" placeholder="YYYY-MM-DD HH:mm" :data-target="this.target"'+ 
				'class="form-control crm-form-control datetimepicker-input" :disabled="!readonly"/>'+ 
				'<div class="input-group-addon input-group-append">'+
			'</div></div></div>',
	mounted: function(){
		var vm = this
		vm.$nextTick(function () {
			$(vm.$el)
			.datetimepicker({
				format: 'YYYY-MM-DD hh:mm A',
				sideBySide: true,
				icons: {
					time: 'fas fa-clock',
				}
			});
			$(vm.$el).data("datetimepicker").date(this.value);
			$(vm.$el).on('change.datetimepicker' ,function(e){
				vm.$emit('set-datetime', e.date.format('YYYY-MM-DD hh:mm A'))
			})
		})
	},
	watch:{
		value: function (value){
			// update value
			$(this.$el).data("datetimepicker")
			.date(value)
		}
	},
})
Vue.component('datepicker',{
	props: ['value','readonly'],
	template: `<div class="input-group date datepicker p-0">
				<input type="text" class="form-control crm-form-control" placeholder="yyyy-mm-dd" :disabled="!readonly">
				<span class="input-group-addon input-group-append">
				</span>
			</div>`,
	mounted: function(){
		var vm = this
		vm.$nextTick(function () {
			$(vm.$el)
			.datepicker({
				enableOnReadonly: false,
				todayHighlight: true,
				autoclose: true,
				format: "yyyy-mm-dd"
			})
			$(vm.$el).datepicker('update', this.value);
			$(vm.$el).on('changeDate' ,function(e){
				vm.$emit('set-date', e.format("yyyy-mm-dd"))
			})
		})
	},
	watch:{
		value: function (value){
			// update value
			$(this.$el).datepicker('update', value);
		}
	},

})