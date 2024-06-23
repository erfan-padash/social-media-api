from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('post_image', 'text', 'comments')

    def get_comments(self, obj):
        if not isinstance(obj, dict):
            result = obj.com_post.all()
            com = CommentSerializer(instance=result, many=True).data
            return com


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

