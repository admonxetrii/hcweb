# Generated by Django 3.1.4 on 2021-01-04 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LandingPage', '0012_auto_20210104_0149'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageExtra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numberofprj', models.IntegerField()),
                ('numberofemp', models.IntegerField()),
                ('numberofconst', models.IntegerField()),
                ('numberofpart', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='Team/Images/')),
            ],
        ),
    ]
