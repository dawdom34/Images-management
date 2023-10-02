from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication

from django.utils import timezone
from django.core.signing import Signer

from users.models import Account

from .serializers import ImageSerializer, OriginalImageSerializer, ThumbnailSerializer, ExpiredLinkSerializer
from .models import Image, Thumbnail, TemporaryImages
from .utils import resize_image


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def image_save(request):
    """
    Save image to the database
    """
    serializer = ImageSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "Image saved"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def list_images(request):
    """
    Get links to all images
    """
    data = {}
    user = request.user
    images = Image.objects.filter(owner=user)
    for img in images:
        data[img.id] = img.image.url
    return Response({"data": data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_original_image(request):
    """
    Returns link to original image
    """
    serializer = OriginalImageSerializer(data=request.data)
    if serializer.is_valid():
        image_id = serializer.data['id']
        # Check if image with given id exist
        try:
            image = Image.objects.get(id=image_id)
            # check if user have permissions to get link to original image
            user_id = request.user.id
            user = Account.objects.get(id=user_id)
            if user.account_tier.original_file == True:
                data = {}
                data['id'] = image.id
                data['image'] = image.image.url
                return Response({"data": data}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Account tier of given user does not allow to get  original size image."}, status=status.HTTP_400_BAD_REQUEST)

        except Image.DoesNotExist:
            return Response({"error": "Image with given id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_thumbnail(request):
    """
    Get thumbnail of the given size
    """
    serializer = ThumbnailSerializer(data=request.data)
    if serializer.is_valid():
        image_id = serializer.data['image_id']
        size = serializer.data['size']
        # Check if user can generate link with given size
        user = Account.objects.get(id=request.user.id)
        tier_sizes = [x.size for x in user.account_tier.thumbnail_size.all()]
        if size in tier_sizes:
            #Check if image with given id exist
            try:
                image_obj = Image.objects.get(id=image_id)
                # Check if a thumbnail with the given size exists for a given image
                created_sizes = [x.size for x in image_obj.thumbnails.all()]
                if size in created_sizes:
                    c = image_obj.thumbnails.get(size=size)
                    data = {}
                    data['id'] = c.id
                    data['image'] = c.thumbnail.url
                    return Response({"data": data}, status=status.HTTP_200_OK)
                else:
                    # Create new thumbnail


                    resized_image = resize_image(image_obj, size)

                    # Save resized image to database
                    thumbnail = Thumbnail(size=size, thumbnail=resized_image)
                    thumbnail.save()
                    # Add resized image to relation
                    image_obj.thumbnails.add(thumbnail)

                    # Return image
                    data = {}
                    data['id'] = thumbnail.id
                    data['image'] = thumbnail.thumbnail.url
                    return Response({"data": data}, status=status.HTTP_200_OK)

            except Image.DoesNotExist:
                return Response({"error": "Image with given id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Account tier of given user does not allow to generate thumbnails with given size."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def generate_expiring_image_link(request):
    """
    Generate a link to an image that will expire after a specified time
    """
    serializer = ExpiredLinkSerializer(data=request.data)
    if serializer.is_valid():
        # Get validated data from serializer
        image_id = serializer.data['image_id']
        time = serializer.data['time']
        # Check if user have permissions to generate expired links
        user_id = request.user.id
        user = Account.objects.get(id=user_id)
        if user.account_tier.expiring_links == True:
            # Check if image with given id exist
            try:
                image = Image.objects.get(id=image_id)
                # Check if expiration time is between 300 and 30000 seconds:
                if time >= 300 and time <= 30000:
                    # Calculate expiration time
                    exp_time = timezone.now() + timezone.timedelta(seconds=time)
                    # Create Temporary image object
                    tp = TemporaryImages.objects.create(image=image.image, expiration_date=exp_time)
                    # Sign temporary image object id
                    signer = Signer()
                    signed_link = signer.sign(tp.id)
                    # Create new url with signed id
                    full_url = f'/validate_expire_link/{signed_link}'
                    return Response({"data": full_url}, status=status.HTTP_200_OK)
                else:
                    return Response({"data": "Expiration time not between 300 and 30000 seconds"}, status=status.HTTP_400_BAD_REQUEST)
            except Image.DoesNotExist:
                return Response({"data": "Image with given id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"data": "Account tier of given user does not allow to generate expired links"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)