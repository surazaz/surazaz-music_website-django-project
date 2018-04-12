from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Album(models.Model):
	artist = models.CharField(max_length=250)
	album_title  = models.CharField(max_length=500)
	genre = models.CharField(max_length=100)
	album_logo = models.FileField(max_length=1000)

	def get_absolute_url(self):
		return reverse('music:detail',kwargs={'pk':self.pk})
	def __str__(self):
		return self.album_title+"-"+self.artist


class Song(models.Model):
	album = models.ForeignKey(Album,on_delete=models.CASCADE)
	#part of album and on_delete cascade means whever we delete album song is itself deleted
	file_type = models.CharField(max_length=10)
	song_title = models.CharField(max_length=250)
	is_fav=models.BooleanField(default=False)
	def __str__(self):
		return self.song_title
class UserProfile(models.Model):
	user=models.OneToOneField(User)
	description=models.CharField(max_length=200,default='')
	city=models.CharField(max_length=50,default='')
	phone=models.IntegerField(default='0')
	
def create_profile(sender,**kwargs):
	if kwargs['created']:
		user_profile=UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)	