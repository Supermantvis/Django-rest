from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


User = get_user_model()


# Band
#     name
class Band(models.Model):
    name = models.CharField(_("name"), max_length=50)

    class Meta:
        verbose_name = _("band")
        verbose_name_plural = _("bands")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("band_detail", kwargs={"pk": self.pk})


# Song
#     name
#     duration
#     song_id(FK) (band)
class Song(models.Model):
    name = models.CharField(_("name"), max_length=50)
    duration = models.PositiveIntegerField(_("duration"))  # in seconds
    band = models.ForeignKey(
        Band,
        verbose_name=_("band"),
        on_delete=models.CASCADE,
        related_name='songs'
        )

    class Meta:
        verbose_name = _("song")
        verbose_name_plural = _("songs")

    def __str__(self):
        return f"{self.name} {self.duration} {self.band}"

    def get_absolute_url(self):
        return reverse("song_detail", kwargs={"pk": self.pk})


# SongReview
#     user(FK User)
#     song_id(FK)
#     content (comment)
#     score (pvz 8/10)
class SongReview(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name='song_reviews'
        )
    song = models.ForeignKey(
        Song,
        verbose_name=_("song"),
        on_delete=models.CASCADE,
        related_name='reviews'
        )
    content = models.TextField(_("content"), max_length=4000)

    SCORE = (
        (1, '1/10'),
        (2, '2/10'),
        (3, '3/10'),
        (4, '4/10'),
        (5, '5/10'),
        (6, '6/10'),
        (7, '7/10'),
        (8, '8/10'),
        (9, '9/10'),
        (10, '10/10')
    )

    score = models.PositiveSmallIntegerField(_("score"), default=5, choices=SCORE)
    
    class Meta:
        verbose_name = _("song review")
        verbose_name_plural = _("song reviews")

    def __str__(self):
        return f"{self.user} {self.song} {self.score}"

    def get_absolute_url(self):
        return reverse("songreview_detail", kwargs={"pk": self.pk})


# SongReviewComment
#     user(FK User)
#     song_review_id(FK)
#     content (comment)
class SongReviewComment(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name='song_review_comments'
        )
    song_review = models.ForeignKey(
        SongReview,
        verbose_name=_("song review"),
        on_delete=models.CASCADE,
        related_name='comments'
        )
    content = models.TextField(_("content"), max_length=4000)

    class Meta:
        verbose_name = _("song review comment")
        verbose_name_plural = _("song review comments")

    def __str__(self):
        return f"{self.user} {self.song_review}"

    def get_absolute_url(self):
        return reverse("songreviewcomment_detail", kwargs={"pk": self.pk})


# SongReviewLike
#     user(FK User)
#     song_review_id(FK)
class SongReviewLike(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name='song_review_likes'
        )
    song_review = models.ForeignKey(
        SongReview,
        verbose_name=_("song review"),
        on_delete=models.CASCADE,
        related_name='likes'
        )

    class Meta:
        verbose_name = _("song review like")
        verbose_name_plural = _("song review likes")

    def __str__(self):
        return f"{self.user} {self.song_review}"

    def get_absolute_url(self):
        return reverse("songreviewlike_detail", kwargs={"pk": self.pk})
