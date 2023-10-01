from django.db import models

from users.models import Account


def images_filepath(self, filename):
    """
    Return path to save the original images
    """
    return f'images/{filename}'

def thumbnails_filepath(self, filename):
    """
    Return path to save the thumbnails
    """
    return f'thumbnails/{filename}'


class Thumbnail(models.Model):
    """
    Thumbnails of the image
    """
    size = models.IntegerField()
    thumbnail = models.ImageField(upload_to=thumbnails_filepath)


class Image(models.Model):
    """
    Original images
    """
    thumbnails = models.ManyToManyField(Thumbnail, help_text='Thumbnails created from original image', blank=True, null=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=images_filepath, blank=False, null=False)
