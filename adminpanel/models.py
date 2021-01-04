from django.db import models


# Create your models here.
class ContactDetails(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(null=True, unique=True)
    phone = models.CharField(max_length=20, null=True)
    subject = models.CharField(max_length=500, null=True)
    message = models.TextField(max_length=1000, null=True)
    respmessage = models.TextField(max_length=1000, null=True)
    is_responded = models.BooleanField(null=True)

    def __str__(self):
        return "Contact" + self.email


class QuotationRequest(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(null=True, unique=True)
    phone = models.CharField(max_length=12, null=True)
    about_company = models.TextField(max_length=1000, null=True)
    about_project = models.TextField(max_length=1000, null=True)
    respmessage = models.TextField(max_length=1000, null=True)
    is_responded = models.BooleanField(null=True)

    def __str__(self):
        return "Quotation" + self.email

