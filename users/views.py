from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from .models import Account, AccountTier, ThumbnailSizes
from .serializers import UserSerializer, TierSerializer


@api_view(['POST'])
def login_user(request):
    user = get_object_or_404(Account, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Wrong username or password"}, status=status.HTTP_404_NOT_FOUND)
    authenticate(username=request.data['username'], password=request.data['password'])
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def logout_user(request):
    try:
        request.user.auth_token.delete()
    except:
        pass
    return Response({"detail": "Logout successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_tier(request):
    """
    Create new acount tier
    """

    # Check if user have admin permissions
    if request.user.is_admin:
        serialzier = TierSerializer(data=request.data)
        if serialzier.is_valid():
            # Save data from serializer
            tier_name = serialzier.data['name']
            original_file = serialzier.data['original_file']
            expiring_links = serialzier.data['expiring_links']
            # Convert thumbnail_size (string) to list
            thumbnail_size = serialzier.data['thumbnail_size'].split(',')
            # Validate data
            try:
                sizes = [int(x) for x in thumbnail_size]
                if 0 in sizes:
                    return Response({"error": "invalid data type for thumbnail_size"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "invalid data type for thumbnail_size"}, status=status.HTTP_400_BAD_REQUEST)

            # Create account tier object
            new_tier = AccountTier.objects.create(name=tier_name, original_file=original_file, expiring_links=expiring_links)

            # Assign thumbnail sizes to new created account tier
            for size in sizes:
                new_size = ThumbnailSizes.objects.get_or_create(size=size)
                new_tier.thumbnail_size.add(new_size[0])
            
            return Response({"detail": "New tier created"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serialzier.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Access denied"}, status=status.HTTP_401_UNAUTHORIZED)