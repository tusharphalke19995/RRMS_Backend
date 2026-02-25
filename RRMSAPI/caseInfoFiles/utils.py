from pathlib import Path, PureWindowsPath
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
    container_path = Path(container_file_path)
    media_root = Path(settings.MEDIA_ROOT)

    relative_path = container_path.relative_to(media_root)

    # always build WINDOWS path
    physical_path = PureWindowsPath(settings.PHYSICAL_MEDIA_ROOT) / relative_path

    return str(physical_path)

def physical_to_container_path(physical_path):
    """
    Convert:
    \\172.21.12.20\rrms\CID\dept1\a.pdf
    →
    /app/media/dept1/a.pdf
    """
    physical_root = PureWindowsPath(settings.PHYSICAL_MEDIA_ROOT)
    full_path = PureWindowsPath(physical_path)

    relative = full_path.relative_to(physical_root)

    return str(Path(settings.MEDIA_ROOT) / relative)
