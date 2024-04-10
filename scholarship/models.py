from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page
from cloudinary.models import CloudinaryField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

# Create your models here.
class ScholarshipIndexPage(Page):
    template = 'scholarship/scholarship_list.html'
    intro = RichTextField(blank=True)
    banner = CloudinaryField("image", null=True, help_text="Select a background banner image")
    church_invitation_heading = models.CharField(max_length=500, null=True, blank=True)
    church_invitation_body = RichTextField(blank=True, null=True, help_text="Write a short invitation message")
    academic_charge = RichTextField(blank=True, null=True, help_text="Write a short inspiring educational message")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('banner'),
        FieldPanel('church_invitation_heading'),
        FieldPanel('church_invitation_body'),
        FieldPanel('academic_charge')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(ScholarshipIndexPage, self).get_context(request, *args, **kwargs)

        scholarships = ScholarshipPage.objects.all()
        
        context["scholarships"] = scholarships
        return context

class ScholarshipPage(Page):
    template = 'scholarship/scholarship_page.html'
    scholarship_title = models.CharField(max_length=500, null=True, blank=True)
    short_description = models.CharField(max_length=1000, null=True, blank=True, help_text="Enter a text less than 250 words")
    display_on_home_page = models.BooleanField(default=False)
    scholarship_image = CloudinaryField("image", null=True, blank=True)
    scholarship_body = RichTextField(null=True)


    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('scholarship_title'),
            FieldPanel('short_description'),
            FieldPanel('display_on_home_page'),
            FieldPanel('scholarship_image'),
        ], heading="Post information"),
        
        FieldPanel('scholarship_body'),
    ]

    def save(self, *args, **kwargs):
        if self.display_on_home_page:
            ScholarshipPage.objects.all().update(**{'display_on_home_page': False})
        super(ScholarshipPage, self).save(*args, **kwargs)