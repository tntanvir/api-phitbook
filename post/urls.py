from django.urls import path, include
from . import views






# The API URLs are now determined automatically by the router.
urlpatterns = [
  
    path('allpost/', views.AllPostView.as_view(), name='allpost'),
    path('posts/following/', views.FollowingPostsAPIView.as_view(), name='following-posts'),
    path('likes/', views.LikeView.as_view(), name='likes'),
    path('allpost/<int:pk>/', views.PostDetailView.as_view(), name='postdetail'),
    path('allcomment/', views.AllCommentsView.as_view(), name='allcomment'),
    
]