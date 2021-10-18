from django import template
from django.conf import settings

register = template.Library()

@register.filter
def getattribute(obj,arg):
	if hasattr(obj,str(arg)):
		return getattr(obj,arg)
	elif hasattr(obj,'get'):
		return obj[arg]
	else:
		print("%s is not attribute of %s"% (arg,obj))


@register.filter
def getcontact_info_val(obj,arg):
	if arg != 'campaign':
		sec_name = arg.split(":")[0].replace(' ','_').lower()
		arg = arg.split(":")[1].replace(' ','_').lower()

	if arg == "campaign":
		return obj.contact.phonebook.campaign_name
	elif sec_name in obj.customer_raw_data:
		if arg in obj.customer_raw_data[sec_name]:
			return obj.customer_raw_data[sec_name][arg]
	else:
		print("%s is not attribute of %s"% (arg,obj))

@register.simple_tag
def custom_format_crmfield(section_name,field_name):
	return section_name+"__"+field_name


