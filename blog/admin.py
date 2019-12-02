from django.contrib import admin

# Register your models her.

from .models import Post, Tag, Images

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Images)

