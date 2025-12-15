import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def convert_links(content):
    regex = r"\[\[([\S]+)\|([\S ]+)\]\]"
    result = r'<a href="\1">\2</a>'
    content = re.sub(regex, result, str(content))
    return mark_safe(content)
