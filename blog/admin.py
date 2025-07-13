from django.contrib import admin
from .models import Blog, Comment, BlogLove

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_published', 'love_count']
    list_filter = ['is_published', 'created_at', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['love_count']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'blog', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'content']

@admin.register(BlogLove)
class BlogLoveAdmin(admin.ModelAdmin):
    list_display = ['blog', 'ip_address', 'created_at']
    list_filter = ['created_at']