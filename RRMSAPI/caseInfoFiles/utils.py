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
    path = settings.MEDIA_ROOT
    os.makedirs(path, exist_ok=True)
    return path

def get_physical_path(container_file_path):
    """
    Convert container path → physical UNC path
    input path: /app/media/dept1/a.pdf
    Output Path: \\172.21.12.20\rrms\CID\dept1\a.pdf
    """
    relative_path = os.path.relpath(container_file_path, settings.MEDIA_ROOT)
    relative_path = relative_path.replace("/", "\\")  # Windows format

    return os.path.join(settings.PHYSICAL_MEDIA_ROOT, relative_path)


def physical_to_container_path(physical_path):
    """
    Convert:
    \\172.21.12.20\rrms\CID\dept1\a.pdf
    →
    /app/media/dept1/a.pdf
    """
    relative = physical_path.replace(settings.PHYSICAL_MEDIA_ROOT, "")
    relative = relative.lstrip("\\").replace("\\", "/")

    return os.path.join(settings.MEDIA_ROOT, relative)
