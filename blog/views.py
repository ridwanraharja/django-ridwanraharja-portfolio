from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Blog, Comment, BlogLove
from .serializers import BlogSerializer, CommentSerializer, BlogLoveSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.filter(is_published=True)
    serializer_class = BlogSerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        """
        Admin endpoints: create, update, delete
        Public endpoints: list, retrieve
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def admin_list(self, request):
        """Endpoint khusus untuk admin - termasuk unpublished blogs"""
        blogs = Blog.objects.all()
        serializer = self.get_serializer(blogs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def love(self, request, slug=None):
        blog = self.get_object()
        ip_address = request.META.get('REMOTE_ADDR')
        
        love, created = BlogLove.objects.get_or_create(
            blog=blog,
            ip_address=ip_address
        )
        
        if created:
            blog.love_count += 1
            blog.save()
            return Response({'message': 'Blog loved!', 'loved': True}, status=status.HTTP_201_CREATED)
        else:
            love.delete()
            blog.love_count -= 1
            blog.save()
            return Response({'message': 'Love removed!', 'loved': False}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def add_comment(self, request, slug=None):
        blog = self.get_object()
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(blog=blog)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        """Admin bisa delete comment siapa saja"""
        if self.action in ['destroy', 'update']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]