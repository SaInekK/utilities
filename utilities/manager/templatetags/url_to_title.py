from django import template

register = template.Library()


@register.filter(name='url_to_title')
def cut(value: str) -> str:
    return value.replace('-', ' ').title()
