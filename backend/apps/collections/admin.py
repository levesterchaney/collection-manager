from django.contrib import admin
from .models import Collection, CollectionItem


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'collection_type', 'item_count', 'is_public', 'created_at']
    list_filter = ['collection_type', 'is_public']
    search_fields = ['name', 'owner__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CollectionItem)
class CollectionItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'version', 'collection', 'status', 'price_paid', 'current_value']
    list_filter = ['status', 'collection__collection_type']
    search_fields = ['name', 'manufacturer', 'originating_property']
    readonly_fields = ['created_at', 'updated_at']
