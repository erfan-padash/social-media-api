from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializer
from accounts.permissions import UserCanWriteOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .models import Post, Vote, Follow
from accounts.models import Account


class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        instance = Post.objects.all()
        ser_ins = PostSerializer(instance=instance, many=True)
        return Response(ser_ins.data)


class ShowPost(APIView):
    """
    the authenticated users just can watch the post
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = get_object_or_404(Account, pk=request.account_id)
        posts = account.all_post()
        ser_ins = PostSerializer(instance=posts, many=True)
        return Response(ser_ins.data)


class CreatePostView(APIView):

    permission_classes = [IsAuthenticated, UserCanWriteOrReadOnly]

    def post(self, request):
        account = get_object_or_404(Account, id=request.account_id)
        self.check_object_permissions(request, account)
        ser_data = PostSerializer(data=request.data)
        if ser_data.is_valid():
            cd = ser_data.validated_data
            Post.objects.create(
                account=account,
                post_image=cd['post_image'],
                text=cd['text'],
            )
            return Response(ser_data.data)
        return Response(ser_data.errors)


class ChangePostView(APIView):
    """
    change their post value with put method
    """

    permission_classes = [IsAuthenticated, UserCanWriteOrReadOnly]

    def put(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        self.check_object_permissions(request, post)
        ser_data = PostSerializer(instance=post, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data)
        return Response(ser_data.errors)


class DeletePostView(APIView):

    permission_classes = [IsAuthenticated, UserCanWriteOrReadOnly]

    def delete(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        self.check_object_permissions(request, post)
        post.delete()
        return Response('you delete your post successfully')


class GetLikeView(APIView):
    """
    Authenticated user can like posts
    """

    permission_classes = [IsAuthenticated, UserCanWriteOrReadOnly]

    def post(self, request, post_id):
        account = get_object_or_404(Account, id=request.account_id)
        self.check_object_permissions(request, account)
        post = get_object_or_404(Post, pk=post_id)
        vote = Vote.objects.filter(post=post, profile=account)
        if vote.exists():
            return Response({
                'vote': 'you liked this post before cant like again'
            })
        Vote.objects.create(
            profile=account,
            post=post,
        )
        return Response({
            'like': 'you liked this post with {} account'.format(account.account_name)
        })


class DeleteLike(APIView):

    permission_classes = [IsAuthenticated, UserCanWriteOrReadOnly]

    def delete(self, request, post_id):
        account = get_object_or_404(Account, id=request.account_id)
        self.check_object_permissions(request, account)
        post = get_object_or_404(Post, id=post_id)
        vote = Vote.objects.filter(account=account, post=post)
        if vote.exists():
            vote.delete()
            return Response({
                'success': 'you take back your like'
            })
        return Response({
            'error': 'you dont like this post before. you cant take back your like'
        })


class FollowView(APIView):
    permission_classes = [IsAuthenticated, UserCanWriteOrReadOnly]

    def post(self, request, account_id):
        follower = get_object_or_404(Account, id=request.account_id)
        self.check_object_permissions(request, follower)
        followed = get_object_or_404(Account, id=account_id)
        follow_check = Follow.objects.filter(follower=follower, followed=followed)
        if follower == followed or follow_check.exists():
            return Response({
                'error': 'you follow this page before cant do it again'
            })
        Follow.objects.create(
            follower=follower,
            followed=followed
        )
        return Response({
            'success': f'you follow {followed.account_name} account successfully'
        })
