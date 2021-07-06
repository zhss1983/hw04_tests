import tempfile
import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Group, Post

User = get_user_model()


class MySetupTestCase():
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(
            username='user',
        )
        cls.group = Group.objects.create(
            title='Тест ' * 40,
            slug='test_' * 30,
            description='Текст ' * 50,
        )
        cls.post = Post.objects.create(
            text='Тест ' * 100,
            author=cls.user,
            group=cls.group,
            image=cls.img_upload()
        )
        cls.form = PostForm
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.url_index = reverse('index')
        cls.url = reverse('index')
        cls.url_new_post = reverse('new_post')
        cls.url_group = reverse('group', kwargs={'slug': cls.group.slug})
        cls.url_profile = reverse(
            'profile',
            kwargs={'username': cls.user.username}
        )
        cls.url_post_edit = reverse(
            'post_edit',
            kwargs={
                'username': cls.user.username,
                'post_id': cls.post.pk
            }
        )
        cls.url_post = reverse(
            'post',
            kwargs={
                'username': cls.user.username,
                'post_id': cls.post.pk
            }
        )

    @classmethod
    def init_media(cls):
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    @classmethod
    def img_upload(cls):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        return SimpleUploadedFile(
                   name='small.gif',
                   content=small_gif,
                   content_type='image/gif'
               )
