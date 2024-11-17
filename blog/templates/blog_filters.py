from django import template

register = template.Library()

@register.filter
def get_file_fields(obj):
    return [field for field in obj._meta.fields if field.name.startswith('file') and getattr(obj, field.name)]
