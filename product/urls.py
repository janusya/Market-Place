from django.urls import path

from .views import ProductListView, ProfileProductListView, \
    CreateProductView, DeleteProductView, UpdateProductView, \
    find_products, FilterProducByCategoryView, CategoryListView
from django.conf.urls.static import static
from django.conf import settings

app_name = 'product'
urlpatterns = [
    path('p/', ProductListView().as_view()),
    path('p/<product_id>/', ProductListView().as_view()),
    path('search/', find_products),
    path('categories/<slug:category_slug>/', FilterProducByCategoryView().as_view()),
    path('categories/', CategoryListView().as_view()),
    path('', ProfileProductListView().as_view()),
    path('create/', CreateProductView().as_view()),
    path('update/<int:product_id>/', UpdateProductView().as_view()),
    path('delete/<int:product_id>/', DeleteProductView().as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
