from django.db import models

class Settings(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='settings')
    subtitle = models.TextField(max_length=500)
    call_us = models.CharField(max_length=25)
    email_us = models.CharField(max_length=50)
    emails = models.TextField(max_length=50)
    phones = models.TextField(max_length=50)
    address = models.TextField(max_length=100)
    android_app = models.URLField(null = True,blank = True)
    ios_app = models.URLField(null = True,blank = True)
    facebook = models.URLField(null = True,blank = True)
    youtube = models.URLField(null = True,blank = True)
    
    def __str__(self):
        return self.name