from rest_framework import serializers

from .models import Account


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Account
        fields = ['id', 'username', 'password']