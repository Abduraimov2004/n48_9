from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser
)

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer
from .permissions import MyIsAuthenticated, IsOwner, IsAnnaPermission


@method_decorator(cache_page(60 * 2), name='dispatch')
class PostListView(ListCreateAPIView):
    queryset = Post.objects.select_related('user').all()
    serializer_class = PostSerializer
    permission_classes = [MyIsAuthenticated]

    def get_queryset(self):
        cache_key = 'post-list'
        cached_data = cache.get(cache_key)
        if not cached_data:
            queryset = Post.objects.all().select_related('user')
            queryset = queryset.prefetch_related('user__groups', 'user__user_permissions')
            cache.set(cache_key, queryset, timeout=60 * 2)
            return queryset
        return cached_data


@method_decorator(cache_page(60 * 2), name='dispatch')
class PostDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related('user').all()
    serializer_class = PostSerializer
    permission_classes = [IsAnnaPermission, IsOwner]
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        cache_key = f'post-detail-{kwargs["pk"]}'
        cached_data = cache.get(cache_key)
        if not cached_data:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            cache.set(cache_key, serializer.data, timeout=60 * 2)
            return Response(serializer.data)
        return Response(cached_data)
