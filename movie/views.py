from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin
from .filters import MovieFilter
from .forms import *
from .models import *
from .service import open_file, get_client_ip
from users.models import Profile


class MovieListWithFilters(ListView):
    model = Movie
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = MovieFilter(self.request.GET, queryset=self.get_queryset())
        return context


class MovieList(ListView):
    model = Movie
    queryset = Movie.objects.all()
    template_name = 'movie_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['get_most_rating'] = Movie.objects.all().order_by('-middle_rating')
        context['get_most_popular'] = Movie.objects.all().order_by('-views')
        context['get_most_recent'] = Movie.objects.all().order_by('-year')
        return context


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')
    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        context["star_form"] = RatingForm()
        return context


class GenreListView(SingleObjectMixin, ListView):
    template_name = 'genre_list.html'


    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Genre.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = self.object
        context['filter'] = MovieFilter(self.request.GET, queryset=self.get_queryset())

        return context

    def get_queryset(self):
        return self.object.genres.all()


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))})
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class CreateReview(CreateView):
    form_class = ReviewForm
    model = Reviews

    def form_valid(self, form):
        form.instance.movie_id = self.kwargs.get('pk')
        form.instance.profile = Profile.objects.get(id=self.request.POST.get("profile"))
        if self.request.POST.get("parent", None):
            form.instance.parent_id = int(self.request.POST.get("parent"))
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.movie.get_absolute_url()
