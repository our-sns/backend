from django.urls import path
from comments.views import CommentList, CommentDetail, CommentLikeList

urlpatterns = [
    path("", CommentList.as_view(), name="comment_list"),
    path("<int:pk>", CommentDetail.as_view(), name="comment_detail"),
    path("like/", CommentLikeList.as_view(), name="comment_like_list"),
]
