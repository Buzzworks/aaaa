from django import template
from django.conf import settings

register = template.Library()

@register.filter
def dict_values_list(data):
	return list(data)
