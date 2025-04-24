from django.urls import path,include
from .views import UserListView, ToggleUserStatusView, AdminBlogViewSet, AdminCommentBlockView, AdminDashboardView
from rest_framework.routers import DefaultRouter

admin_router = DefaultRouter()
admin_router.register(r'blogs', AdminBlogViewSet, basename='admin-blogs')

urlpatterns = [
    path('', include(admin_router.urls)),
    path("users/", UserListView.as_view(), name="users-list"),
    path("users/<int:user_id>/toggle-status/", ToggleUserStatusView.as_view(), name="toggle-user-status"),
    path("comments/<int:comment_id>/toggle-status/", AdminCommentBlockView.as_view(), name="toggle-comment-status"),
    path("dashboard-stats/", AdminDashboardView.as_view(), name="admin-dashboard"),
]