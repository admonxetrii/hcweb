# Generated by Django 3.1.4 on 2020-12-25 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LandingPage', '0008_auto_20201224_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='Projects/Cover/'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='date_of_complete',
            field=models.DateField(blank=True, default='', null=True),
        ),
    ]