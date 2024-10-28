from django.db import models
from django.urls import reverse
from django.db.models import Q

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

     def get_friends(self):
        friends = []
        for friend in Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self)):
            if friend.profile1 == self:
                friends.append(friend.profile2)
            else:
                friends.append(friend.profile1)
        return friends
     def add_friend(self,other):
         if self == other:
             raise ValueError("cannot add self as a friend.")
         if not Friend.objects.filter(Q(profile1=self,profile2=other) | Q(profile1=other,profile2=self)).exists():
             Friend.objects.create(profile1=self,profile2=other)
     def get_friend_suggestions(self):
         c_friends = [friend.pk for friend in self.get_friends()]
         c_friends.append(self.pk)
         s_friends = Profile.objects.exclude(pk__in=c_friends)
         return s_friends
     def get_news_feed(self):
         #own_messages = StatusMessage.objects.filter(profile=self)
         friends = self.get_friends()
         friends_messages = StatusMessage.objects.filter(profile__in=friends)

         #all_messages = (own_messages | friends_messages).order_by('-timestamp')

         return friends_messages
     
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
   
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="profile1")
    profile2 = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)

    def  __str__(self):
        return f"{self.profile1} & {self.profile2}"
