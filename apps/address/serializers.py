from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [ 'id', 'city', 'area', 'postal_code', 'block_sector', 'street_road', 'house_no', 'flat_no', 
                  'floor_no', 'name', 'phone', 'address_type', 'is_default'
            ]
        read_only_fields = ['id']

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        if user is None:
            user = None
            request = self.context.get('request') if self.context else None
            if request and hasattr(request, 'user'):
                user = request.user

       
        if validated_data.get('is_default', False) and user is not None:
            Address.objects.filter(user=user, is_default=True).update(is_default=False)

        return Address.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        
        if validated_data.get('is_default', False):
            Address.objects.filter(user=instance.user, is_default=True).exclude(id=instance.id).update(is_default=False)
        return super().update(instance, validated_data)
