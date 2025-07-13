from rest_framework import serializers
from .models import Blog, Comment, BlogLove

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'name', 'email', 'content', 'created_at', 'replies']
        read_only_fields = ['created_at']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

class BlogSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'content', 'excerpt', 'featured_image', 
                 'author_name', 'created_at', 'updated_at', 'love_count', 
                 'comments', 'comments_count']
        read_only_fields = ['created_at', 'updated_at', 'love_count']
    
    def get_comments_count(self, obj):
        return obj.comments.filter(parent=None).count()

class BlogLoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogLove
        fields = ['blog', 'ip_address']