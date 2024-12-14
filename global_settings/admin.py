from django.contrib import admin

from global_settings.models import GlobalSettings, FileExtension

admin.site.register(GlobalSettings)
admin.site.register(FileExtension)
