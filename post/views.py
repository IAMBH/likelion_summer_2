from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404

from .models import Post, Comment, PostReaction
from .serializers import PostSerializer, CommentSerializer, PostListSerializer
# from .permissions import IsOwnerOrReadOnly

# GenericViewSet
# class PostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
#                   mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# ModelViewSet

class PostViewSet(viewsets.ModelViewSet):
    # queryset = Post.objects.all()
    queryset = Post.objects.annotate(
        like_cnt = Count(
            "reactions", filter=Q(reactions__reaction="like"), distinct=True
        ),
        dislike_cnt = Count(
            "reactions", filter=Q(reactions__reaction='dislike'), distinct=True
        ),
    )
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content']
    # serializer_class = PostSerializer
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer
    
    @action(methods=["GET"], detail=False)
    def like_top3(self, request, pk=None):
        # 좋아요 기능
        best3_post = self.get_queryset().order_by('-like_count')[:3]
        best3_post_serializer = PostSerializer(best3_post, many=True)
        return Response(best3_post_serializer.data)
    
    @action(methods=['POST'], detail=True)
    def likes(self, request, pk=None):
        post = self.get_object()    # 현재 url의 post
        reaction = PostReaction.objects.filter(post=post, user=request.user, reaction='like')
        # 이미 좋아요를 누른 user이면
        if reaction.exists():    # reaction
            reaction.delete()
        # 좋아요를 누르지 않았다면 
        else:
            PostReaction.objects.create(post=post, user=request.user, reaction='like')

        return Response()
    
    @action(methods=['POST'], detail=True)
    def dislikes(self, request, pk=None):
        post = self.get_object()    # 현재 url의 post
        reaction = PostReaction.objects.filter(post=post, user=request.user, reaction='dislike') 
        # 이미 좋아요를 누른 user이면
        if reaction.exists:
            reaction.delete()
        # 좋아요를 누르지 않았다면 
        else:
            PostReaction.objects.create(post=post, user=request.user, reaction='dislike')

        return Response()
    
    
    @action(methods=['GET'], detail=False)
    def top5(self, request):
        queryset = self.get_queryset().order_by('-like_cnt')[:5]
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

        
    # @action(methods=["POST"], detail=True)
    # def like(self, request, pk=None):
    #     like_post = self.get_object()
    #     if request.user in like_post.like.all():
    #             print(like_post.like_count, "if")
    #             like_post.like_count -= 1
    #             like_post.like.remove(request.user)
    #     else:
    #         print(like_post.like_count)
    #         like_post.like_count += 1
    #         like_post.like.add(request.user)

    #     like_post.save(update_fields=["like_count"])

    #     return Response()


class PostCommentViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = self.kwargs.get("post_id")
        queryset = Comment.objects.filter(post_id=post)
        return queryset

        
    # def list(self, request, post_id=None):
    #     post = get_object_or_404(Post, id = post_id)
    #     queryset = self.filter_queryset(self.get_queryset().filter(post=post)) # 위에서 정의한 queryset을 filtering (Post 중에서 id=post_id)
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    
    def create(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data)

class CommentViewSet(viewsets.GenericViewSet, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # def get_permissions(self):
    #     if self.action in ['updated','destroy','partial_update']:
    #         return [IsOwnerOrReadOnly()]
    #     return []
    
    # def get_object(self):
    #     obj = super().get_object()
    #     return obj
