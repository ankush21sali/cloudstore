from django import forms
from . models import UploadedFile, Folder

class UploadedFileForm(forms.ModelForm):

    class Meta:
        model = UploadedFile
        fields = ['folder', 'file']

        widgets = {
            'folder': forms.Select(attrs={
                'class': 'form-select',
            }),

            'file': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }

    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Show only current user's folders
        if user:
            self.fields['folder'].queryset = Folder.objects.filter(user=user)
        else:
            self.fields['folder'].queryset = Folder.objects.none()

        # Make folder optional
        self.fields['folder'].required = False


class CreateFolderForm(forms.ModelForm):

    class Meta:
        model = Folder
        fields = ['name']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Folder Name',
            }),
        }


class AddFavourites(forms.Form):

    file = forms.ModelChoiceField(
        queryset=UploadedFile.objects.none(),
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["file"].queryset = UploadedFile.objects.filter(
                user=user,
                is_favourite=False
            )