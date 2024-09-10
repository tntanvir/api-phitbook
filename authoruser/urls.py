from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


# router = DefaultRouter()
# router.register('user', views.MainUserView ,basename='user')
# router.register('usermore', views.AllUserView ,basename='usermore')


# The API URLs are now determined automatically by the router.
urlpatterns = [
    # path('', include(router.urls)),
    path('user/', views.MainUserView.as_view(), name='user-list'),
    path('user/<int:pk>/', views.MainUserView.as_view(), name='user-detail'),
    path('usermore/',views.AllUserView.as_view(),name='usermore'),
    path('registar/',views.PatientRegistration.as_view(),name='registar'),
    path('active/<uid64>/<token>/',views.activate ),
    path('login/',views.UserLogin.as_view(),name='login'),
    path('logout/',views.Userlogout.as_view(),name='logout'),

    path('user/<str:username>/follow/', views.FollowUserView.as_view(), name='follow-unfollow'),
    path('user/<str:username>/followers/', views.FollowersView.as_view(), name='user-followers'),
    path('user/<str:username>/following/', views.FollowingView.as_view(), name='user-following'),
    path('user/<str:username>/follow-status/', views.FollowStatusAPIView.as_view(), name='follow-status'),
]