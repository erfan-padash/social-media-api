from django.contrib import admin
from .models import Post, Vote, Follow

admin.site.register(Post)
admin.site.register(Follow)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    raw_id_fields = ('profile', )




