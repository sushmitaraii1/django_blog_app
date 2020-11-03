from django.urls import path, include
from . import views as user_views
from django.contrib.auth import views as auth_views
from .views import UserPostListView


urlpatterns = [
    #cadmin
    path('post/add/',user_views.post_add, name='post_add'),
    # path('post/update/<int:pk>/', user_views.post_update, name='post_update'),
    path('activate/account/', user_views.activate_account, name='activate'),
    path('dashboard/',user_views.profile,name='dashboard'),
    path('post/userpost/', UserPostListView.as_view(), name = 'user-post'),

    path('login/', auth_views.LoginView.as_view(template_name='cadmin/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='cadmin/logout.html'), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='cadmin/password_reset.html'),
         name='password_reset'),
    path('password-reset-done/',
         auth_views.PasswordResetDoneView.as_view(template_name='cadmin/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='cadmin/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='cadmin/password_reset_complete.html'),
         name='password_reset_complete'),
    path('register/',user_views.register,name='register'),
    path('profile/',user_views.profile,name='profile'),
    # path('', views.home, name='home'),
]


