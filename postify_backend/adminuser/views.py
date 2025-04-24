from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from django.contrib.auth import get_user_model
from blogs.models import BlogPost, Comment
from .serializers import UserListSerializer,AdminBlogSerializer


User = get_user_model()

# Create your views here.

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserListView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.exclude(role="admin").order_by('id')
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['username']

class ToggleUserStatusView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.is_active = not user.is_active
            user.save()
            return Response({
                "id": user.id,
                "is_active": user.is_active,
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
             return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        

class AdminBlogViewSet(ModelViewSet):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = AdminBlogSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'author__username']
    filterset_fields = ['is_active']

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        try:
            blog = self.get_object()
            blog.is_active = not blog.is_active
            blog.save()
            return Response({
                "message": f"Blog post {'deactivated' if not blog.is_active else 'activated'} successfully.",
                "is_active": blog.is_active  
            }, status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response({"error": "Blog post not found."}, status=status.HTTP_404_NOT_FOUND)
   


class AdminCommentBlockView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.is_active = not comment.is_active
            comment.save()
            return Response({
                "message": f"Comment {'unblocked' if comment.is_active else 'blocked'} successfully.",
                "id": comment.id,
                "is_active": comment.is_active
            }, status=status.HTTP_200_OK)

        except Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
        
class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = User.objects.exclude(role="admin").count()
        total_blogs = BlogPost.objects.count()
        active_users = User.objects.exclude(role="admin").filter(is_active=True).count()

        return Response({
            "total_users": total_users,
            "total_blogs": total_blogs,
            "active_users": active_users
        }, status=status.HTTP_200_OK)