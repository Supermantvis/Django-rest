from rest_framework import serializers
from . import models


class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Song
        fields = ['id', 'name', 'duration', 'picture', 'band']


# class BandSerializer():
        
#     class Meta:
#         model = models.Band
#         fields = ['name']


class SongReviewCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    song_review = serializers.ReadOnlyField(source='song_review.id')

    class Meta:
        model = models.SongReviewComment
        fields = ['id', 'user', 'user_id', 'song_review', 'content']


class SongReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    comments = SongReviewCommentSerializer(many=True, read_only=True)
    # comments = serializers.StringRelatedField(many=True, read_only=True)  # STR return, better not use
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return models.SongReviewComment.objects.filter(song_review=obj).count()

    def get_likes_count(self, obj):
        return models.SongReviewLike.objects.filter(song_review=obj).count()

    class Meta:
        model = models.SongReview
        fields = ['id', 'user', 'user_id', 'song', 'content', 'score', 'comments', 'comments_count', 'likes_count']


class SongReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SongReviewLike
        fields = ['id']
    