from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def check_user_r_campaigns(obj,extension,campaign):
	if extension in obj[campaign]:
		return True
	else:
		return False
