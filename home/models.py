from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page
from django.shortcuts import render
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.admin.panels import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel, PageChooserPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from cloudinary.models import CloudinaryField

class HomePage(Page):
    template = 'home/home_page.html'
    max_count = 1
    hero_section_title = models.CharField(max_length=500, null=True)
    hero_section_text = RichTextField(null=True, blank=True)
    about_church_title_1 = models.CharField(max_length=500, null=True, blank=True)
    about_church_text_1 = RichTextField(null=True, blank=True)
    about_church_image_1 = CloudinaryField("image", null=True, blank=True)
    about_church_title_2 = models.CharField(max_length=500, null=True, blank=True)
    about_church_text_2 = RichTextField(null=True, blank=True)
    about_church_image_2 = CloudinaryField("image", null=True, blank=True)
    about_church_title_3 = models.CharField(max_length=500, null=True, blank=True)
    about_church_text_3 = RichTextField(null=True, blank=True)
    about_church_image_3 = CloudinaryField("image", null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('hero_section_title'),
        FieldPanel('hero_section_text'),
        FieldPanel('about_church_title_1'),
        FieldPanel('about_church_text_1'),
        FieldPanel('about_church_image_1'),
        FieldPanel('about_church_title_2'),
        FieldPanel('about_church_text_2'),
        FieldPanel('about_church_image_2'),
        FieldPanel('about_church_title_3'),
        FieldPanel('about_church_text_3'),
        FieldPanel('about_church_image_3'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)

        worship_services = WorshipService.objects.all()
        daily_devotions = DailyDevotion.objects.all()
        events = Event.objects.filter(display_on_home_page=True)

        # context["home_page"] = self.home_page
        context["worship_services"] = worship_services
        context["daily_devotions"] = daily_devotions
        return context

@register_snippet
class WorshipService(models.Model):
    service_title = models.CharField(max_length=500, null=True, blank=True)
    WEEK_DAYS = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    service_day = models.CharField(max_length=500, choices=WEEK_DAYS, null=True, blank=True)
    start_time = models.CharField(max_length=500, null=True, blank=True)
    service_image = CloudinaryField("image", null=True, blank=True)

    panels = [
        FieldPanel('service_title'),
        FieldPanel('service_day'),
        FieldPanel('start_time'),
        FieldPanel('service_image'),
    ]
    def __str__(self):
        return self.service_title

@register_snippet
class Event(models.Model):
    event_name = models.CharField(max_length=500, null=True, blank=True)
    short_description = RichTextField(null=True, blank=True)
    event_date = models.DateField(null=True, blank=True)
    event_start_time =models.TimeField(null=True, blank=True)
    event_end_time =models.TimeField(null=True, blank=True)
    event_venue = models.CharField(max_length=500, null=True, blank=True)
    event_image = CloudinaryField("image", null=True, blank=True)
    display_on_home_page = models.BooleanField(default=True)
    can_register = models.BooleanField(default=False)
    external_registration = models.BooleanField(default=False)
    external_registration_link = models.URLField(null=True, blank=True)
    panels = [
        FieldPanel('event_name'),
        FieldPanel('short_description'),
        FieldPanel('event_date'),
        FieldPanel('event_start_time'),
        FieldPanel('event_end_time'),
        FieldPanel('event_venue'),
        FieldPanel('event_image'),
        FieldPanel('display_on_home_page'),
        FieldPanel('can_register'),
        FieldPanel('external_registration'),
        FieldPanel('external_registration'),
    ]
    def __str__(self):
        return self.event_name
@register_snippet
class DailyDevotion(models.Model):
    devotion_type = models.CharField(max_length=500, null=True, blank=True)
    devotion_url = models.URLField(null=True, blank=True)
    devotion_image = CloudinaryField("image", null=True, blank=True)

    panels = [
        FieldPanel('devotion_type'),
        FieldPanel('devotion_url'),
        FieldPanel('devotion_image'),
    ]
    def __str__(self):
        return self.devotion_type

class SubscribeFormField(AbstractFormField):
    page = ParentalKey('SubscribeFormPage', on_delete=models.CASCADE, related_name='form_fields')

class SubscribeFormPage(AbstractEmailForm):
    template = 'home/subscribe_form.html'
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form(request.POST, page=self, user=request.user)

            if form.is_valid():
                self.process_form_submission(form)
                
                # Update the original landing page context with other data
                landing_page_context = self.get_context(request)
                landing_page_context['email'] = form.cleaned_data['email']

                return render(
                    request,
                    self.get_landing_page_template(request),
                    landing_page_context
                )
        else:
            form = self.get_form(page=self, user=request.user)

        context = self.get_context(request)
        context['form'] = form
        return render(
            request,
            self.get_template(request),
            context
        )

@register_setting
class SubscribeFormSettings(BaseSiteSetting):
    subscribe_form_page = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL)

    panels = [
        # note the page type declared within the pagechooserpanel
        PageChooserPanel('subscribe_form_page', ['home.SubscribeFormPage']),
    ]

