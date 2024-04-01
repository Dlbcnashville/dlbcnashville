from django import template
from home.models import ContactFormSettings

register = template.Library()
# https://docs.djangoproject.com/en/4.2/howto/custom-template-tags/


@register.simple_tag(takes_context=True)
def get_contact_form(context):
    request = context['request']
    # print(request)
    contact_form_settings = ContactFormSettings.for_request(request)
    contact_form_page = contact_form_settings.request_form_page.specific
    form = contact_form_page.get_form(
        page=contact_form_page, user=request.user)
    return {'page': contact_form_page, 'form': form}