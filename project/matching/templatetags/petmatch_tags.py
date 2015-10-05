from django import template
register = template.Library()

@register.inclusion_tag("matching/petmatch_table.html")
def show_petmatch_table(petreport_fields):
  return {"fields": petreport_fields}