from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Account
        fields = ['id', 'name', 'profile_image', 'phone', 'country', 'created_at', 'updated_at', 'email']
        read_only_fields = ['id', 'created_at', 'updated_at', 'email']
    def update(self, instance, validated_data):
        # Update only the fields provided in validated_data
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
    
    # def get_profile_image(self, value):
    #     request = self.context.get('request')
    #     if value and request:
    #         return request.build_absolute_uri(value.url)
    #     return None