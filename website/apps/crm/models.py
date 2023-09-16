from django.db import models
from phone_field import PhoneField

class BaseClient(models.Model):
    uid = models.CharField(max_length=64, default="0")
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ["created"]

    def __str__(self):
        return self.uid


class Client(BaseClient):
    name = models.CharField(max_length=128)
    client_type = models.CharField(max_length=128)
    def __str__(self):
        return self.name


class ContactDetails(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    

class Email(models.Model):
    client = models.ForeignKey(ContactDetails, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    def __str__(self):
        return self.name


class Phone(models.Model):
    client = models.ForeignKey(ContactDetails, on_delete=models.CASCADE)
    phone = PhoneField(blank=True, help_text='Contact phone number')

    def __str__(self):
        return self.name