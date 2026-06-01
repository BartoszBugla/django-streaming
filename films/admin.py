from django.contrib import admin
from .models import Category, Film, Favorite, Rating, Comment, WatchHistory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'genre', 'duration', 'added_at')
    list_filter = ('genre', 'year', 'categories')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'film', 'added_at')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'film', 'score', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'film', 'created_at')
    list_filter = ('created_at',)


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'film', 'watched_at')
