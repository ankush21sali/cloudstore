from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . forms import UploadedFileForm, CreateFolderForm, AddFavourites
from . models import UploadedFile, Folder
from .utils import get_total_size, human_readable_size, filter_file
from django.db.models import Count

@login_required(login_url='signin')
def dashboard(request):

    form = UploadedFileForm(user=request.user)
    create_form = CreateFolderForm()
    

    # -------- Upload File Form --------
    if request.method == 'POST' and 'upload_file' in request.POST:
        form = UploadedFileForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            file_obj = form.save(commit=False)
            file_obj.user = request.user
            file_obj.folder = form.cleaned_data.get('folder')
            file_obj.save()
            return redirect('files:dashboard')
        

    # -------- Create Folder Form --------
    elif request.method == 'POST' and 'create_folder' in request.POST:
        create_form = CreateFolderForm(request.POST)

        if create_form.is_valid():
            name = create_form.cleaned_data['name']

            if Folder.objects.filter(user=request.user, name=name).exists():
                create_form.add_error('name', 'Folder already exists')
            else:
                folder_obj = create_form.save(commit=False)
                folder_obj.user = request.user
                folder_obj.save()
                return redirect('files:dashboard')
            

    user_files = UploadedFile.objects.filter(user=request.user)
    user_folders = Folder.objects.filter(user=request.user)

    recent_files = UploadedFile.objects.order_by('-uploaded_at')[:5]

    context = {
        'form': form,
        'create_form': create_form,
        'user_files': user_files,
        'user_folders': user_folders,
        'images': filter_file('image', request.user),
        'videos': filter_file('video', request.user),
        'audios': filter_file('audio', request.user),
        'docs': filter_file('application', request.user),
        'recent_files': recent_files
    }

    return render(request, 'files/dashboard.html', context)

    

@login_required(login_url='signin')
def videos(request):

    form = UploadedFileForm(user=request.user)           

    # ---------- Upload Video ----------
    if request.method == 'POST'and 'upload_video' in request.POST:
        form = UploadedFileForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            file_obj = form.save(commit=False)
            uploaded_file = request.FILES.get('file')

            if not uploaded_file.content_type.startswith('video'):
                messages.error(request, "Uploaded file is not a video.")
            else:
                file_obj.user = request.user
                file_obj.file_type = uploaded_file.content_type
                file_obj.save()
                return redirect('files:videos')
            

    videos = filter_file('video', request.user)

    # Calculate total videos size
    bytes_size = get_total_size(videos)

    context = {
        'videos': videos,
        'form': form,
        'total_size': human_readable_size(bytes_size)
    }

    return render(request, 'files/videos.html', context)



@login_required(login_url='signin')
def images(request):

    form = UploadedFileForm(user=request.user)           

    # ---------- Upload Images ----------
    if request.method == 'POST'and 'upload_image' in request.POST:
        form = UploadedFileForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            file_obj = form.save(commit=False)
            uploaded_file = request.FILES.get('file')

            if not uploaded_file.content_type.startswith('image'):
                messages.error(request, "Uploaded file is not a image.")
            else:
                file_obj.user = request.user
                file_obj.file_type = uploaded_file.content_type
                file_obj.save()
                return redirect('files:images')
            

    images = filter_file('image', request.user)

    # Calculate total videos size
    bytes_size = get_total_size(images)

    context = {
        'form': form,
        'images': images,
        'total_size': human_readable_size(bytes_size),
    }

    return render(request, 'files/images.html', context)



@login_required(login_url='signin')
def docs(request):
    form = UploadedFileForm(user=request.user)           

    # ---------- Upload Document ----------
    if request.method == 'POST'and 'upload_docs' in request.POST:
        form = UploadedFileForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            file_obj = form.save(commit=False)
            uploaded_file = request.FILES.get('file')

            if not uploaded_file.content_type.startswith('application'):
                messages.error(request, "Uploaded file is not a application.")
            else:
                file_obj.user = request.user
                file_obj.file_type = uploaded_file.content_type
                file_obj.save()
                return redirect('files:docs')
            

    docs = filter_file('application', request.user)

    # Calculate total videos size
    bytes_size = get_total_size(docs)

    context = {
        'docs': docs,
        'form': form,
        'total_size': human_readable_size(bytes_size)
    }

    return render(request, 'files/docs.html', context)




@login_required(login_url='signin')
def audios(request):
    form = UploadedFileForm(user=request.user)           

    # ---------- Upload Audio ----------
    if request.method == 'POST'and 'upload_audio' in request.POST:
        form = UploadedFileForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            file_obj = form.save(commit=False)
            uploaded_file = request.FILES.get('file')

            if not uploaded_file.content_type.startswith('audio'):
                messages.error(request, "Uploaded file is not a audio.")
            else:
                file_obj.user = request.user
                file_obj.file_type = uploaded_file.content_type
                file_obj.save()
                return redirect('files:audios')
            

    audios = filter_file('audio', request.user)

    # Calculate total Audios size
    bytes_size = get_total_size(audios)

    context = {
        'audios': audios,
        'form': form,
        'total_size': human_readable_size(bytes_size)
    }

    return render(request, 'files/audios.html', context)



def folder_detail(request, slug):
    folder = get_object_or_404(Folder, user=request.user, slug=slug)

    # -------- Upload File In Folder--------
    if request.method == 'POST' and 'upload_file' in request.POST:
        file = request.FILES.get('file')
        
        if file:
            UploadedFile.objects.create(
                file=file,
                user=request.user,
                folder=folder
            )
            messages.success(request, "File uploaded successfully!")

        else:
            messages.error(request, "No file selected!")
        return redirect('files:folder_detail', slug=slug)
            
    files = UploadedFile.objects.filter(folder=folder).order_by('-id')

    bytes_size = get_total_size(files)

    context = {
        'folder': folder,
        'files': files,
        'total_size': human_readable_size(bytes_size),
    }

    return render(request, 'files/folder_detail.html', context)






@login_required(login_url='signin')
def delete_file(request, id):
    request_path = request.META.get('HTTP_REFERER', 'files:dashboard')

    try:
        file = UploadedFile.objects.get(pk=id, user=request.user)
    except UploadedFile.DoesNotExist:
        messages.error(request, "File does not exist!")
        return redirect(request_path)

    file.delete()
    messages.success(request, "File deleted successfully!")
    return redirect(request_path)


def delete_folder(request, folder_id):
    try:
        folder = Folder.objects.get(pk=folder_id)
        folder.delete()
    except Folder.DoesNotExist:
        pass

    return redirect('files:dashboard')


@login_required(login_url='signin')
def favourites(request):
    user = request.user

    if request.method == 'POST':
        form = AddFavourites(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            file = form.cleaned_data['file']
            file.is_favourite = True
            file.save()
    else:
        form = AddFavourites(user=request.user)


    files = UploadedFile.objects.filter(
        user=user,
        is_favourite=True,
    ).order_by('-id')

    bytes_size = get_total_size(files)

    context = {
        'files': files,
        'total_size': human_readable_size(bytes_size),
        'form': form,
    }

    return render(request, 'files/favourites.html', context)



def favourite_item(request, id):
    if request.method == 'POST':
        file = UploadedFile.objects.get(user=request.user, pk=id)
        file.is_favourite = not file.is_favourite
        file.save()

        return JsonResponse({
            "status": "ok",
            "is_favourite": file.is_favourite
        })
    
    return JsonResponse({
        "status": "error",
        "message": "File DoesNotExist!"
    }, status=400)