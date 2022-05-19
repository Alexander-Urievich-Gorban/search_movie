
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [

    path("", views.MovieList.as_view(), name="movie_list"),
    path("add-review/<int:pk>/", views.CreateReview.as_view(), name='add_review'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("list/", views.MovieListWithFilters.as_view(), name='list'),
    path("movie_detail/<int:pk>",views.MovieDetailView.as_view(),name="movie_detail"),
    path("genre_list/<slug:slug>",views.GenreListView.as_view(),name="genre_list"),
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),
]
