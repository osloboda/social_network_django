from django.contrib import admin
from django.urls import path, include
from .views import Post, Like, ObtainToken, Analytics, Activity

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('login', ObtainToken.as_view()),
    path('post/', Post.as_view()),
    path('like/<int:post_id>', Like.as_view()),
    path('analytics/', Analytics.as_view()),
    path('activity/', Activity.as_view())
]
