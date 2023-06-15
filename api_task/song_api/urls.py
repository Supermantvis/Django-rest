from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.SongList.as_view()),
    path("song-reviews/", views.SongReviewList.as_view()),
    path('song-detail/<int:pk>/', views.SongDetail.as_view()),
    path("song-review/<int:pk>/", views.SongReviewDetail.as_view()),
    path('song-review/<int:review_pk>/comments/', views.SongReviewCommentList.as_view()),
    path('comment/<int:pk>', views.SongReviewCommentDetail.as_view()),
    path("review/<int:pk>/like/", views.SongReviewLikeCreateDestroy.as_view()),
]
