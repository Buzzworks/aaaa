from django import template
from django.conf import settings
import datetime

register = template.Library()

@register.filter
def getattribute(obj,arg): 
	if hasattr(obj,str(arg)):
		if isinstance(getattr(obj,arg),datetime.time):
			return getattr(obj,arg).strftime('%H:%M:%S')
		return getattr(obj,arg)
	elif hasattr(obj,'get'):
		if arg in obj : 
			return obj[arg]
		else:
			return ""
	# else:
		# print("%s is not attribute of %s"% (arg,obj))

@register.filter 
def table_header(name):
	return str(name).replace("_"," ")

@register.filter
def convert_in_json(data):
	data = str(data).replace('True', 'true').replace('False', 'false').replace('None','null')
	return data

@register.filter
def get_type(value):
    return type(value)

@register.filter
def str_convert(value):
    return str(value)

@register.filter
def crm_header(value):
	if len(value.split(":")) > 1:
		return value.split(":")[1]
	return value.split(":")

@register.filter
def list_convert(value):
	return value.split(',')