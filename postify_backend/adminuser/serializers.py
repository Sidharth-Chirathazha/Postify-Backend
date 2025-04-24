from rest_framework.serializers import ModelSerializer,SerializerMethodField,IntegerField
from django.contrib.auth import get_user_model
from blogs.models import Comment,BlogPost

User = get_user_model()


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_pic', 'is_active', 'date_joined']
        read_only_fields = ['id']

class UserBlogSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_pic']
        read_only_fields = ['id']

class AdminCommentSerializer(ModelSerializer):
    replies = SerializerMethodField()
    user = UserBlogSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'replies', 'parent_comment', 'blog', 'is_active']
        read_only_fields = ['id','blog']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            replies = obj.replies.all()
            return AdminCommentSerializer(replies, many=True, context=self.context).data
        return []
    
class AdminBlogSerializer(ModelSerializer):
    author = UserBlogSerializer(read_only=True)
    comments = AdminCommentSerializer(many=True, read_only=True)
    like_count = IntegerField(read_only=True)
    read_count = IntegerField(read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'content', 'image_1', 'image_2', 'image_3', 'created_at', 'updated_at', 'is_active', 'like_count', 'read_count', 'comments']
