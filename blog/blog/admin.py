from django.contrib import admin

# Register your models here.
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author',)
    search_fields = ('id', 'title', 'author')

