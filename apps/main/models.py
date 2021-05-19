from django.db import models
from django.core.validators import validate_email
import re
# Create your models here.
class RegiManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name']="First name needs at least 2 characters"
        if len(post_data['last_name']) < 2:
            errors['last_name']="Last name needs at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")
        if len(post_data['password']) < 8:
            errors['password']="Password needs to be at least 8 characters"
        if post_data['pw_confirm'] != post_data['password']:
            errors['pw_confirm']="Invalid password"

        return errors
        
class Register(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RegiManager()

class CityManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['city']) < 1:
            errors['city'] = "Provide a city"

        return errors

class City(models.Model):
    cityName = models.CharField(max_length=255)

    objects = CityManager()

    def save(self, *args, **kwargs):
        self.cityName = self.cityName.title()
        return super(City, self).save(*args, **kwargs)

    def __repr__(self):
        return f"{self.city}"

class EventManager(models.Manager):
    def event_validator(self, post_data):
        errors = {}
        if len(post_data['event_title']) < 1:
            errors['event_title']="Please enter a title"
        if len(post_data['event_description']) < 24:
            errors['event_description']="Description must be at least 25 characters"
        
        return errors

class Event(models.Model):
    event_title = models.CharField(max_length=255)
    event_description = models.TextField()
    event_user = models.ForeignKey(Register, on_delete=models.CASCADE)
    event_user_firstName = models.CharField(max_length=255, default=None, null=True, blank=True)
    event_user_lastName = models.CharField(max_length=255, default=None, null=True, blank=True)
    event_city = models.ForeignKey(City, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EventManager()

    def save(self, *args, **kwargs):
        self.event_title = self.event_title.capitalize()
        return super(Event, self).save(*args, **kwargs)

class Attendance(models.Model):
    user_name = models.CharField(max_length=255, default=None)
    name_users = models.ForeignKey(Register, on_delete=models.CASCADE)
    name_city = models.ForeignKey(City, on_delete=models.CASCADE)
    name_event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)
    join_event = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

