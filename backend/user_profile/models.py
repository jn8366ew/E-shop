from .countries import Countries
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255, default='')
    address_line_2 = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    state_province_region = models.CharField(max_length=255, default='')
    postal_zip_code = models.CharField(max_length=20, default='')
    telephone_number = models.CharField(max_length=255, default='')
    country_region = models.CharField(
        max_length=255, choices=Countries.choices, default=Countries.Republic_of_Korea)


    def __str__(self):
        return self.user.first_name
