# Generated by Django 3.1.4 on 2020-12-24 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LandingPage', '0006_projects_is_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='coverimg',
            field=models.ImageField(blank=True, null=True, upload_to='<django.db.models.fields.CharField>/'),
        ),
    ]