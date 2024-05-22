from django.contrib import admin
from .models import Post, Vote

admin.site.register(Post)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    raw_id_fields = ('profile', )


