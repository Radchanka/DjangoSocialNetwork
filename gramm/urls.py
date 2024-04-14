from django.urls import path

from .views import home_page, register, profile, login_view, edit_profile, create_post, delete_post, like_post, \
    tag_posts, activation_info, manage_subscription, logout_view

app_name = 'gramm'

urlpatterns = [
    path('', home_page, name='home_page'),
    path('register/', register, name='register'),
    path('activation_info/', activation_info, name='activation_info'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout_view'),
    path('profile/<int:user_id>/', profile, name='profile'),
    path('profile/<int:user_id>/edit/', edit_profile, name='edit_profile'),
    path('post/', create_post, name='create_post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('like_post/<int:post_id>/', like_post, name='like_post'),
    path('tag/<str:tag_name>/', tag_posts, name='tag_posts'),
    path('users/<int:user_id>/<str:action>/', manage_subscription, name='manage_subscription'),
]
