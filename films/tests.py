from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Film, Category, Favorite, Rating, Comment, WatchHistory


class FilmModelTest(TestCase):

    def setUp(self):
        self.film = Film.objects.create(
            title='Test Film',
            description='Opis testowy',
            year=2020,
            genre='Dramat',
            duration=120,
        )
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_film_str(self):
        self.assertEqual(str(self.film), 'Test Film (2020)')

    def test_average_rating_empty(self):
        self.assertEqual(self.film.average_rating(), 0)

    def test_average_rating_with_scores(self):
        user2 = User.objects.create_user(username='user2', password='testpass123')
        Rating.objects.create(user=self.user, film=self.film, score=8)
        Rating.objects.create(user=user2, film=self.film, score=6)
        self.assertEqual(self.film.average_rating(), 7.0)

    def test_rating_count(self):
        Rating.objects.create(user=self.user, film=self.film, score=5)
        self.assertEqual(self.film.rating_count(), 1)

    def test_category_relation(self):
        cat = Category.objects.create(name='Akcja')
        self.film.categories.add(cat)
        self.assertIn(cat, self.film.categories.all())
        self.assertIn(self.film, cat.films.all())


class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.film = Film.objects.create(
            title='Testowy Film',
            description='Opis',
            year=2023,
            genre='Akcja',
            duration=90,
        )

    def test_home_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_contains_film(self):
        response = self.client.get('/')
        self.assertContains(response, 'Testowy Film')

    def test_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class FilmDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.film = Film.objects.create(
            title='Detail Film',
            description='Pelny opis filmu',
            year=2021,
            genre='Sci-Fi',
            duration=130,
        )

    def test_detail_status(self):
        response = self.client.get(f'/film/{self.film.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_detail_contains_title(self):
        response = self.client.get(f'/film/{self.film.pk}/')
        self.assertContains(response, 'Detail Film')

    def test_detail_contains_description(self):
        response = self.client.get(f'/film/{self.film.pk}/')
        self.assertContains(response, 'Pelny opis filmu')

    def test_detail_creates_watch_history(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.get(f'/film/{self.film.pk}/')
        self.assertTrue(WatchHistory.objects.filter(user=self.user, film=self.film).exists())

    def test_detail_prevents_duplicate_watch_history(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.get(f'/film/{self.film.pk}/')
        self.assertEqual(WatchHistory.objects.filter(user=self.user, film=self.film).count(), 1)
        self.client.get(f'/film/{self.film.pk}/')
        self.assertEqual(WatchHistory.objects.filter(user=self.user, film=self.film).count(), 1)

    def test_detail_no_history_for_anonymous(self):
        self.client.get(f'/film/{self.film.pk}/')
        self.assertEqual(WatchHistory.objects.count(), 0)

    def test_detail_404_for_nonexistent(self):
        response = self.client.get('/film/9999/')
        self.assertEqual(response.status_code, 404)


class SearchViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        Film.objects.create(title='Matrix', description='Opis', year=1999, genre='Sci-Fi', duration=136)
        Film.objects.create(title='Incepcja', description='Opis', year=2010, genre='Sci-Fi', duration=148)
        Film.objects.create(title='Shawshank', description='Opis', year=1994, genre='Dramat', duration=142)

    def test_search_by_title(self):
        response = self.client.get('/szukaj/', {'q': 'Matrix'})
        self.assertContains(response, 'Matrix')
        self.assertNotContains(response, 'Shawshank')

    def test_search_by_genre(self):
        response = self.client.get('/szukaj/', {'genre': 'Sci-Fi'})
        self.assertContains(response, 'Matrix')
        self.assertContains(response, 'Incepcja')
        self.assertNotContains(response, 'Shawshank')

    def test_search_empty_query(self):
        response = self.client.get('/szukaj/')
        self.assertEqual(response.status_code, 200)


class FavoriteViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.film = Film.objects.create(
            title='Fav Film', description='Opis', year=2020, genre='Akcja', duration=100
        )

    def test_toggle_favorite_requires_login(self):
        response = self.client.post(f'/film/{self.film.pk}/ulubione/')
        self.assertEqual(response.status_code, 302)

    def test_add_favorite(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.post(f'/film/{self.film.pk}/ulubione/')
        self.assertTrue(Favorite.objects.filter(user=self.user, film=self.film).exists())

    def test_remove_favorite(self):
        self.client.login(username='testuser', password='testpass123')
        Favorite.objects.create(user=self.user, film=self.film)
        self.client.post(f'/film/{self.film.pk}/ulubione/')
        self.assertFalse(Favorite.objects.filter(user=self.user, film=self.film).exists())

    def test_favorites_list(self):
        self.client.login(username='testuser', password='testpass123')
        Favorite.objects.create(user=self.user, film=self.film)
        response = self.client.get('/ulubione/')
        self.assertContains(response, 'Fav Film')

    def test_toggle_favorite_rejects_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(f'/film/{self.film.pk}/ulubione/')
        self.assertEqual(response.status_code, 405)


class RatingViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.film = Film.objects.create(
            title='Rated Film', description='Opis', year=2022, genre='Dramat', duration=110
        )

    def test_add_rating(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.post(f'/film/{self.film.pk}/ocen/', {'score': 8})
        rating = Rating.objects.get(user=self.user, film=self.film)
        self.assertEqual(rating.score, 8)

    def test_update_rating(self):
        self.client.login(username='testuser', password='testpass123')
        Rating.objects.create(user=self.user, film=self.film, score=5)
        self.client.post(f'/film/{self.film.pk}/ocen/', {'score': 9})
        rating = Rating.objects.get(user=self.user, film=self.film)
        self.assertEqual(rating.score, 9)

    def test_invalid_rating(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.post(f'/film/{self.film.pk}/ocen/', {'score': 15})
        self.assertFalse(Rating.objects.filter(user=self.user, film=self.film).exists())

    def test_rating_requires_login(self):
        response = self.client.post(f'/film/{self.film.pk}/ocen/', {'score': 7})
        self.assertEqual(response.status_code, 302)


class CommentViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.film = Film.objects.create(
            title='Comment Film', description='Opis', year=2023, genre='Komedia', duration=95
        )

    def test_add_comment(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.post(f'/film/{self.film.pk}/komentarz/', {'content': 'Swietny film!'})
        self.assertTrue(Comment.objects.filter(user=self.user, film=self.film).exists())

    def test_delete_own_comment(self):
        self.client.login(username='testuser', password='testpass123')
        comment = Comment.objects.create(user=self.user, film=self.film, content='Do usuniecia')
        self.client.post(f'/komentarz/{comment.pk}/usun/')
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_cannot_delete_other_user_comment(self):
        other_user = User.objects.create_user(username='other', password='testpass123')
        comment = Comment.objects.create(user=other_user, film=self.film, content='Nie moj')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(f'/komentarz/{comment.pk}/usun/')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Comment.objects.filter(pk=comment.pk).exists())

    def test_comment_requires_login(self):
        response = self.client.post(f'/film/{self.film.pk}/komentarz/', {'content': 'Test'})
        self.assertEqual(response.status_code, 302)

    def test_delete_comment_rejects_get(self):
        self.client.login(username='testuser', password='testpass123')
        comment = Comment.objects.create(user=self.user, film=self.film, content='Do usuniecia')
        response = self.client.get(f'/komentarz/{comment.pk}/usun/')
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Comment.objects.filter(pk=comment.pk).exists())


class WatchHistoryViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.film = Film.objects.create(
            title='History Film', description='Opis', year=2021, genre='Akcja', duration=100
        )

    def test_watch_history_page(self):
        self.client.login(username='testuser', password='testpass123')
        WatchHistory.objects.create(user=self.user, film=self.film)
        response = self.client.get('/historia/')
        self.assertContains(response, 'History Film')

    def test_watch_history_requires_login(self):
        response = self.client.get('/historia/')
        self.assertEqual(response.status_code, 302)


class AccountsViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_page(self):
        response = self.client.get('/konto/rejestracja/')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get('/konto/logowanie/')
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        response = self.client.post('/konto/rejestracja/', {
            'username': 'newuser',
            'email': 'new@test.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_user(self):
        User.objects.create_user(username='logintest', password='testpass123')
        response = self.client.post('/konto/logowanie/', {
            'username': 'logintest',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_invalid(self):
        response = self.client.post('/konto/logowanie/', {
            'username': 'notexist',
            'password': 'wrong',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nieprawidlowa')

    def test_logout(self):
        User.objects.create_user(username='logouttest', password='testpass123')
        self.client.login(username='logouttest', password='testpass123')
        response = self.client.get('/konto/wyloguj/')
        self.assertEqual(response.status_code, 302)

    def test_profile_edit(self):
        User.objects.create_user(username='profiletest', password='testpass123')
        self.client.login(username='profiletest', password='testpass123')
        response = self.client.get('/konto/profil/')
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        user = User.objects.create_user(username='profiletest2', password='testpass123')
        self.client.login(username='profiletest2', password='testpass123')
        self.client.post('/konto/profil/', {
            'username': 'profiletest2',
            'email': 'updated@test.com',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
        })
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Jan')
        self.assertEqual(user.email, 'updated@test.com')
