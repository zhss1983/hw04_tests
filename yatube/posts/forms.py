from PIL import Image

from django import forms
from django.conf import settings

from .models import Comment, Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('group', 'text', 'image')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_image(self):
        image = self.cleaned_data['image']
        if not image:
            return image
        img = Image.open(image)
        if img.width < settings.MIN_WIDTH:
            raise forms.ValidationError(
                (f'Ширина изображения меньше {settings.MIN_WIDTH} px, '
                 f'загрузите изображение по меньшей мере {settings.MIN_WIDTH}x'
                 f'{settings.MIN_HEIGHT} px.'),
                params={'width': img.width},
            )
        if img.height < settings.MIN_HEIGHT:
            raise forms.ValidationError(
                (f'Высота изображения меньше {settings.MIN_HEIGHT} px, '
                 f'загрузите изображение по меньшей мере {settings.MIN_WIDTH}x'
                 f'{settings.MIN_HEIGHT} px.'),
                params={'height': img.height},
            )
        return image


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
