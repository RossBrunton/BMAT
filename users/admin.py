from django.contrib import admin

from .models import Settings

class SettingsAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ["user__username"]

admin.site.register(Settings, SettingsAdmin)
