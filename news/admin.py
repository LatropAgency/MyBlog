from django.contrib import admin
from .models import News, Comments, Extended

admin.site.register(News)
admin.site.register(Comments)
admin.site.register(Extended)