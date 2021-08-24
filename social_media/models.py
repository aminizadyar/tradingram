from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from paper_trade.models import OrderOpenPosition
from api.models import Symbol
from paper_trade.models import OrderOpenPosition

User._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='profile_pictures/', default='profile_pictures/default.png')
    free_margin = models.FloatField(default=100000)
    is_post_public = models.BooleanField(default=True,
                                         help_text="* What does this mean?  If it is active, all users, even those who havn't followed you will see your post. If not, only your followers will see them")
    is_signal_public = models.BooleanField(default=False,
                                           help_text="* What does this mean?  If it is active, all users, even those who havn't followed you will see your signals. If not, only your followers will see them")

    def followers(self):
        return UserFollow.objects.filter(followed_user=self.user)

    def number_of_followers(self):
        return UserFollow.objects.filter(followed_user=self.user).count()

    def followings(self):
        return UserFollow.objects.filter(following_user=self.user)

    def number_of_followings(self):
        return UserFollow.objects.filter(following_user=self.user).count()

    def all_open_positions(self):
        return OrderOpenPosition.objects.filter(user=self.user, result='S', current_quantity__gt=0)

    def blocked_margins(self):
        sum_of_blocked_margins = 0
        open_positions = self.all_open_positions()
        for open_position in open_positions:
            sum_of_blocked_margins += open_position.blocked_margin
        return sum_of_blocked_margins

    def unrealized_gains(self):
        sum_of_unrealized_gains = 0
        open_positions = self.all_open_positions()
        for open_position in open_positions:
            sum_of_unrealized_gains += open_position.unrealized_gain
        return sum_of_unrealized_gains

    def equity(self):
        return self.free_margin + self.blocked_margins() + self.unrealized_gains()

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
    related_symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, primary_key=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    text_content = models.TextField(null=True, blank=False)
    likes = models.ManyToManyField(User, related_name='likes_relation')
    symbol_initial_bid_price = models.FloatField(null=True, blank=True)
    symbol_initial_ask_price = models.FloatField(null=True, blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def like_related_users(self):
        return self.likes.all()

    def __str__(self):
        return self.user.username + " Post"


class UserFollow(models.Model):
    followed_user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['followed_user', 'following_user'], name="unique_followers")
        ]

        ordering = ['-created_datetime']

    def __str__(self):
        return self.following_user.username + " followed " + self.followed_user.username
