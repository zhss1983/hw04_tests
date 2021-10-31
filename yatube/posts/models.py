from PIL import Image

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Q
from django.utils.safestring import mark_safe

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Имя группы',
        help_text=mark_safe('Название тематической группы. Обязательно к '
                            'заполнению.<Br>Применяется для автоматического '
                            'заполнения slug адреса')
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес группы',
        help_text=mark_safe('Адрес по которому можно будет обратиться и '
                            'посмотреть записи в группе.<Br>Можно не '
                            'выбирать, есть автозаполнение.')

    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text=mark_safe('Тема групп.<br>Можно не выбирать.'),
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('title',)

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
        help_text=mark_safe('Тематическая группа. Группы создают '
                            'администраторы.<br>Можно не выбирать.')
    )
    image = models.ImageField(
        upload_to='posts/',
        verbose_name='Изображение',
        blank=True,
        null=True,
        help_text=('Загрузите изображение. Оптимальный размер 960x339. '
                   'Допускаются 1920x678, 640x226, 480x170 px.'),
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.text[:15]

    def delete(self, *args, **kwargs):
        self.image.delete()
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        image = self.image
        if not image:
            return super().save(*args, **kwargs)
        img = Image.open(image)
        if img.width < settings.MIN_WIDTH:
            raise Exception(
                   (f'Ширина изображения меньше {settings.MIN_WIDTH} px, '
                 f'загрузите изображение по меньшей мере {settings.MIN_WIDTH}x'
                 f'{settings.MIN_HEIGHT} px.'),
            )
        if img.height < settings.MIN_HEIGHT:
            raise Exception(
                (f'Высота изображения меньше {settings.MIN_HEIGHT} px, '
                 f'загрузите изображение по меньшей мере {settings.MIN_WIDTH}x'
                 f'{settings.MIN_HEIGHT} px.'),
            )
        return super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст вашего комментария.',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('user__username', 'author__username')
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_user_author',
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='name_not_author',
            )
        )
