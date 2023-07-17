from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# GenericViewSet
# class PostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
#                   mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# ModelViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostCommentViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
        
    def list(self, request, post_id=None):
        post = get_object_or_404(Post, id = post_id)
        queryset = self.filter_queryset(self.get_queryset().filter(post=post)) # 위에서 정의한 queryset을 filtering (Post 중에서 id=post_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data)

class CommentViewSet(viewsets.GenericViewSet, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer