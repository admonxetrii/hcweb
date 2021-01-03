from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# custom validator
def mycustomvalidator(value):
    if len(value) > 1:
        return True
    else:
        raise ValidationError("Must have more than 1 characters.")


def val2(value):
    if '@' in value or '#' in value or '*' in value:
        raise ValidationError("Title cannot have special charaters.")
    else:
        return True


# models
class ServicesDetail(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True, validators=[mycustomvalidator, val2])
    image = models.ImageField(upload_to='ServicesDetails/', null=True, blank=True)
    descriptions = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = ServicesDetail.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(ServicesDetail, self).save(*args, **kwargs)


class HomeSlider(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True, validators=[mycustomvalidator, val2])
    subtitle = models.CharField(max_length=70, null=True, blank=True)
    image = models.ImageField(upload_to='HomeSlider/', null=True, blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = HomeSlider.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(HomeSlider, self).save(*args, **kwargs)


class Projects(models.Model):
    client = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    nature_of_work = models.TextField(null=True, blank=True)
    contract_number = models.CharField(max_length=100, null=True, blank=True)
    value_of_work = models.FloatField(null=True, blank=True)
    contract_period = models.IntegerField(null=True, blank=True)
    date_of_start = models.DateField(null=True, blank=True)
    date_of_complete = models.DateField(null=True, default='', blank=True)
    percentage_of_complete = models.IntegerField(null=True, blank=True)
    value_of_completed_work = models.FloatField(null=True, blank=True)
    balance_value = models.FloatField(null=True, blank=True)
    is_completed = models.BooleanField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='Projects/Cover/', null=True, blank=True)

    def __str__(self):
        return self.client

    def delete(self, *args, **kwargs):
        self.cover_image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Projects.objects.get(id=self.id)
            if this.coverimg != self.cover_image:
                this.coverimg.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(Projects, self).save(*args, **kwargs)


class ProjectsPictures(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Projects/Pictures/', null=True, blank=True)

    def __str__(self):
        return self.project.client

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = ProjectsPictures.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(ProjectsPictures, self).save(*args, **kwargs)


class StaffCategory(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

class StaffSubCategory(models.Model):
    category = models.ForeignKey(StaffCategory, on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=50)

    def __str__(self):
        return self.subcategory


class TeamMembers(models.Model):
    category = models.ForeignKey(StaffCategory, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(StaffSubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    experience = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='Team/Images/', null=True, blank=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = TeamMembers.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(TeamMembers, self).save(*args, **kwargs)
