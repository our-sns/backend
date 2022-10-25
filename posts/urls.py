from django.urls import path
from .views import PostList, PostDetail, ImageList, ImageDetail, LikeList, PostSearchList

urlpatterns = [
    path("", PostList.as_view(), name="post_list"),
    path("<int:pk>", PostDetail.as_view(), name="post_detail"),
    path("image/", ImageList.as_view(), name="image_list"),
    path("image/<int:pk>/", ImageDetail.as_view(), name="image_detail"),
    path("like/", LikeList.as_view(), name="like_list"),
    path('search/', PostSearchList.as_view(), name="post_search"),

]