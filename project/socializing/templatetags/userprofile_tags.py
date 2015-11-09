from django import template
register = template.Library()

@register.inclusion_tag("socializing/userprofile_table.html")
def show_userprofile_table(show_profile, userprofile):
  return {"show_profile": show_profile, "userprofile":userprofile}