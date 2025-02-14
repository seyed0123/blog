from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import *

urlpatterns = [
    path('auth/', create_user, name='create_user'),
    path('auth/detail/', user_detail, name='user_detail'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posts/', post_list, name='list-posts'),
    path('posts/<int:pk>/', post_detail, name='retrieve-post'),
    path('posts/search', search_post, name='search-posts'),
    path('categories/', category_list, name='list-categories'),
    path('categories/<int:pk>/', category_detail, name='retrieve-category'),
]