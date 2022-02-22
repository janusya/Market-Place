from django.urls import path

from .views import LikeView, DisLikeView

app_name = 'likes'
urlpatterns = [
    path('like/', LikeView().as_view()),
    path('dislike/', DisLikeView().as_view()),
]
