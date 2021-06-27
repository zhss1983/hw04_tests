# hw04_tests

about/tests/test_urls.py

> StaticURLTests

	1) Проверяет отображаются ли страницы (код 200) | test_url_exists_at_desired_location

	2) Проверяет корректные или нет применяются шаблоны | test_url_uses_correct_template

	3) Проверяет соответствие абсолютных и относительных адресов (полученных через name) | test_urls_name_correct



posts/tests/test_forms.py

> class PostsSaveTests

	1) Проверка на то, что форма передаётся в контекст и это правильная форма | test_posts_contain_form

	2) Проверка что зарегистрированный пользователь может сохранить свой пост и после этого будет перенаправлен на корректную страницу | test_auth_user_save_post_and_correct_redirect

	3) Проверка что зарегистрированный пользователь может изменить свой пост и после этого будет перенаправлен на корректную страницу | test_auth_user_edit_post_and_correct_redirect



posts/tests/test_models.py

> class PostModelTest

	1) Проверяет что вернётся при обращении к методу __str__ | test_object_text_field


> class GroupModelTest
	1) Проверяет что вернётся при обращении к методу __str__ | test_object_title_field


posts/tests/test_urls.py

> class PostsURLTests

	1) Соответствие путей абсолютных и полученных по name | test_absolute_url_path_by_name

	2) Наличие страниц с кодом 200 для всех не авторизованных пользователей | test_url_exists_at_desired_location

	3) Наличие страниц с кодом 200 для всех авторизованных пользователей | test_auth_url_exists_at_desired_location

	4) Проверка на автоматический редирект для не авторизованных пользователей на страницу авторизации | test_list_url_redirect_anonymous


posts/tests/test_views.py

> class PostURLTests

	1) Проверка соответствия применяемых шаблонов на страницах, не требующих авторизации | test_url_uses_correct_template_by_guest

	2) Проверка соответствия применяемых шаблонов на страницах, требующих авторизации | test_url_uses_correct_template_auth_user

	3) Проверка что пост созданный в определённой группе доступен только в этой группе и не доступенг в других | test_posts_contain_in_correct_group

	4) Проверка куда происходит перенаправление при попытке изменить пост не автором. | test_wron_user_edit_post

> class PostsContextTests

	1) Проверка, передается ли общий контекст, не относящийся к пагинатору (листовороту) | test_posts_shows_correct_context

> class PaginatorViewsTest
	1) Проверяет что моя функция пагинатор возвращает корректные значения для всех страниц в диапазоне | test_my_paginator_return_context

	2) Проверяет что во все функции, где это необходимо, передаётся контекст из пагинатора | test_paginator_in_context


user/tests/test_urls.py

> class UsersURLTests

	1) проверяет соответствие путей абсолютных и полученных через name | test_absolute_url_path_by_name

	2) Проверяет существование указанной страницы (возвращает код 200) | test_url_exists_at_desired_location


user/tests/test_views.py
> class UsersViewsTests
	1) Проверяет корректность применённых шаблонов | test_url_correct_template_name


yatube/tests/test_urls.py

> class StaticURLTests

	1) Проверка на то что главная страница правильно открывается, возвращает код 200. | test_homepage


posts/tests/test_setups.py

> class MySetupTestCase

Все классы тестов posts/tests наследуют данный класс.

	cls.url_index - URL адрес полученный по 'name'

	Синаксис для всех однотипных: url_<name> = reverse('<name>')

[![CI](https://github.com/yandex-praktikum/hw04_tests/actions/workflows/python-app.yml/badge.svg?branch=master)](https://github.com/yandex-praktikum/hw04_tests/actions/workflows/python-app.yml)
