from .models import UploadedFile


def get_total_size(files):
    total = 0

    if not files:
        return 0

    if hasattr(files, "size") and not hasattr(files, "__iter__"):
        return files.size or 0

    for f in files:
        if hasattr(f, "file") and f.file and hasattr(f.file, "size"):
            total += f.file.size or 0
        elif hasattr(f, "size"):
            total += f.size or 0

    return total


def human_readable_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1000:
            return f"{bytes_size:.2f} {unit}"
        
        bytes_size /= 1000



def filter_file(file_name, user):
    
    files = UploadedFile.objects.filter(
        user=user,
        file_type__startswith=file_name,
    ).order_by('-uploaded_at')

    return files
