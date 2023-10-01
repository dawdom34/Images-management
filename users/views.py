from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from .models import Account
from .serializers import UserSerializer


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