from django.contrib import admin
from .models import Post, Vote, Follow, Comment

admin.site.register(Post)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    raw_id_fields = ('profile', )


@admin.register(Follow)
class FollowView(admin.ModelAdmin):
    raw_id_fields = ('follower', 'followed')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', ]
