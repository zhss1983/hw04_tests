from django.contrib.auth import get_user_model
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
        )
        cls.form = PostForm
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.url_index = reverse('index')
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
