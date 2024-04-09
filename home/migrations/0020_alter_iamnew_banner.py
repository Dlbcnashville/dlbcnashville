# Generated by Django 5.0.3 on 2024-04-08 08:46

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_alter_iamnew_caption_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iamnew',
            name='banner',
            field=cloudinary.models.CloudinaryField(blank=True, help_text='Select a background image banner', max_length=255, null=True, verbose_name='image'),
        ),
    ]
