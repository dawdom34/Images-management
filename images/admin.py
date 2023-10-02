from django.contrib import admin
from django.utils.html import format_html

from .models import Image, Thumbnail, TemporaryImages


class ImageAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html(f'<img src={obj.image.url} style="max-width:200px; max-height:200px"/>')
    
    list_display = ('owner', 'image_tag')


admin.site.register(Image, ImageAdmin)


class ThumbnailAdmin(admin.ModelAdmin):
    def thumbnail_tag(self, obj):
        return format_html(f'<img src={obj.thumbnail.url} style="max-width:200px; max-height:200px"/>')
    
    list_display = ('size', 'thumbnail_tag')

admin.site.register(Thumbnail, ThumbnailAdmin)


class TemporaryImagesAdmin(admin.ModelAdmin):
    def img_tag(self, obj):
        return format_html(f'<img src={obj.image.url} style="max-width:200px; max-height:200px"/>')
    
    list_display = ('expiration_date', 'image')

admin.site.register(TemporaryImages, TemporaryImagesAdmin)