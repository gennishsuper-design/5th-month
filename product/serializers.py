from django.db.models import Avg
from rest_framework import serializers
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Name may not be empty.')
        # unique name (case-insensitive) excluding current instance
        qs = Category.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Category with this name already exists.')
        return value

    class Meta:
        model = Category
        fields = ('id', 'name', 'products_count')


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Title may not be empty.')
        return value

    def validate_price(self, value):
        try:
            # Decimal comparison
            if value < 0:
                raise serializers.ValidationError('Price must be non-negative.')
        except TypeError:
            raise serializers.ValidationError('Invalid price value.')
        return value

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'stars', 'product')

    def validate_text(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Review text may not be empty.')
        return value

    def validate_stars(self, value):
        if value is None:
            raise serializers.ValidationError('Stars value is required.')
        if not (1 <= value <= 5):
            raise serializers.ValidationError('Stars must be between 1 and 5.')
        return value


class ProductReviewsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'category', 'reviews', 'rating')

    def get_rating(self, obj):
        average = obj.reviews.aggregate(avg_rating=Avg('stars'))['avg_rating']
        return round(average, 2) if average is not None else None
