import os
import mimetypes
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from mutagen import File as MutagenFile
from django.utils.text import slugify


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_file_size(value):
    if value.size > MAX_FILE_SIZE:
        raise ValidationError("File size should not exceed 5 MB.")


def format_duration(seconds):
    if not seconds:
        return "00:00"
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"


class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "name")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to="uploads/", validators=[validate_file_size])

    file_type = models.CharField(max_length=50, blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)  # seconds

    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_favourite = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if self.file:
            self.file_size = self.file.size
            mime_type, _ = mimetypes.guess_type(self.file.name)
            self.file_type = mime_type or "application/octet-stream"

        super().save(*args, **kwargs)

        # calculate duration once after file saved
        if self.file and is_new:
            try:
                audio = MutagenFile(self.file.path)
                if audio and audio.info and hasattr(audio.info, "length"):
                    length = audio.info.length

                    # fix ms vs sec
                    if length > 100000:
                        length = length / 1000

                    self.duration = int(length)
                    super().save(update_fields=["duration"])

            except Exception as e:
                print("Duration error:", e)

    @property
    def duration_display(self):
        return format_duration(self.duration)

    def delete(self, *args, **kwargs):
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return os.path.basename(self.file.name)