# Generated by Django 3.1.4 on 2021-01-03 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactdetails',
            name='is_responded',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
