from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Song, Genre

class SongSerializer(serializers.ModelSerializer):
    genre_name = serializers.SerializerMethodField()
    audio_download_url = serializers.SerializerMethodField()
    video_download_url = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = ['id', 'genre', 'genre_name', 'singer_name', 'song_name', 'lyrics',
                 'url_video', 'image', 'url_audio', 'user', 'create_at', 'update_at',
                 'audio_download_url', 'video_download_url']
        read_only_fields = ['user', 'create_at', 'update_at']

    def get_genre_name(self, obj):
        return obj.genre.name if obj.genre else None

    def get_audio_download_url(self, obj):
        if obj.url_audio:
            request = self.context.get('request')
            return request.build_absolute_uri(f'/api/songs/{obj.id}/download/audio/')
        return None

    def get_video_download_url(self, obj):
        if obj.url_video:
            request = self.context.get('request')
            return request.build_absolute_uri(f'/api/songs/{obj.id}/download/video/')
        return None

    @action(detail=True, methods=['get', 'patch'], url_path='lyrics')
    def lyrics(self, request, pk=None):
        song = get_object_or_404(Song, pk=pk)

        if request.method == 'GET':
            return Response({'lyrics': song.lyrics})

        elif request.method == 'PATCH':
            # Kiểm tra quyền sở hữu (nếu cần)
            # if song.user != request.user:
            #     return Response({'error': 'You do not have permission to update this song'},
            #                     status=status.HTTP_403_FORBIDDEN)

            lyrics = request.data.get('lyrics', '')
            song.lyrics = lyrics
            song.save()

            return Response({
                'message': 'Lyrics updated successfully',
                'lyrics': song.lyrics
            })
        return None

class GenreSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = ['id', 'name', 'songs']
        read_only_fields = ['songs']