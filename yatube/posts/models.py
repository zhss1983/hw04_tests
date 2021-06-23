from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Имя группы',
        help_text=('Название тематической группы. Обязательно к заполнению. '
                   'Применяется для автоматического заполнения slug адреса')
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес группы',
        help_text=('Адрес по которому можно будет обратиться и посмотреть '
                   'записи в группе. Можно не выбирать. Есть автозаполнение.')

    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Тема групп. Можно не выбирать.',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('title', 'slug')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст вашего поста.',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='posts',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Группа',
        related_name='posts',
        help_text=('Тематическая группа. Группы создают администраторы. '
                   'Можно не выбирать.')
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]