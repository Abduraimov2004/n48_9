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

# Optimized List View for Posts
class PostListView(ListCreateAPIView):
    queryset = Post.objects.select_related('user').all()  # Optimized query
    serializer_class = PostSerializer
    permission_classes = [MyIsAuthenticated]

    # Overriding to ensure query optimization
    def get_queryset(self):
        return Post.objects.select_related('user').all()


# Optimized Detail View for Post
class PostDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related('user').all()  # Optimized query
    serializer_class = PostSerializer
    permission_classes = [IsAnnaPermission, IsOwner]  # Multiple permissions
    lookup_field = 'pk'

    # Overriding to ensure query optimization
    def get_queryset(self):
        return Post.objects.select_related('user').all()
