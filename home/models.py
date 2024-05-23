from django.db import models
from accounts.models import Account


class Post(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='accountuser')
    post_image = models.ImageField(upload_to='posts/')
    text = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text[:30]}'

    def get_count(self):
        return self.lpost.count()


class Vote(models.Model):
    profile = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='lruser')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='lpost')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile} liked {self.post}'


class Follow(models.Model):
    follower = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='follower_user')
    followed = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='followed_user')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
