from django.db import models
from django.contrib.auth.models import User

Address_TYPE =(
    ('Home','Home'),
    ('Office','Office'),
    ('Other','Other')
)
class Address(models.Model):
    user = models.ForeignKey(User,related_name='address_address', on_delete = models.CASCADE)
    address = models.TextField(max_length=200)
    type = models.CharField(max_length=12,choices=Address_TYPE)

