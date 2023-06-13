from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.SongList.as_view()),
    path("song-reviews/", views.SongReviewList.as_view()),
    path("<int:pk>/", views.SongReviewDetail.as_view()),
]
