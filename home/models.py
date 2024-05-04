from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page
from django.shortcuts import render
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.admin.panels import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel, PageChooserPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractFormSubmission
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from cloudinary.models import CloudinaryField
from django.shortcuts import get_object_or_404
from scholarship.models import ScholarshipPage
from outreach.models import OutreachPage
from django.urls import reverse
from wagtail.admin.forms import WagtailAdminModelForm, WagtailAdminPageForm

class HomePage(Page):
    template = 'home/home_page.html'
    max_count = 1
    banner = CloudinaryField("image", null=True, blank=True, help_text="Select the background image for the hero section")
    hero_section_title = models.CharField(max_length=500, null=True)
    hero_section_text = RichTextField(null=True, blank=True)
    about_church_title_1 = models.CharField(max_length=500, null=True, blank=True)
    about_church_text_1 = RichTextField(null=True, blank=True)
    about_church_image_1 = CloudinaryField("image", null=True, blank=True, help_text="Select the first about us image")
    about_church_title_2 = models.CharField(max_length=500, null=True, blank=True)
    about_church_text_2 = RichTextField(null=True, blank=True)
    about_church_image_2 = CloudinaryField("image", null=True, blank=True, help_text="Select the second about us image")
    about_church_title_3 = models.CharField(max_length=500, null=True, blank=True)
    about_church_text_3 = RichTextField(null=True, blank=True)
    about_church_image_3 = CloudinaryField("image", null=True, blank=True, help_text="Select the third about us image")
    donate_main_text = models.CharField(max_length=500, null=True, blank=True, help_text="make text as short as possible")
    donate_main_subtext = models.CharField(max_length=1000, null=True, blank=True, help_text="make text as short as possible")
    donate_background_image = CloudinaryField("image", null=True, blank=True, help_text="Select image to use as donate background image")
    church_name = models.CharField(max_length=500, null=True, blank=True, help_text="Enter the name of the church e.g DLCF Nashville")
    church_address = models.CharField(max_length=500, null=True, blank=True, help_text="Enter the church address")
    church_google_map_embed_iframe  = models.URLField(max_length=1000, null=True, blank=True, help_text="Enter the church location google map iframe embed src link")
    church_location_image = CloudinaryField("image", null=True, blank=True, help_text="Select image of church location")
    church_description1 = models.CharField(max_length=500, null=True, blank=True, help_text="Enter a very short inspiring message here")
    church_description2 = models.CharField(max_length=500, null=True, blank=True, help_text="Enter a very short inspiring message here")
    connect_with_us_sub_text = models.CharField(max_length=500, null=True, blank=True, help_text="Enter a very short inspiring message here")
    connect_with_us_image = CloudinaryField("image", null=True, blank=True, help_text="Select image for connect with us background image")
    content_panels = Page.content_panels + [
        FieldPanel('banner'),
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
        FieldPanel('donate_main_text'),
        FieldPanel('donate_main_subtext'),
        FieldPanel('donate_background_image'),
        FieldPanel('church_name'),
        FieldPanel('church_google_map_embed_iframe'),
        FieldPanel('church_location_image'),
        FieldPanel('church_description1'),
        FieldPanel('church_description2'),
        FieldPanel('connect_with_us_sub_text'),
        FieldPanel('connect_with_us_image'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)

        worship_services = WorshipService.objects.all()
        daily_devotions = DailyDevotion.objects.all()
        events = Event.objects.filter(display_on_home_page=True)
        scholarship = get_object_or_404(ScholarshipPage, display_on_home_page=True)
        outreach = get_object_or_404(OutreachPage, display_on_home_page=True)
        event_registration_form = get_object_or_404(EventRegistrationFormPage)

        context["event_registration_form"] = event_registration_form
        context["worship_services"] = worship_services
        context["daily_devotions"] = daily_devotions
        context["events"] = events
        context["scholarship"] = scholarship
        context["outreach"] = outreach
        return context

@register_snippet
class WorshipService(models.Model):
    service_title = models.CharField(max_length=500, null=True, blank=True)
    service_description = models.CharField(max_length=500, null=True, blank=True)
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
        FieldPanel('service_description'),
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
    event_start_date = models.DateField(null=True, blank=True)
    event_end_date = models.DateField(null=True, blank=True)
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
        FieldPanel('event_start_date'),
        FieldPanel('event_end_date'),
        FieldPanel('event_start_time'),
        FieldPanel('event_end_time'),
        FieldPanel('event_venue'),
        FieldPanel('event_image'),
        FieldPanel('display_on_home_page'),
        FieldPanel('can_register'),
        FieldPanel('external_registration'),
        FieldPanel('external_registration_link'),
    ]
    def __str__(self):
        return self.event_name
    

