from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import models, serializers


class SongList(generics.ListAPIView):
    queryset = models.Song.objects.all()
    serializer_class = serializers.SongSerializer


class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Song.objects.all()
    serializer_class = serializers.SongSerializer
    permission_classes = [
        permissions.IsAdminUser
    ]


class SongReviewList(generics.ListCreateAPIView):
    queryset = models.SongReview.objects.all()
    serializer_class = serializers.SongReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SongReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SongReview.objects.all()
    serializer_class = serializers.SongReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, *args, **kwargs):
        review = models.SongReview.objects.filter(
            pk=kwargs['pk'],
            user=self.request.user
        )
        if review.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_('You have no rights to update this.'))
        
    def delete(self, request, *args, **kwargs):
        review = models.SongReview.objects.filter(
            pk=kwargs['pk'],
            user=self.request.user
        )
        if review.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_('You have no rights to delete this.'))
        

class SongReviewCommentList(generics.ListCreateAPIView):
    # queryset = models.SongReviewComment.objects.all()
    serializer_class = serializers.SongReviewCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        review = models.SongReview.objects.get(pk=self.kwargs['review_pk'])
        serializer.save(user=self.request.user, song_review=review)

    def get_queryset(self):
        review = models.SongReview.objects.get(pk=self.kwargs['review_pk'])
        return models.SongReviewComment.objects.filter(song_review=review)
    

class SongReviewCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SongReviewComment.objects.all()
    serializer_class = serializers.SongReviewCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def put(self, request, *args, **kwargs):
        try:
            review = models.SongReview.objects.get(pk=kwargs['pk'], user=request.user)
        except Exception as e:
            raise ValidationError(_('You cannot update this.'))
        else:
            return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            review = models.SongReview.objects.get(pk=kwargs['pk'], user=request.user)
        except Exception as e:
            raise ValidationError(_('You cannot delete this.'))
        else:
            return self.destroy(request, *args, **kwargs)


class SongReviewLikeCreateDestroy(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.SongReviewLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        review = models.SongReview.objects.get(pk=self.kwargs['pk'])
        return models.SongReviewLike.objects.filter(user=self.request.user, song_review=review)
    
    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError(_('You have already liked this'))
        review = models.SongReview.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, song_review=review)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError(_('You cannot unlike, what you don\'t like'))