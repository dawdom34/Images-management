"""
URL configuration for images_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from users.views import login_user, logout_user, create_tier

from images.views import image_save, list_images, get_original_image, get_thumbnail, generate_expiring_image_link, validate_expired_link

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    # Authentication
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    # Create new account tier
    path('create_tier/', create_tier, name='create_tier'),
    # Save new image to db
    path('image_save/', image_save, name='image_save'),
    # Get links to all images
    path('list_images/', list_images, name='list_images'),
    # Get link to original image
    path('get_original_image/', get_original_image, name='get_original_file'),
    # Get link to the thumbnail with given size
    path('get_thumbnail/', get_thumbnail, name='get_thumbnail'),
    # Generate expiring link
    path('generate_expiring_link/', generate_expiring_image_link, name='generate_expiring_image_link'),
    # Validate expired link
    path('validate_link/<link>/', validate_expired_link, name='validate_link'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)