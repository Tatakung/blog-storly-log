from django.contrib import admin

# Register your models here.
from .models import Category, Blog,Comment
admin.site.register(Blog)
admin.site.register(Comment)