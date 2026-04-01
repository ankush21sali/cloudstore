from .models import UploadedFile
from .utils import get_total_size, human_readable_size

def vault_space(request):
    if not request.user.is_authenticated:
        return {'total_space': '50 MB'}
    files = UploadedFile.objects.filter(user=request.user)
    bytes_size = get_total_size(files)
    total_space = human_readable_size(bytes_size)

    return {'total_space': total_space}
