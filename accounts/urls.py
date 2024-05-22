from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # user create url
    path('create-user/', views.CreateUserView.as_view()),
    # login url
    path('user-login/', views.UserLogin.as_view()),
    # account urls
    path('', views.AccountsView.as_view()),
    path('create-account/', views.CreateAccountView.as_view()),
    path('change-account/', views.ChangeAccountView.as_view()),
    path('delete-account/<int:profile_id>/', views.DeleteAccountView.as_view()),
]
