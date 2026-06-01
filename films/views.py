from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q, Avg, Count
from .models import Film, Favorite, Rating, Comment, WatchHistory, Category
from .forms import CommentForm, RatingForm, SearchForm


def home(request):
    latest_films = Film.objects.annotate(
        avg_rating=Avg('ratings__score'),
        ratings_count=Count('ratings')
    )[:8]
    all_films = Film.objects.all()
    categories = Category.objects.all()
    search_form = SearchForm()
    return render(request, 'home.html', {
        'latest_films': latest_films,
        'all_films': all_films,
        'categories': categories,
        'search_form': search_form,
    })


def film_detail(request, pk):
    film = get_object_or_404(Film, pk=pk)
    comments = film.comments.select_related('user').all()
    comment_form = CommentForm()
    rating_form = RatingForm()
    user_rating = None
    is_favorite = False

    if request.user.is_authenticated:
        last_view = WatchHistory.objects.filter(user=request.user).first()
        if not last_view or last_view.film != film:
            WatchHistory.objects.create(user=request.user, film=film)
        user_rating = Rating.objects.filter(user=request.user, film=film).first()
        is_favorite = Favorite.objects.filter(user=request.user, film=film).exists()

    return render(request, 'films/film_detail.html', {
        'film': film,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'user_rating': user_rating,
        'is_favorite': is_favorite,
    })


def search(request):
    form = SearchForm(request.GET)
    results = Film.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get('q')
        genre = form.cleaned_data.get('genre')

        if q:
            results = results.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )
        if genre:
            results = results.filter(genre__icontains=genre)

    return render(request, 'films/search_results.html', {
        'form': form,
        'results': results,
    })


@login_required
@require_POST
def toggle_favorite(request, pk):
    film = get_object_or_404(Film, pk=pk)
    favorite = Favorite.objects.filter(user=request.user, film=film)

    if favorite.exists():
        favorite.delete()
    else:
        Favorite.objects.create(user=request.user, film=film)

    return redirect('film_detail', pk=pk)


@login_required
def add_rating(request, pk):
    film = get_object_or_404(Film, pk=pk)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data['score']
            Rating.objects.update_or_create(
                user=request.user,
                film=film,
                defaults={'score': score}
            )

    return redirect('film_detail', pk=pk)


@login_required
def add_comment(request, pk):
    film = get_object_or_404(Film, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.film = film
            comment.save()

    return redirect('film_detail', pk=pk)


@login_required
@require_POST
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    film_pk = comment.film.pk
    comment.delete()
    return redirect('film_detail', pk=film_pk)


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('film')
    return render(request, 'films/favorites.html', {
        'favorites': favorites,
    })


@login_required
def watch_history(request):
    history = WatchHistory.objects.filter(user=request.user).select_related('film')
    return render(request, 'films/watch_history.html', {
        'history': history,
    })
