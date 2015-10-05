from django import template
register = template.Library()

@register.inclusion_tag("reporting/petreport_table.html")
def show_petreport_table(petreport_fields):
  return {"fields": petreport_fields}