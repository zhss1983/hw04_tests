from http import HTTPStatus

from django.test import TestCase

from .test_setups import MySetupTestCase


class PostsURLTests(TestCase, MySetupTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        MySetupTestCase.setUpClass()

    def test_absolute_url_path_by_name(self):
        """Check absolute url paths."""
        cls = self.__class__
        urls_by_name = (
            (cls.url_index, '/'),
            (cls.url_new_post, '/new/'),
            (cls.url_profile, f'/{cls.user.username}/'),
            (cls.url_post, f'/{cls.user.username}/{cls.post.pk}/'),
            (cls.url_group, f'/group/{cls.group.slug}/'),
            (cls.url_post_edit, f'/{cls.user.username}/{cls.post.pk}/edit/'),
        )
        for name, url in urls_by_name:
            with self.subTest(name=name):
                self.assertEqual(name, url)

    def test_url_exists_at_desired_location(self):
        """Check addres available."""
        cls = self.__class__
        url_list = (
            cls.url_index,
            cls.url_profile,
            cls.url_group,
            cls.url_post,
        )
        for url in url_list:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_auth_url_exists_at_desired_location(self):
        """Check addres available."""
        cls = self.__class__
        auth_url_list = (
            cls.url_new_post,
            cls.url_post_edit,
        )
        for url in auth_url_list:
            response = cls.authorized_client.get(url)
            with self.subTest(url=url):
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_list_url_redirect_anonymous(self):
        """Check redirect for an unauthorized user."""
        cls = self.__class__
        url_list = (
            cls.url_new_post,
            cls.url_post_edit,
        )
        for url in url_list:
            response = self.client.get(url)
            with self.subTest(url=url):
                self.assertRedirects(response, f'/auth/login/?next={url}')
