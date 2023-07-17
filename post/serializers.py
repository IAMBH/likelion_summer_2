from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)
    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data
    
    class Meta:
        model = Post
        fields = '__all__'
        read_only_field = ['id', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    def get_post(self, instance):
        return instance.post.title
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_field = ['id', 'created_at', 'updated_at']
        