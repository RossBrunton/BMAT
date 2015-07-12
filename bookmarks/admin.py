from django.contrib import admin

from .models import Bookmark

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("pk", "owner",)
    search_fields = ["title", "url"]

admin.site.register(Bookmark, BookmarkAdmin)
