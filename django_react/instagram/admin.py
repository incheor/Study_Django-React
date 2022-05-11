from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class postAdmin(admin.ModelAdmin) :
    list_display = ['id', 'photo_tag', 'message', 'message_length','is_public', 'created_at', 'updated_at']
    list_display_links = ['message']
    list_filter = ['created_at', 'is_public']
    search_fields = ['message']
    
@admin.register(Comment)
class commentAdmin(admin.ModelAdmin) :
    pass