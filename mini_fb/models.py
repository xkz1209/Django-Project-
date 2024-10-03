from django.db import models

# Create your models here.
class Profile(models.Model):
     firstName = models.TextField(blank=False)
     lastName = models.TextField(blank=False)
     city = models.TextField(blank=False)
     email = models.TextField(blank=False)
     image_url = models.URLField(blank=True)
     
     def __str__(self):
        '''Return a string representation of this profile object.'''
        return f'{self.firstName} {self.lastName}'