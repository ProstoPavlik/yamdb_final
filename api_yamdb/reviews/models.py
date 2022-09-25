from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='Категория',
        db_index=True
    )
    slug = models.SlugField(max_length=50, unique=True, verbose_name='url')

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=250, verbose_name='Жанр', db_index=True)
    slug = models.SlugField(max_length=50, unique=True, verbose_name='url')

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=250, verbose_name='Произведение')
    year = models.PositiveSmallIntegerField(verbose_name='Год')
    description = models.TextField(max_length=250, null=True,
                                   blank=True, verbose_name='Описание')
    genre = models.ManyToManyField(
        Genres,
        through='GenresTitle',
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name


class GenresTitle(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.genre} {self.title}'


class Review(models.Model):
    text = models.TextField(verbose_name='Текст комментария',
                            blank=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор')
    score = models.PositiveSmallIntegerField(
        choices=list(zip(range(1, 11), range(1, 11)))
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Cсылка на произведение')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['author']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_review'
            )
        ]

    def __str__(self) -> str:
        return f'{self.author} {self.text}'


class Comments(models.Model):
    text = models.TextField(verbose_name='Текст комментария',
                            blank=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Cсылка на отзыв')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['author']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return f'{self.author} {self.text}'
