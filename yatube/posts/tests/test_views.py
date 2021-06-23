from datetime import datetime as dt
from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from .test_setups import MySetupTestCase
from posts.models import Group, Post, User
from posts.views import my_paginator
from yatube.settings import DELTA_PAGE_COUNT, MAX_PAGE_COUNT


class PostsURLTests(TestCase, MySetupTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        MySetupTestCase.setUpClass()

    def test_url_uses_correct_template_by_guest(self):
        """Check matching of template name and URL address."""
        cls = self.__class__
        url_list = (
            (cls.url_index, 'posts/index.html'),
            (cls.url_profile, 'posts/profile.html'),
            (cls.url_post, 'posts/post.html'),
            (cls.url_group, 'posts/group.html'),
        )
        for url, template_name in url_list:
            response = self.client.get(url)
            with self.subTest(url=url):
                self.assertTemplateUsed(response, template_name=template_name)

    def test_url_uses_correct_template_auth_user(self):
        """Check matching of template name and URL address."""
        cls = self.__class__
        auth_url_list = (
            (cls.url_new_post, 'posts/manage_post.html'),
            (cls.url_post_edit, 'posts/manage_post.html'),
        )
        for url, template_name in auth_url_list:
            response = self.authorized_client.get(url)
            with self.subTest(url=url):
                self.assertTemplateUsed(response, template_name=template_name)

    def test_posts_contain_in_correct_group(self):
        """Check correct access by group."""
        cls = self.__class__
        new_group = Group.objects.create(
            title='Group №2',
            slug='test_group_2',
            description='Тестовая группа № 2',
        )
        context = {
            'group': cls.group.pk,
            'text': f'Test post (group = {cls.group.pk}). {id(cls.group)}'
        }
        cls.authorized_client.post(cls.url_new_post, data=context)
        my_post = Post.objects.filter(text=context['text']).last()
        in_list_url = (
            cls.url_index,
            cls.url_group,
        )
        for url in in_list_url:
            with self.subTest(url=url):
                response = cls.authorized_client.get(url)
                posts = response.context['page'].object_list
                self.assertIn(my_post, posts)
        url_new_group = reverse('group', kwargs={'slug': new_group.slug})
        response = cls.authorized_client.get(url_new_group)
        posts = response.context['page'].object_list
        self.assertNotIn(my_post, posts)

    def test_wron_user_edit_post(self):
        """Check redirect from edit_post page for an unauthorized user."""
        cls = self.__class__
        authorized_client = Client()
        other_user = User.objects.create(
            username='other_user',
        )
        authorized_client.force_login(other_user)
        response = authorized_client.get(cls.url_post_edit)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, cls.url_post)


class PostsContextTests(TestCase, MySetupTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        MySetupTestCase.setUpClass()

    def test_posts_shows_correct_context(self):
        """Check specific context, not paginator context."""
        cls = self.__class__
        year = dt.today().year
        url_list = (
            (
                cls.url_profile,
                ('author', cls.user),
                ('year', year),
            ),
            (
                cls.url_group,
                ('group', cls.group),
                ('year', year),
            ),
            (
                cls.url_post,
                ('post', cls.post),
                ('year', year),
            ),
            (
                cls.url_new_post,
                ('edit', False),
                ('year', year),
            ),
            (
                cls.url_post_edit,
                ('edit', True),
                ('year', year),
            ),
        )
        for url, *context in url_list:
            response = cls.authorized_client.get(url)
            for name, value in context:
                with self.subTest(url=url, name=name):
                    self.assertEqual(value, response.context[name])


class PaginatorViewsTest(TestCase, MySetupTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        MySetupTestCase.setUpClass()
        cls.less_ten = 3
        cls.page_count = DELTA_PAGE_COUNT * 2 + cls.less_ten
        cls.posts = tuple(
            Post.objects.create(text=f'Тест {count}', author=cls.user,
                                group=cls.group) for count in
            range(cls.page_count * MAX_PAGE_COUNT + cls.less_ten)
        )

    def test_my_paginator_return_context(self):
        """Check my_paginator function on correct return"""
        pages = self.page_count + 1
        check_context = (
            (
                1,
                2,
                DELTA_PAGE_COUNT + 1,
                MAX_PAGE_COUNT
            ),
            (
                2,
                max(2, 2 - DELTA_PAGE_COUNT),
                2 + DELTA_PAGE_COUNT,
                MAX_PAGE_COUNT
            ),
            (
                3,
                max(2, 3 - DELTA_PAGE_COUNT),
                3 + DELTA_PAGE_COUNT,
                MAX_PAGE_COUNT
            ),
            (
                pages,
                pages - DELTA_PAGE_COUNT,
                pages - 1,
                self.less_ten
            ),
            (
                pages - 1,
                pages - 1 - DELTA_PAGE_COUNT,
                min(pages - 1, pages - 1 + DELTA_PAGE_COUNT),
                MAX_PAGE_COUNT
            ),
            (
                pages - 2,
                pages - 2 - DELTA_PAGE_COUNT,
                min(pages - 1, pages - 2 + DELTA_PAGE_COUNT),
                MAX_PAGE_COUNT
            ),
            (
                pages // 2,
                pages // 2 - DELTA_PAGE_COUNT,
                pages // 2 + DELTA_PAGE_COUNT,
                MAX_PAGE_COUNT
            ),
        )
        for page_number, from_page, to_page, page_count in check_context:
            with self.subTest(page_number=page_number):
                paginator = my_paginator(self.__class__.posts, page_number)
                self.assertEqual(
                    len(paginator.get('page')),
                    page_count
                )
                self.assertEqual(
                    paginator.get('from_page'),
                    from_page
                )
                self.assertEqual(
                    paginator.get('to_page'),
                    to_page
                )

    def test_paginator_in_context(self):
        """ """
        cls = self.__class__
        check_context = (
            cls.url_index,
            cls.url_group,
            cls.url_profile,
        )
        for url in check_context:
            response = cls.authorized_client.get(url)
            with self.subTest(url=url):
                self.assertIn('page', response.context)
                self.assertIn('from_page', response.context)
                self.assertIn('to_page', response.context)