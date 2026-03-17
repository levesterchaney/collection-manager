from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Collection, CollectionItem
from .serializers import (
    CollectionSerializer,
    CollectionDetailSerializer,
    CollectionItemSerializer,
    CollectionItemWriteSerializer,
)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        owner = obj.owner if hasattr(obj, 'owner') else obj.collection.owner
        return owner == request.user


class CollectionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'collection_type']
    ordering_fields = ['created_at', 'name', 'updated_at']

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user).prefetch_related('items')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CollectionDetailSerializer
        return CollectionSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        collection = self.get_object()
        return Response({
            'item_count': collection.item_count,
            'total_paid': collection.total_paid,
            'total_value': collection.total_value,
            'gain_loss': float(collection.total_value) - float(collection.total_paid),
        })


class CollectionItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'version', 'manufacturer', 'originating_property', 'status']
    ordering_fields = ['created_at', 'name', 'current_value', 'price_paid']

    def get_queryset(self):
        collection_id = self.kwargs.get('collection_pk')
        collection = get_object_or_404(
            Collection,
            pk=collection_id,
            owner=self.request.user
        )
        return CollectionItem.objects.filter(collection=collection)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CollectionItemWriteSerializer
        return CollectionItemSerializer

    def perform_create(self, serializer):
        collection_id = self.kwargs.get('collection_pk')
        collection = get_object_or_404(
            Collection,
            pk=collection_id,
            owner=self.request.user
        )
        serializer.save(collection=collection)
