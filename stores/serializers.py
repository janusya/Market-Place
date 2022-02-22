from rest_framework import serializers
from .models import Store, StoreFeedbacks


class StoreSerializer(serializers.ModelSerializer):
    founder = serializers.ReadOnlyField(source='founder.email')

    class Meta:
        model = Store
        fields = ('__all__')


class FeedbacksSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    store_name = serializers.SerializerMethodField("get_store_name")

    class Meta:
        model = StoreFeedbacks
        fields = (
            'body',
            'rating',
            'store',
            'author',
            'store_name',
        )

        # read_only_fields = ('store',)

    def get_store_name(self, store_feedback):
        name = store_feedback.store.name
        return name

    def validate(self, validated_data):
        rating = validated_data.get("rating")
        if int(rating) not in range(1, 6):
            raise serializers.ValidationError("Enter a value from 1 to 6")
        return validated_data

    def create(self, validated_data):
        request = self.context.get('request')
        feedback = StoreFeedbacks.objects.create(
            author=request.user,
            **validated_data
        )
        return feedback
