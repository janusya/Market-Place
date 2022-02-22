from django.urls import path, include
from .views import RetrieveStoreView, CreateStoreView, \
    UpdateStoreView, FeedBacksViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('feedbacks', FeedBacksViewSet)

app_name = 'stores'

urlpatterns = [
    path('', RetrieveStoreView().as_view()),
    path('create/', CreateStoreView().as_view()),
    path('update/', UpdateStoreView().as_view()),
    path('', include(router.urls))
]
