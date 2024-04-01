from django.db import models
from wagtail.fields import RichTextField
from modelcluster.fields import ParentalManyToManyField
from authentication.models import User

# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=500, null=True)
    message = RichTextField(null=True)
    receiver = ParentalManyToManyField(User, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-date"]