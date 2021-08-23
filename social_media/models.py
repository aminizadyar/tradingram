from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from paper_trade.models import OrderOpenPosition
from api.models import Symbol

User._meta.get_field('email')._unique = True

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(null=True,blank=True,upload_to='profile_pictures/')
    free_margin = models.FloatField(default=100000)
# test
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Post(models.Model):
    related_symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE,primary_key=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,primary_key=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    text_content = models.TextField(null=True,blank=False)
    likes = models.ManyToManyField(User,related_name='likes_relation')
    symbol_initial_bid_price = models.FloatField(null=True,blank=True)
    symbol_initial_ask_price = models.FloatField(null=True,blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def related_users(self):
        return self.likes.all()

    def __str__(self):
        return self.user.username + "--" +self.related_symbol.symbol + "Post"

