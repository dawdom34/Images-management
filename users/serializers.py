from rest_framework import serializers

from .models import Account, AccountTier


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Account
        fields = ['id', 'username', 'password']


class TierSerializer(serializers.Serializer):
    name = serializers.CharField()
    thumbnail_size = serializers.CharField()
    original_file = serializers.BooleanField()
    expiring_links = serializers.BooleanField()

    def validate(self, attrs):
        name = attrs['name']
        if not name.isalpha():
            raise serializers.ValidationError('Name can contain only letters')
        return attrs