from rest_framework import serializers

from .models import Account, AccountTier


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Account
        fields = ['id', 'username', 'password']


class TierSerializer(serializers.ModelSerializer):
    thumbnail_size = serializers.CharField()

    class Meta:
        model = AccountTier
        fields = ['name', 'thumbnail_size', 'original_file', 'expiring_links']