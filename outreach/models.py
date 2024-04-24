from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page
from cloudinary.models import CloudinaryField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

# Create your models here.
class OutreachIndexPage(Page):
    template = 'outreach/outreach_list.html'
    intro = RichTextField(blank=True)
    banner = CloudinaryField("image", null=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('banner')
    ]
    def get_context(self, request, *args, **kwargs):
        context = super(OutreachIndexPage, self).get_context(request, *args, **kwargs)

        outreaches = OutreachPage.objects.all()
        
        context["outreaches"] = outreaches
        return context

class OutreachPage(Page):
    template = 'outreach/outreach_page.html'
    outreach_title = models.CharField(max_length=500, null=True, blank=True)
    short_description = models.CharField(max_length=1000, null=True, blank=True, help_text="Enter a text less than 250 words")
    display_on_home_page = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    outreach_image = CloudinaryField("image", null=True, blank=True)
    outreach_body = RichTextField(null=True)


    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('outreach_title'),
            FieldPanel('short_description'),
            FieldPanel('display_on_home_page'),
            FieldPanel('outreach_image'),
        ], heading="Post information"),
        
        FieldPanel('outreach_body'),
    ]

    def save(self, *args, **kwargs):
        if self.display_on_home_page:
            OutreachPage.objects.all().update(**{'display_on_home_page': False})
        super(OutreachPage, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-date_created"]