from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Extended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/favicon.jpg')

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_extended(sender, instance, created, **kwargs):
        if created:
            Extended.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_extended(sender, instance, **kwargs):
        instance.extended.save()


class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    title = models.CharField(max_length=200)
    prev_text = models.TextField(default='')
    text = models.TextField()
    views = models.IntegerField(default=0)
    image = models.ImageField(blank=True, null=True, default=None, upload_to='media/', height_field=None,
                              width_field=None, max_length=100)
    date = models.DateField(auto_now_add=True)
    hidden = models.BooleanField(default=False)


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, default=0, related_name='comments')

    def __str__(self):
        return f'{self.user_id} {self.date}'
