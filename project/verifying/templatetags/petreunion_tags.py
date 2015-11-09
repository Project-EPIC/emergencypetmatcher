from django import template
register = template.Library()

@register.inclusion_tag("verifying/petreunion_table.html")
def show_petreunion_table(petreunion_fields):
  return {"fields": petreunion_fields}