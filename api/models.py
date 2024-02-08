from django.db import models
import uuid

# Create your models here.
from django.db import models

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    email_id = models.EmailField(max_length=100, unique=True, blank=False)
    password = models.CharField(max_length=100, blank=False)
    role_type = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateField(null=True, blank=True)

    def set_role_type(__self__, role_type):
        __self__.role_type = role_type
    
    def set_password(__self__, password):
        __self__.password = password
        
class Rent_Items(models.Model):

    car_model = models.CharField(max_length=100, blank=False)
    image = models.CharField(max_length=100, blank=False)
    person_name = models.CharField(max_length=100, blank=False)
    model_name = models.CharField(max_length=100, blank=False)
    color = models.CharField(max_length=50, blank=False)
    number_plate = models.CharField(max_length=50, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rent_status = models.CharField(max_length=50, blank=False, default='AVAILABLE')



