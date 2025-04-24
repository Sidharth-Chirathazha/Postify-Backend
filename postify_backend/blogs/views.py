from rest_framework import viewsets,permissions,status
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied,NotFound
from rest_framework.response import Response
from .models import BlogPost, Comment, BlogLike, BlogRead
from .serializers import BlogPostSerializer, CommentSerializer, BlogLikeSerializer, BlogReadSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a blog post to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'author__username']
    ordering_fields = ['created_at','read_count']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.author != request.user:
            raise PermissionDenied("You do not have permission to edit this blog post.")
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.author != request.user:
            raise PermissionDenied("You do not have permission to delete this blog post.")
        return super().destroy(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except BlogPost.DoesNotExist:
            raise NotFound("Blog post not found.")
        

    
class UserBlogListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            blogs = BlogPost.objects.filter(author=request.user).order_by('-created_at')
            serializer = BlogPostSerializer(blogs, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Something went wrong while fetching your blogs."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class BlogLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, blog_id):
        try:
            blog = BlogPost.objects.get(id=blog_id)
            like, created = BlogLike.objects.get_or_create(user=request.user, blog=blog)
            if not created:
                like.delete()
                blog.like_count = blog.likes.count()
                blog.save()
                return Response({"message": "Blog unliked."}, status=status.HTTP_200_OK)
            blog.like_count = blog.likes.count()
            blog.save()
            return Response({"message": "Blog liked."}, status=status.HTTP_201_CREATED)
        except BlogPost.DoesNotExist:
            return Response({"detail": "Blog not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class BlogReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, blog_id):
        try:
            blog = BlogPost.objects.get(pk=blog_id)
            _, created = BlogRead.objects.get_or_create(user=request.user, blog=blog)
            if created:
                blog.read_count = blog.reads.count()
                blog.save()
                return Response({"message": "Blog marked as read."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Blog already marked as read."}, status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response({"detail": "Blog not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({'error': 'Error while updating read count'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, blog_id):
        try:
            blog = BlogPost.objects.get(pk=blog_id)
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, blog=blog)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BlogPost.DoesNotExist:
            return Response({"error": "Blog not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Failed to add comment'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CommentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)

            if comment.user == request.user:
               
                comment.delete()
                return Response({'message': 'Comment deleted'}, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'You do not have permission to delete this comment'}, status=status.HTTP_403_FORBIDDEN)

        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error deleting comment: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
