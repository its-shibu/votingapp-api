from rest_framework import serializers
from . models import Post, Vote, FormData

class PostSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source = 'poster.id')
    poster_id = serializers.ReadOnlyField(source = 'poster.id')
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'url', 'poster', 'poster_id', 'created_at', 'votes']
    
    def get_votes(self, post):
        return Vote.objects.filter(post = post).count()

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']
        
class FormDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormData
        fields = ['id', 'name', 'email', 'phone', 'address', 'message', 'created_at']