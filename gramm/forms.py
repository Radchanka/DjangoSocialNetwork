from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser, Post, Image
from cloudinary.forms import CloudinaryFileField


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class CustomUserEditForm(forms.ModelForm):
    avatar = CloudinaryFileField(
        options={
            'folder': 'avatars',
            'resource_type': 'auto',
            'overwrite': True,
            'width': 300,
            'height': 300,
        }
    )

    class Meta:
        model = CustomUser
        fields = ['full_name', 'biography', 'avatar']


class PostForm(forms.ModelForm):
    tags = forms.CharField(max_length=255, required=False, help_text='Enter tags separated by commas (optional)')

    class Meta:
        model = Post
        fields = ['caption', 'tags']


class ImageForm(forms.ModelForm):
    image = CloudinaryFileField(
        options={
            'folder': 'post_images',
            'resource_type': 'auto',
        }
    )

    class Meta:
        model = Image
        fields = ['image']


ImageFormSet = forms.inlineformset_factory(Post, Image, form=ImageForm, extra=3)
