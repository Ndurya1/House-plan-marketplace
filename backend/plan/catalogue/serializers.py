from rest_framework import serializers
from .models import Catalogue


class catalogueSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.user.name', read_only=True)

    class Meta:
        model = Catalogue
        fields = [
            'id',
            'title',
            'category',
            'category_group',
            'description',
            'designs',
            'price',
            'thumbnail',
            'seller',
            'seller_name',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['seller', 'created_at', 'updated_at']

    def validate_category(self, value):
        return value.strip().title()

    def validate(self, attrs):
        if self.instance is None and not attrs.get('category_group'):
            raise serializers.ValidationError(
                {'category_group': 'Category group is required when posting a plan.'}
            )
        return attrs
