import pandoc

from django import template


register = template.Library()


@register.filter(is_safe=True)
def markdown_to_html(value):
    # todo: cache
    doc = pandoc.Document()
    doc.markdown = value
    return doc.html
