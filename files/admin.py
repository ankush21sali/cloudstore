from django.contrib import admin
from .models import UploadedFile, Folder

# Register your models here.
admin.site.register(UploadedFile)
admin.site.register(Folder)