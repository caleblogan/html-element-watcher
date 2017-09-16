from django.contrib import admin

from .models import WatchedElement


@admin.register(WatchedElement)
class BookAdmin(admin.ModelAdmin):
    list_display = ('user', 'url', 'callback_url', 'element_value')
