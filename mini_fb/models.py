from django.db import models
from django.urls import reverse

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
     def getcity(self):
         return f'{self.city}'
     def getemail(self):
         return f'{self.email}'
     def getimageurl(self):
         return f'{self.image_url}'
     def get_status_messages(self):
        '''return string representation of profile'''
        status = StatusMessage.objects.filter(profile=self)
        return status
     def get_absolute_url(self):
        return reverse("show_profile",kwargs={'pk':self.pk})
        
     
class StatusMessage(models.Model):
      profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
      timestamp = models.DateTimeField(auto_now=True)
      message = models.TextField(blank=False)
      
      def __str__(self):
         return f'{self.profile} {self.timestamp} {self.message}' 
      
      def get_images(self):
         return self.images.all()
      
      
class Image(models.Model):
    image_file = models.ImageField(upload_to='images/') # an actual image
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(StatusMessage,related_name='images', on_delete=models.CASCADE)
    
    def __str__(self):
      return f'Image for {self.status}'  
   
    
