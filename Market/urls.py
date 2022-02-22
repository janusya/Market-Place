from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings

from .yasg import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('stores/', include('stores.urls')),
    path('products/', include('product.urls')),
    path('likes/', include('likes.urls')),
    path('bookmarks/', include('bookmark.urls')),
    # for doc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
