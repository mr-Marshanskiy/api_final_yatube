from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from .models import Follow, Post, Group
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    FollowSerializer,
    PostSerializer,
    CommentSerializer,
    GroupSerializer,
)
from .filters import FollowFilter, PostFilter


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
    )
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
    )

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, id=self.kwargs.get('post_id'))
        )


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FollowFilter

    def get_queryset(self):
        return Follow.objects.filter(following=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
    )
