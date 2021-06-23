from http import HTTPStatus

from django.test import TestCase

from .test_setups import MySetupTestCase
from posts.forms import PostForm
from posts.models import Post


class PostsSaveTests(TestCase, MySetupTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        MySetupTestCase.setUpClass()

    def test_posts_contain_form(self):
        """Check templates on form context containing."""
        cls = self.__class__
        url_list = (
            cls.url_new_post,
            cls.url_post_edit,
        )
        for url in url_list:
            response = cls.authorized_client.get(url)
            self.assertIn('form', response.context)
            form = response.context['form']
            for field, value in PostForm().fields.items():
                with self.subTest(form_field=field):
                    self.assertIsInstance(form.fields[field], type(value))

    def test_auth_uses_save_post_and_correct_template(self):
        """Check matching of template name and URL address."""
        cls = self.__class__
        auth_url_list = (
            (
                cls.url_new_post,
                cls.url_index,
                {
                    'group': cls.group.pk,
                    'text': ('Save new post (group = '
                             f'{cls.group.pk}). {id(cls.group)}')
                },
            ),
            (
                cls.url_new_post,
                cls.url_index,
                {
                    'group': '',
                    'text': f'Save new post without group.  {id(cls.group)}'
                },
            ),
            (
                cls.url_post_edit,
                cls.url_post,
                {
                    'group': cls.group.pk,
                    'text': ('Edit post (group = '
                             f'{cls.group.pk}).  {id(cls.group)}')
                },
            ),
            (
                cls.url_post_edit,
                cls.url_post,
                {
                    'group': '',
                    'text': f'Edit post without group.  {id(cls.group)}'
                },
            ),
        )
        for url, redirect_name, context in auth_url_list:
            with self.subTest(url=url, context=context):
                response = cls.authorized_client.post(url, data=context)
                post = Post.objects.filter(text=context['text']).last()
                self.assertEqual(response.url, redirect_name)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)
                self.assertEqual(post.author, cls.user)
                if context['group'] != '':
                    self.assertEqual(post.group.pk, context['group'])
                else:
                    self.assertIsNone(post.group)
