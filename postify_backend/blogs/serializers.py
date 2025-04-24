from rest_framework import serializers
from .models import BlogPost, Comment, BlogLike, BlogRead
from django.contrib.auth import get_user_model

User = get_user_model()

class UserBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_pic']

class BlogLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogLike
        fields = ['id', 'user', 'blog', 'liked_at']
        read_only_fields = ['id', 'liked_at']

class BlogReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogRead
        fields = ['id', 'user', 'blog', 'read_at']
        read_only_fields = ['id', 'read_at']

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = UserBlogSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'replies', 'parent_comment', 'blog']
        read_only_fields = ['id','blog']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            replies = obj.replies.filter(is_active=True)
            return CommentSerializer(replies, many=True, context=self.context).data
        return []
    
class BlogPostSerializer(serializers.ModelSerializer):
    author = UserBlogSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(read_only=True)
    read_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'content', 'image_1', 'image_2', 'image_3', 'created_at', 'updated_at', 'is_active', 'like_count', 'read_count', 'comments', 'is_liked', 'is_read']

    def get_comments(self, obj):
        active_comments = obj.comments.filter(is_active=True, parent_comment__isnull=True)
        return CommentSerializer(active_comments, many=True, context=self.context).data

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return BlogLike.objects.filter(user=user, blog=obj).exists()
        return False
    
    def get_is_read(self,obj):
        user=self.context['request'].user
        if user.is_authenticated:
            return BlogRead.objects.filter(user=user, blog=obj).exists()
        return False

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)