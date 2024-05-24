from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view()),
    # post urls
    path('post/', views.ShowPost.as_view()),
    path('create-post/', views.CreatePostView.as_view()),
    path('update-post/<int:post_id>/', views.ChangePostView.as_view()),
    path('delete-post/<int:post_id>/', views.DeletePostView.as_view()),
    # like urls
    path('like-post/<int:post_id>/', views.GetLikeView.as_view()),
    # follow urls
    path('follow-account/<int:account_id>/', views.FollowView.as_view())
]
