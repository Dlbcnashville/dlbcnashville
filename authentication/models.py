from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel, PageChooserPanel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from cloudinary.models import CloudinaryField

@register_snippet
class Gender(models.Model):
    gender = models.CharField(max_length=200, null=True, blank=True)
    panels = [
        FieldPanel('gender'),
    ]

    def __str__(self):
        return self.gender
    
    class Meta:
        verbose_name_plural = _("Gender")

class User(AbstractUser):
    country = models.CharField(verbose_name='country', max_length=255, null=True, blank=True)
    region = models.CharField(verbose_name='region', max_length=255, null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)
    MEMBER_CHOICE= (
        ("Worker", "Worker"),
        ("New Convert", "New Convert"),
        ("Member", "Member"),
    )
    status = models.CharField(max_length=100, choices=MEMBER_CHOICE, default="Member")
    # status = models.ForeignKey(MembershipStatus, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    residential_address = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = CloudinaryField("image", null=True, blank=True)

    def get_absolute_url(self):
        return reverse('authentication:member_profile', kwargs={'pk': self.pk})