import django_filters as filter
from django import forms
from .models import Movie, Genre, Actor


class MovieFilter(filter.FilterSet):
    genres = filter.MultipleChoiceFilter(field_name='title', choices=[
        (genre.title, genre) for genre in Genre.objects.all()], method='filter_by_genres')
    actors = filter.MultipleChoiceFilter(field_name='name', choices=[
        (actor.name, actor) for actor in Actor.objects.all()], method='filter_by_actors')
    year = filter.RangeFilter()
    middle_rating = filter.RangeFilter()

    CHOICES = (
        ('popular', 'По популярности'),
        ('rating', 'По рейтингу'),
        ('realise', 'По новизне'),
    )


    main_ordering = filter.ChoiceFilter(choices=CHOICES,
                                                method='filter_by_order')


    def filter_by_genres(self, queryset, name, values):
        return queryset.filter(genres__title__in=values)

    def filter_by_actors(self, queryset, name, values):
        return queryset.filter(actors__name__in=values)

    def filter_by_order(self, queryset, name, value):
        if value == 'realise':
            return queryset.order_by('-year')
        elif value == 'popular':
            return queryset.order_by('-views')
        else:
            return queryset.order_by('-middle_rating')

    class Meta:
        model = Movie
        fields = ['year','middle_rating' ]

