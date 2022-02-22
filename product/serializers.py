from rest_framework import serializers

from .models import Product, Category


class ProductGetSerializer(serializers.ModelSerializer):
    store_name = serializers.SerializerMethodField("get_store_name")

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'image',
            'category',
            'description',
            'price',
            'stock',
            'store_name',
        )

    def get_store_name(self, store_of_product):
        name = store_of_product.seller.name
        return name


class ProfileProductSerializer(serializers.ModelSerializer):
    store_name = serializers.SerializerMethodField("get_store_name")

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'image',
            'category',
            'description',
            'price',
            'stock',
            'store_name',
        )

    def get_store_name(self, store_of_product):
        name = store_of_product.seller.name
        return name


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = (
            'register_date',
        )

