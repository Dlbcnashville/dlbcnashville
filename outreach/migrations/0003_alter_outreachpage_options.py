# Generated by Django 5.0.3 on 2024-04-20 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outreach', '0002_outreachpage_date_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='outreachpage',
            options={'ordering': ['-date_created']},
        ),
    ]
