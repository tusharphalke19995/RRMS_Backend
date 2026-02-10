from .models import FileUsage
from django.utils import timezone
import os
from django.conf import settings

def record_file_access(user, file):
    FileUsage.objects.update_or_create(
        user=user,
        file=file,
        defaults={'last_accessed': timezone.now()}
    )

def get_upload_dir():
    path = os.path.join(settings.MEDIA_ROOT, settings.UPLOAD_SUBDIR)
    os.makedirs(path, exist_ok=True)
    return path