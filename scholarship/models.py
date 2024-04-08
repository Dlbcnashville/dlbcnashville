from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page
from cloudinary.models import CloudinaryField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

# Create your models here.
class ScholarshipIndexPage(Page):
    template = 'scholarship/scholarship_list.html'
    intro = RichTextField(blank=True)
    banner = CloudinaryField("image", null=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('banner')
    ]

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