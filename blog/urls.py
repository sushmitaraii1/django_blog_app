from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap
from .views import (PostListView, PostDetailView,
                    PostCreateView , PostUpdateView,
                    PostDeleteView, CategoryCreateView,
                    TagCreateView)

sitemaps = {
    'posts':PostSitemap
}


urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps}, name='sitemap'),
    # urls for post CRUD
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/<str:post_slug>/', PostDetailView.as_view(), name='post_detail'),
    path('post/add/', PostCreateView.as_view(), name='post-create'),
    path('category/add/', CategoryCreateView.as_view(), name='category-create'),
    path('tag/add/', TagCreateView.as_view(), name='tag-create'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('feedback/', views.feedback, name='feedback'),
    path('category/<str:category_slug>/', views.post_by_category, name='post_by_category'),
    path('tag/<str:tag_slug>/', views.post_by_tag, name='post_by_tag'),

    # path('blogs/', views.test_redirect, name='test_redirect'),

    path('cookie/', views.test_cookie, name='cookie'),
    path('track_user/', views.track_user, name='track_user'),
    path('stop-tracking/', views.stop_tracking, name='stop_tracking'),
    path('test-delete/', views.test_delete, name='test_delete'),
    path('test-session/', views.test_session, name='test_session'),
    path('save-session-data/', views.save_session_data, name='save_session_data'),
    path('access-session-data/', views.access_session_data, name='access_session_data'),
    path('delete-session-data/', views.delete_session_data, name='delete_session_data'),
    path('lousy-login/', views.lousy_login, name='lousy_login'),
    path('lousy-secret/', views.lousy_secret, name='lousy_secret'),
    path('lousy-logout/', views.lousy_logout, name='lousy_logout'),
    # path('login/', views.login, name='blog_login'),
    # path('logout/', views.logout, name='blog_logout'),
    path('admin_page/', views.admin_page, name='admin_page'),

]