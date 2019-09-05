from django import template

register = template.Library()

@register.simple_tag
def join_queryset(queryset,field):
    field_values = queryset.values(field)
    value_list =[]
    for item in field_values:
        value_list.append(item[field])

    return ','.join(value_list)