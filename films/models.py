from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    year = models.IntegerField()
    genre = models.CharField(max_length=100)
    duration = models.IntegerField(help_text='Czas trwania w minutach')
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name='films', blank=True)

    class Meta:
        ordering = ['-added_at']
        verbose_name = 'Film'
        verbose_name_plural = 'Filmy'

    def __str__(self):
        return f'{self.title} ({self.year})'

    def average_rating(self):
        if hasattr(self, 'avg_rating') and self.avg_rating is not None:
            return round(self.avg_rating, 1)
        ratings = self.ratings.all()
        if not ratings:
            return 0
        return round(sum(r.score for r in ratings) / len(ratings), 1)

    def rating_count(self):
        if hasattr(self, 'ratings_count'):
            return self.ratings_count
        return self.ratings.count()


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='favorites')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'film')
        verbose_name = 'Ulubiony'
        verbose_name_plural = 'Ulubione'

    def __str__(self):
        return f'{self.user.username} - {self.film.title}'


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'film')
        verbose_name = 'Ocena'
        verbose_name_plural = 'Oceny'

    def __str__(self):
        return f'{self.user.username} - {self.film.title}: {self.score}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Komentarz'
        verbose_name_plural = 'Komentarze'

    def __str__(self):
        return f'{self.user.username} - {self.film.title}'


class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watch_history')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='watch_history')
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-watched_at']
        verbose_name = 'Historia oglądania'
        verbose_name_plural = 'Historia oglądania'

    def __str__(self):
        return f'{self.user.username} - {self.film.title}'