class EventRegistration(models.Model):
    first_name = models.CharField(max_length=1000, null=True)
    last_name = models.CharField(max_length=1000, null=True)
    # phone = models.CharField(max_length=1000, null=True)
    email = models.EmailField(null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse('home:event-detail', kwargs={'pk': self.id})

class EventRegistrationFormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thankyou_page_title = models.CharField(
        max_length=255, help_text="Title text to use for the 'thank you' page")

    # Note that there's nothing here for specifying the actual form fields -
    # those are still defined in forms.py. There's no benefit to making these
    # editable within the Wagtail admin, since you'd need to make changes to
    # the code to make them work anyway.

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro', classname="full"),
        FieldPanel('thankyou_page_title'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]


    def serve(self, request):
        from .form import EventForm

        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save()
                return render(request, 'home/event_form_landing.html', {
                    'page': self,
                    'event': event,
                })
        else:
            form = EventForm()

        return render(request, 'home/event_form.html', {
            'page': self,
            'form': form,
        })

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
    who_we_are_image = CloudinaryField("image", null=True, blank=True, help_text="Who we are image")
    our_belief = RichTextField(null=True, blank=True)
    our_belief_image = CloudinaryField("image", null=True, blank=True, help_text="Our believe image")
    # ministries = RichTextField(null=True, blank=True)
    advert_image = CloudinaryField("image", null=True, blank=True, help_text="You can add a unique advertisement banner image here")
    regional_overseer = RichTextField(null=True, blank=True)
    general_superintendent = RichTextField(null=True, blank=True)
    GS_image = CloudinaryField("image", null=True, blank=True, help_text="Select image of the General Superintendent")
    message_from_location_church_heading = models.CharField(max_length=500, null=True, blank=True, help_text="Write a short inspiring heading")
    message_from_location_church_text = RichTextField(null=True, blank=True, help_text="Write a short inspiring message here")
    message_from_location_church_text2 = RichTextField(null=True, blank=True, help_text="Write a short inspiring message here")
    location_church_image1 = CloudinaryField("image", null=True, blank=True, help_text="Location church image 1")
    location_church_image2 = CloudinaryField("image", null=True, blank=True, help_text="Location church image 2")
    location_church_image3 = CloudinaryField("image", null=True, blank=True, help_text="Location church image 3")
    learn_more = models.URLField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('who_we_are'),
        FieldPanel('who_we_are_image'),
        FieldPanel('our_belief'),
        FieldPanel('our_belief_image'),
        FieldPanel('advert_image'),
        FieldPanel('regional_overseer'),
        FieldPanel('general_superintendent'),
        FieldPanel('GS_image'),
        FieldPanel('message_from_location_church_heading'),
        FieldPanel('message_from_location_church_text'),
        FieldPanel('message_from_location_church_text2'),
        FieldPanel('location_church_image1'),
        FieldPanel('location_church_image2'),
        FieldPanel('location_church_image3'),
        FieldPanel('learn_more'),
    ]

class IamNew(Page):
    max_count = 1
    template = 'home/new.html'

    caption_title = models.CharField(max_length=1000, null=True, blank=True, help_text="Write a short inspiring heading")
    caption_text = RichTextField(null=True, blank=True)
    banner = CloudinaryField("image", null=True, blank=True, help_text="Select a background image banner")
    first_section_title = models.CharField(max_length=1000, null=True, blank=True, help_text="Write a short inspiring heading")
    first_section_body = RichTextField(null=True, blank=True)
    second_section_title = models.CharField(max_length=1000, null=True, blank=True, help_text="Write a short inspiring heading")
    second_section_body = RichTextField(null=True, blank=True)
    third_section_title = models.CharField(max_length=1000, null=True, blank=True, help_text="Write a short inspiring heading")
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
    donate_account_name = models.CharField(max_length=500, null=True, blank=True)
    donate_account_tag = models.CharField(max_length=500, null=True, blank=True)
    donate_account_number = models.CharField(max_length=500, null=True, blank=True)
    donate_account_image = CloudinaryField("image", null=True, blank=True, help_text="Upload an image for the donate account")
    mailing_address = models.CharField(max_length=500, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('caption_title'),
        FieldPanel('caption_text'),
        FieldPanel('donate_link'),
        FieldPanel('donate_account_name'),
        FieldPanel('donate_account_tag'),
        FieldPanel('donate_account_number'),
        FieldPanel('donate_account_image'),
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
    select_related = ["about", "donate", "home", "scholarship", "outreach", "contact"]

    about = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')
    donate = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')
    home = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')
    scholarship = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')
    outreach = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')
    contact = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')

    panels = [
        PageChooserPanel('about', ['home.About']),
        PageChooserPanel('donate', ['home.Donate']),
        PageChooserPanel('home', ['home.HomePage']),
        PageChooserPanel('scholarship', ['scholarship.ScholarshipIndexPage']),
        PageChooserPanel('outreach', ['outreach.OutreachIndexPage']),
        PageChooserPanel('contact', ['home.ContactFormPage']),
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