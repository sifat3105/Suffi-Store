from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    # profile_image = serializers.SerializerMethodField()

    # def get_profile_image(self, obj):
    #     if obj.account.profile_image:
    #         return obj.account.profile_image.url
        
    def get_name(self, obj):
        return obj.account.name
        
    class Meta:
        model = User
        fields = ('id', 'email', 'name')


    