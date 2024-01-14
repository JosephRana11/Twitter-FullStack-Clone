
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following" , views.following_posts_view , name ="following"),


    path("user/<str:request_user_name>" , views.user_profile_view , name = "user"),



    path("api/posts" , views.get_posts_api_view),
    path("api/likes" , views.get_likes_api_view),
    path("api/following" , views.get_following_posts_api_view),
    path("api/posts/<str:request_user_name>" , views.get_user_post),
    path("api/user/relation/<str:request_user_name>" , views.get_user_relation_view),
    path("api/user/follow" , views.update_user_relation_api_view)
]
