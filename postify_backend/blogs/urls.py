from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import BlogPostViewSet, UserBlogListView, BlogLikeToggleView, CommentView, CommentDeleteView, BlogReadView

router = DefaultRouter()
router.register(r'posts', BlogPostViewSet, basename='posts')

urlpatterns = [
    *router.urls,
    path('my-posts/', UserBlogListView.as_view(), name='my_posts'),
    path('<int:blog_id>/like/', BlogLikeToggleView.as_view(), name='blog_like_toggle'),
    path('<int:blog_id>/read/', BlogReadView.as_view(), name='blog_read'),
    path('<int:blog_id>/comment/', CommentView.as_view(), name='add_comment'),
    path('comment/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
]
