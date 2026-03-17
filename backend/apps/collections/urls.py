from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers as nested_routers
from .views import CollectionViewSet, CollectionItemViewSet

router = DefaultRouter()
router.register(r'collections', CollectionViewSet, basename='collection')

collections_router = nested_routers.NestedDefaultRouter(
    router, r'collections', lookup='collection'
)
collections_router.register(r'items', CollectionItemViewSet, basename='collection-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(collections_router.urls)),
]
