from django.contrib import admin

from .models import Autotag

class AutotagAdmin(admin.ModelAdmin):
    list_display = ("pk", "owner",)
    search_fields = ["pattern"]

admin.site.register(Autotag, AutotagAdmin)
