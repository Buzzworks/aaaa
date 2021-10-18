from django import template
from django.utils.crypto import get_random_string
from django.templatetags import static
from django.conf import settings

register = template.Library()


class StaticExtraNode(static.StaticNode):

    def render(self, context):
        files = ['bootstrap', 'melody','font-awesome','validator','dataTables','jpg','png','jpeg']
        url = super().render(context)
        files_match = [True for match in files if match in url]
        if not files_match:
            return super().render(context) + '?__v__=' + settings.URL_PARAMETER
        else:
            return super().render(context)

@register.tag('static')
def do_static_extra(parser, token):
    return StaticExtraNode.handle_token(parser, token)


def static_extra(path):
    return StaticExtraNode.handle_simple(path)