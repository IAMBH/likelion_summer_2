from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)
    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data
    
    like = serializers.SerializerMethodField()
    def get_like(self, instance):
        likes = instance.like.all()
        return [like.username for like in likes]
    
    class Meta:
        model = Post
        fields = '__all__'
        read_only_field = ['id', 'created_at', 'updated_at']

class PostListSerializer(serializers.ModelSerializer):
    comments_cnt = serializers.SerializerMethodField()
    def get_comments_cnt(self, instance):
        return instance.comments.count()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'writer', 'content', 'created_at', 'updated_at', 'comments_cnt', 'like_count'] 
        read_only_field = ['id', 'created_at', 'updated_at', 'comments_cnt', 'like_count']

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    def get_post(self, instance):
        return instance.post.title
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_field = ['id', 'created_at', 'updated_at']
        