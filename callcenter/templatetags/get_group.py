from django import template

register = template.Library()

@register.simple_tag
def get_user_group(user):
	if user.user_role:
		if user.user_role.name == 'admin':
			return True
	return False
