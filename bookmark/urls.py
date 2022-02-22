from django.urls import path

from .views import ListBookmarkView, CreateBookmarkView,\
    DeleteBookmarkView

app_name = 'bookmark'

urlpatterns = [
    path('', ListBookmarkView().as_view()),
    path('add/', CreateBookmarkView().as_view()),
    path('delete/<product_id>/', DeleteBookmarkView().as_view()),
]
