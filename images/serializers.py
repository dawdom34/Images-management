from rest_framework import serializers

from .models import Image
from .constants import ALLOWED_IMAGE_EXTENSIONS


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['owner', 'image']

    def create(self, validated_data):
        files = self.context['request'].FILES
        image = files['image']
        extension = image.name.split('.')[-1]
        # Image format validation
        if not extension.lower() in ALLOWED_IMAGE_EXTENSIONS:
            raise serializers.ValidationError(f'Invalid uploaded file type: {extension}')
        
        return Image.objects.create(**validated_data)