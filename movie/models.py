import time
from datetime import time
from users.models import Profile

from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone


def movie_directory_path(instance, filename):
    return '{0}/{1}/{2}'.format(instance.__class__.__name__, instance.year, filename)


def actor_directory_path(instance, filename):
    return '{0}/{1}/{2}'.format(instance.__class__.__name__, instance.name[0], filename)


class Ip(models.Model):  # наша таблица где будут айпи адреса
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=150)
    slug = models.SlugField(max_length=150, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(models.Model):
    """Актеры и режиссеры"""
    name = models.CharField("Имя", max_length=300)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to=actor_directory_path)
    slug = models.SlugField(max_length=300, default='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    """Жанры"""
    title = models.CharField("Имя", max_length=100)
    slug = models.SlugField(max_length=100, default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def get_absolute_url(self):
        return reverse('genre_list', kwargs={"slug": self.slug})


class Movie(models.Model):
    """Фильм"""
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='', blank=True)
    description = models.TextField("Описание", blank=True)
    poster = models.ImageField("Постер", upload_to=movie_directory_path, blank=True)
    views = models.ManyToManyField(Ip, related_name="movie_views", blank=True)
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=30, blank=True)
    actors = models.ManyToManyField(Actor, verbose_name="актеры", related_name="actors", blank=True)
    genres = models.ManyToManyField(Genre, verbose_name="жанры", related_name="genres", blank=True)
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
        , blank=True)
    draft = models.BooleanField("Черновик", default=False)
    middle_rating = models.FloatField(default=0)
    file = models.FileField(
        upload_to=movie_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mkv'])],
        blank=True
    )

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"pk": self.pk})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def get_rating(self):
        self.middle_rating = self.ratings.all().aggregate(Sum("star__value"))[
                                 'star__value__sum'] / self.ratings.all().count()
        self.save()

    def get_half_rating(self):
        half = 0
        if self.middle_rating > 0:
            half = float(self.middle_rating) % int(self.middle_rating)
        if 0.3 <= half < 0.7:
            return False
        elif half >= 0.7:
            return True
        else:
            return None

    def get_empty_rating(self):
        a = 5 - int(self.middle_rating + 0.7)
        if a == 0:
            return []
        else:
            return [1, 2, 3, 4, 5][-int(a):]

    def get_full(self):
        return ":" + str(int(self.middle_rating))


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    create_at = models.DateTimeField(default=timezone.now)
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
