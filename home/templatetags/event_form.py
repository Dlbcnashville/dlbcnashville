# from django import template
# from home.models import EventFormSettings

# register = template.Library()
# # https://docs.djangoproject.com/en/4.2/howto/custom-template-tags/


# @register.simple_tag(takes_context=True)
# def get_event_form(context):
#     request = context['request']
#     event_form_settings = EventFormSettings.for_request(request)
#     event_form_page = event_form_settings.event_form_page.specific
#     form = event_form_page.get_form(
#         page=event_form_page, user=request.user)
#     return {'page': event_form_page, 'form': form}