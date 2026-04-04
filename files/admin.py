from django.contrib import admin
from .models import UploadedFile, Folder

# Register your models here.

class FolderAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'created_at')
    list_per_page = 20
    search_fields = ('user__username', 'name')
    ordering = ['-created_at']


class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'folder', 'file_size', 'uploaded_at', 'is_favourite')
    list_editable = ('is_favourite',)
    list_filter = ('user', 'folder', 'is_favourite')
    list_per_page = 10
    search_fields = ('user__username', 'folder__name')
    ordering = ['-uploaded_at']

    list_select_related = ('user', 'folder')

admin.site.register(UploadedFile, UploadedFileAdmin)
admin.site.register(Folder, FolderAdmin)