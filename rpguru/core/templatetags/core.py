"""RPGuru Template tags & filters"""

from django import template

register = template.Library()


@register.filter
def spacer(value):
    """Adds leading space if value is not empty"""
    return ' ' + value if value is not None and value else ''


@register.filter
def field_css(field: object, css: str) -> object:
    """Rewrites CSS class attribute for a form field; also adds placeholder attribute"""
    return field.as_widget(attrs={'class': css, 'placeholder': field.label})


@register.filter
def is_field(field: object, value: str = None):
    """If value is not None, returns True if field name matches, otherwise returns field name"""
    f = field.field.__class__.__name__.lower()
    if value is not None:
        return True if f == value else False
    # value is None
    return f


@register.filter
def is_widget(field: object, value: str = None):
    """If value is not None, returns True if widget name matches, otherwise returns widget name"""
    w = field.field.widget.__class__.__name__.lower()
    if value is not None:
        return True if w == value else False
    # value is None
    return w


@register.filter
def csvlist(value: str, index: int) -> str:
    """Returns a single value from a comma separated list of values"""
    return str(value).split(',')[index]


@register.simple_tag
def call_method(obj, func, *args, **kwargs):
    """Calls method from specified object with arguments"""
    return getattr(obj, func)(*args, **kwargs)