class About(Page):
    max_count = 1
    template = 'home/About.html'
    who_we_are = RichTextField(null=True, blank=True)
    our_belief = RichTextField(null=True, blank=True)
    ministries = RichTextField(null=True, blank=True)
    regional_overseer = RichTextField(null=True, blank=True)
    general_superintendent = RichTextField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('who_we_are'),
        FieldPanel('our_belief'),
        FieldPanel('ministries'),
        FieldPanel('regional_overseer'),
        FieldPanel('general_superintendent'),
    ]

class IamNew(Page):
    max_count = 1
    template = 'home/new.html'

    caption_title = RichTextField(null=True, blank=True)
    caption_text = RichTextField(null=True, blank=True)
    banner = CloudinaryField("image", null=True, blank=True)
    first_section_title = RichTextField(null=True, blank=True)
    first_section_body = RichTextField(null=True, blank=True)
    second_section_title = RichTextField(null=True, blank=True)
    second_section_body = RichTextField(null=True, blank=True)
    third_section_title = RichTextField(null=True, blank=True)
    third_section_body = RichTextField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('caption_title'),
        FieldPanel('caption_text'),
        FieldPanel('banner'),
        FieldPanel('first_section_title'),
        FieldPanel('first_section_body'),
        FieldPanel('second_section_title'),
        FieldPanel('second_section_body'),
        FieldPanel('third_section_title'),
        FieldPanel('third_section_body'),
    ]

class Donate(Page):
    max_count = 1
    template = 'home/donate.html'
    caption_title = RichTextField(null=True, blank=True)
    caption_text = RichTextField(null=True, blank=True)
    donate_link = models.URLField(null=True, blank=True)
    cashapp_tag = models.CharField(max_length=500, null=True, blank=True)
    cashapp_number = models.CharField(max_length=500, null=True, blank=True)
    mailing_address = models.CharField(max_length=500, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('caption_title'),
        FieldPanel('caption_text'),
        FieldPanel('donate_link'),
        FieldPanel('cashapp_tag'),
        FieldPanel('cashapp_number'),
        FieldPanel('mailing_address'),
    ]

@register_setting
class SiteSocial(BaseSiteSetting):
    facebook = models.URLField(max_length=500, null=True, blank=True)
    twitter = models.URLField(max_length=500, null=True, blank=True)
    instagram = models.URLField(max_length=500, null=True, blank=True)
    threads = models.URLField(max_length=500, null=True, blank=True)
    linkedin = models.URLField(max_length=500, null=True, blank=True)
    youtube = models.URLField(max_length=500, null=True, blank=True)
    tiktok = models.URLField(max_length=500, null=True, blank=True)


@register_setting
class SiteContact(BaseSiteSetting):
    email1 = models.EmailField(help_text='Your Email address', null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    phone2 = models.CharField(max_length=500, null=True, blank=True)

@register_setting
class SiteLogo(BaseSiteSetting):
    logo = CloudinaryField("image", null=True, blank=True)

@register_setting
class ImportantPages(BaseSiteSetting):
    # Fetch these pages when looking up ImportantPages for or a site
    select_related = ["about", "donate", "home"]

    about = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')
    donate = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')
    home = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')
    # course_index = models.ForeignKey(
    #     'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')

    panels = [
        PageChooserPanel('about', ['home.About']),
        PageChooserPanel('donate', ['home.Donate']),
        PageChooserPanel('home', ['home.HomePage']),
        # PageChooserPanel('course_index', ['course.CourseIndexPage']),
    ]

class ContactFormField(AbstractFormField):
    page = ParentalKey('ContactFormPage', on_delete=models.CASCADE, related_name='form_fields')

class ContactFormPage(AbstractEmailForm):
    template = 'home/connect_form.html'
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form(request.POST, page=self, user=request.user)

            if form.is_valid():
                self.process_form_submission(form)
                
                # Update the original landing page context with other data
                landing_page_context = self.get_context(request)
                landing_page_context['email'] = form.cleaned_data['email']

                return render(
                    request,
                    self.get_landing_page_template(request),
                    landing_page_context
                )
        else:
            form = self.get_form(page=self, user=request.user)

        context = self.get_context(request)
        context['form'] = form
        return render(
            request,
            self.get_template(request),
            context
        )
    
@register_setting
class ContactFormSettings(BaseSiteSetting):
    contact_form_page = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL)

    panels = [
        # note the page type declared within the pagechooserpanel
        PageChooserPanel('contact_form_page', ['home.ContactFormPage']),
    ]