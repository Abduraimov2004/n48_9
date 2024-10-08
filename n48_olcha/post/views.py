from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser
)

from .models import Post
from .serializers import PostSerializer
from .permissions import MyIsAuthenticated, IsOwner, IsAnnaPermission

class PostListView(ListCreateAPIView):
    queryset = Post.objects.select_related('user').all()
    serializer_class = PostSerializer
    permission_classes = [MyIsAuthenticated]

    def get_queryset(self):
        return Post.objects.select_related('user').all()


class PostDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related('user').all()
    serializer_class = PostSerializer
    permission_classes = [IsAnnaPermission, IsOwner]
    lookup_field = 'pk'

    def get_queryset(self):
        return Post.objects.select_related('user').all()
