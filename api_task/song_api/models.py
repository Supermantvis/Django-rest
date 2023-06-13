from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

'''
Modeliai:
Band

name
Album

name
band_id(FK)
Song

name
duration
album_id(FK)
AlbumReview

user(FK User)
album_id(FK)
content
score (pvz 8/10)
AlbumReviewComment

user(FK User)
album_review_id(FK)
content
AlbumReviewLike

user(FK User)
album_review_id(FK)
'''

mod
