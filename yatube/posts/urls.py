from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_post, name='new_post'),
    path('group/<slug:slug>/', views.group_posts, name='group'),
    path('follow/', views.follow_index, name='follow_index'),
    path('user/<str:username>/', views.profile, name='profile'),
    path('user/<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('user/<str:username>/<int:post_id>/edit/',
         views.post_edit,
         name='post_edit'),
    path('user/<str:username>/<int:post_id>/delete/',
         views.post_delete,
         name='post_delete'),
    path('user/<str:username>/<int:comment_id>/comment/edit/',
         views.comment_edit,
         name='comment_edit'),
    path('user/<str:username>/<int:comment_id>/comment/delete/',
         views.comment_delete,
         name='comment_delete'),
    path('user/<str:username>/<int:post_id>/comment/',
         views.add_comment,
         name='add_comment'),
    path('user/<str:username>/follow/', views.profile_follow,
         name='profile_follow'),
    path('user/<str:username>/unfollow/', views.profile_unfollow,
         name='profile_unfollow'),
]
