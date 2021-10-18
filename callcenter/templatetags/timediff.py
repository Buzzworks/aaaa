from django import template

register = template.Library()



def timediff(time_first, time_second):
    from dateutil import parser

    start = parser.parse(time_first)
    end = parser.parse(time_second)
    diff = start - end
    return diff.seconds()

register.tag('timediff', timediff)
