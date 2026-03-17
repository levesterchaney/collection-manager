from rest_framework import serializers
from .models import Collection, CollectionItem


class CollectionItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CollectionItem
        fields = [
            'id', 'collection', 'name', 'version', 'description',
            'price_paid', 'current_value', 'manufacturer',
            'originating_property', 'status', 'image', 'image_url',
            'acquired_at', 'notes', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def validate_collection(self, value):
        request = self.context.get('request')
        if value.owner != request.user:
            raise serializers.ValidationError("You do not own this collection.")
        return value


class CollectionItemWriteSerializer(CollectionItemSerializer):
    class Meta(CollectionItemSerializer.Meta):
        fields = [f for f in CollectionItemSerializer.Meta.fields if f != 'image_url']


class CollectionSerializer(serializers.ModelSerializer):
    item_count = serializers.ReadOnlyField()
    total_paid = serializers.ReadOnlyField()
    total_value = serializers.ReadOnlyField()
    cover_image_url = serializers.SerializerMethodField()
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Collection
        fields = [
            'id', 'name', 'description', 'collection_type',
            'cover_image', 'cover_image_url', 'is_public',
            'item_count', 'total_paid', 'total_value',
            'owner_email', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'owner_email', 'created_at', 'updated_at']

    def get_cover_image_url(self, obj):
        request = self.context.get('request')
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        return None


class CollectionDetailSerializer(CollectionSerializer):
    items = CollectionItemSerializer(many=True, read_only=True)

    class Meta(CollectionSerializer.Meta):
        fields = CollectionSerializer.Meta.fields + ['items']
