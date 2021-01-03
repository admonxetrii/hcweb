# Generated by Django 3.1.4 on 2021-01-03 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LandingPage', '0010_auto_20201228_0111'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StaffSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LandingPage.staffcategory')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('qualification', models.CharField(max_length=100)),
                ('experience', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='Team/Images/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LandingPage.staffcategory')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LandingPage.staffsubcategory')),
            ],
        ),
    ]