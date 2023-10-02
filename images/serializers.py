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
    

class OriginalImageSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        try:
                _ = Image.objects.get(id=attrs['id'])
        except Image.DoesNotExist:
            raise serializers.ValidationError('Image with given id does not exist')


class ThumbnailSerializer(serializers.Serializer):
    image_id = serializers.IntegerField()
    size = serializers.IntegerField()

    def validate(self, attrs):
        try:
                _ = Image.objects.get(id=attrs['image_id'])
        except Image.DoesNotExist:
            raise serializers.ValidationError('Image with given id does not exist')


class ExpiredLinkSerializer(serializers.Serializer):
    time = serializers.IntegerField()
    image_id = serializers.IntegerField()

    def validate(self, attrs):
        if attrs['time'] >= 300 and attrs['time'] <= 30000:
            try:
                _ = Image.objects.get(id=attrs['image_id'])
            except Image.DoesNotExist:
                raise serializers.ValidationError('Image with given id does not exist')
        else:
            raise serializers.ValidationError('Expiration time not between 300 and 30000 seconds')
        return attrs
        