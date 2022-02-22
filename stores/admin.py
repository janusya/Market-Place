from django.contrib import admin
from .models import Store, StoreFeedbacks


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'founder',
        'register_date',

    )
    list_filter = (
        'register_date',
    )


admin.site.register(StoreFeedbacks)
