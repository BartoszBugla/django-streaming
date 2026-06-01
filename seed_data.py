import os
import django
import urllib.request
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'streaming.settings')
django.setup()

from films.models import Film, Category, Favorite, Rating, Comment, WatchHistory
from django.contrib.auth.models import User

# Plakaty z bazy TMDB dla filmów
POSTER_URLS = {
    'incepcja.jpg': 'https://image.tmdb.org/t/p/w500/ljsZTbVsrQSqZgWeep2B1QiDKuh.jpg',
    'mroczny_rycerz.jpg': 'https://image.tmdb.org/t/p/w500/1hRoyzDtpgMU7Dz4JF22RANzQO7.jpg',
    'skazani_na_shawshank.jpg': 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
    'matrix.jpg': 'https://image.tmdb.org/t/p/w500/oMsxZEvz9a708d49b6UdZK1KAo5.jpg',
    'forrest_gump.jpg': 'https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg',
}

def download_and_compress_poster(url, filename):
    posters_dir = os.path.join('media', 'posters')
    os.makedirs(posters_dir, exist_ok=True)
    filepath = os.path.join(posters_dir, filename)
    
    if os.path.exists(filepath):
        print(f" -> Plakat {filename} już jest pobrany. Pomijam.")
        return f"posters/{filename}"
        
    try:
        print(f"Pobieranie plakatu: {filename}...")
        temp_filepath = filepath + '.tmp'
        
        # Nagłówek User-Agent żeby nas nie zablokowało (błąd 403)
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response, open(temp_filepath, 'wb') as out_file:
            out_file.write(response.read())
        
        # Zapis i kompresja za pomocą Pillow do JPG
        with Image.open(temp_filepath) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            # Lżejszy plik (80% jakości)
            img.save(filepath, "JPEG", quality=80, optimize=True)
            
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
            
        size_kb = os.path.getsize(filepath) // 1024
        print(f" -> Zapisano: {filepath} ({size_kb} KB)")
        return f"posters/{filename}"
    except Exception as e:
        print(f" -> Błąd pobierania {filename}: {e}")
        return None

print("Pobieranie plakatów...")
posters = {}
for filename, url in POSTER_URLS.items():
    posters[filename] = download_and_compress_poster(url, filename)

print("Kategorie...")
cat_action, _ = Category.objects.get_or_create(name='Akcja')
cat_drama, _ = Category.objects.get_or_create(name='Dramat')
cat_scifi, _ = Category.objects.get_or_create(name='Sci-Fi')
cat_comedy, _ = Category.objects.get_or_create(name='Komedia')

print("Tworzenie filmów...")
f1, created = Film.objects.get_or_create(
    title='Incepcja',
    defaults={
        'description': 'Złodziej, który kradnie sekrety korporacyjne za pomocą technologii dzielenia snów, dostaje odwrotne zadanie - zaszczepienie idei w umyśle prezesa firmy.',
        'year': 2010,
        'genre': 'Sci-Fi',
        'duration': 148,
        'poster': posters.get('incepcja.jpg'),
    }
)
if created:
    f1.categories.add(cat_scifi, cat_action)

f2, created = Film.objects.get_or_create(
    title='Mroczny Rycerz',
    defaults={
        'description': 'Batman musi zaakceptować jedną z największych prób psychologicznych i fizycznych, aby walczyć z niesprawiedliwością w Gotham City.',
        'year': 2008,
        'genre': 'Akcja',
        'duration': 152,
        'poster': posters.get('mroczny_rycerz.jpg'),
    }
)
if created:
    f2.categories.add(cat_action, cat_drama)

f3, created = Film.objects.get_or_create(
    title='Skazani na Shawshank',
    defaults={
        'description': 'Dwóch uwięzionych mężczyzn łączy się przez lata, znajdując pocieszenie i odkupienie poprzez akty zwykłej przyzwoitości.',
        'year': 1994,
        'genre': 'Dramat',
        'duration': 142,
        'poster': posters.get('skazani_na_shawshank.jpg'),
    }
)
if created:
    f3.categories.add(cat_drama)

f4, created = Film.objects.get_or_create(
    title='Matrix',
    defaults={
        'description': 'Haker komputerowy dowiaduje się od tajemniczych buntowników o prawdziwej naturze swojej rzeczywistości i o swojej roli w wojnie z jej kontrolerami.',
        'year': 1999,
        'genre': 'Sci-Fi',
        'duration': 136,
        'poster': posters.get('matrix.jpg'),
    }
)
if created:
    f4.categories.add(cat_scifi, cat_action)

f5, created = Film.objects.get_or_create(
    title='Forrest Gump',
    defaults={
        'description': 'Prezydentury Kennedy\'ego i Johnsona, wojna w Wietnamie, afera Watergate i inne wydarzenia historyczne rozwijają się z perspektywy człowieka z Alabamy o IQ 75.',
        'year': 1994,
        'genre': 'Dramat',
        'duration': 142,
        'poster': posters.get('forrest_gump.jpg'),
    }
)
if created:
    f5.categories.add(cat_drama, cat_comedy)

print(f'\nDodano/zweryfikowano {Film.objects.count()} filmów i {Category.objects.count()} kategorii.')

print("Użytkownicy...")
users_data = [
    {'username': 'jan_kowalski', 'email': 'jan@example.com', 'password': 'testpassword123', 'first_name': 'Jan', 'last_name': 'Kowalski'},
    {'username': 'anna_nowak', 'email': 'anna@example.com', 'password': 'testpassword123', 'first_name': 'Anna', 'last_name': 'Nowak'},
    {'username': 'filmomaniak', 'email': 'filmomaniak@example.com', 'password': 'testpassword123', 'first_name': 'Michał', 'last_name': 'Zieliński'},
    {'username': 'kino_widz', 'email': 'kinowidz@example.com', 'password': 'testpassword123', 'first_name': 'Katarzyna', 'last_name': 'Wójcik'},
]

users = {}
for u_data in users_data:
    user, created = User.objects.get_or_create(
        username=u_data['username'],
        defaults={
            'email': u_data['email'],
            'first_name': u_data['first_name'],
            'last_name': u_data['last_name'],
        }
    )
    if created:
        user.set_password(u_data['password'])
        user.save()
        print(f" -> Dodano użytkownika: {user.username}")
    else:
        print(f" -> Użytkownik {user.username} już istnieje.")
    users[user.username] = user

print("Oceny...")
ratings_data = [
    # Incepcja
    ('jan_kowalski', 'Incepcja', 9),
    ('anna_nowak', 'Incepcja', 10),
    ('filmomaniak', 'Incepcja', 9),
    ('kino_widz', 'Incepcja', 8),
    
    # Mroczny Rycerz
    ('jan_kowalski', 'Mroczny Rycerz', 10),
    ('anna_nowak', 'Mroczny Rycerz', 9),
    ('filmomaniak', 'Mroczny Rycerz', 10),
    
    # Skazani na Shawshank
    ('jan_kowalski', 'Skazani na Shawshank', 10),
    ('kino_widz', 'Skazani na Shawshank', 10),
    
    # Matrix
    ('filmomaniak', 'Matrix', 9),
    ('kino_widz', 'Matrix', 8),
    ('anna_nowak', 'Matrix', 10),
    
    # Forrest Gump
    ('jan_kowalski', 'Forrest Gump', 9),
    ('anna_nowak', 'Forrest Gump', 9),
    ('kino_widz', 'Forrest Gump', 9),
]

for username, film_title, score in ratings_data:
    user = users.get(username)
    try:
        film = Film.objects.get(title=film_title)
        rating, created = Rating.objects.get_or_create(
            user=user,
            film=film,
            defaults={'score': score}
        )
        if created:
            print(f" -> {username} ocenił '{film_title}' na {score}")
    except Film.DoesNotExist:
        pass

print("Komentarze...")
comments_data = [
    ('jan_kowalski', 'Incepcja', 'Niesamowity film! Christopher Nolan to geniusz, pomysł ze snem wewnątrz snu wgniata w fotel.'),
    ('anna_nowak', 'Incepcja', 'Jeden z moich ulubionych filmów. Muzyka Hansa Zimmera buduje genialne napięcie.'),
    ('filmomaniak', 'Incepcja', 'Świetna gra aktorska Leonardo DiCaprio. Końcówka z bączkiem do dzisiaj pozostawia pole do dyskusji.'),
    
    ('jan_kowalski', 'Mroczny Rycerz', 'Najlepsza rola Jokera w historii kina. Heath Ledger zasłużył na tego Oscara jak nikt inny.'),
    ('filmomaniak', 'Mroczny Rycerz', 'Ten film zrewolucjonizował kino o superbohaterach. Mroczny, dojrzały i trzymający w napięciu do ostatniej sekundy.'),
    
    ('kino_widz', 'Skazani na Shawshank', 'Piękna historia o nadziei i przyjaźni. Klasyka kina, którą każdy musi zobaczyć przynajmniej raz w życiu.'),
    
    ('filmomaniak', 'Matrix', 'Kamień milowy w efektach specjalnych. Słynny bullet time robi wrażenie nawet po tylu latach. I ta zielona estetyka!'),
    ('anna_nowak', 'Matrix', 'Wspaniała fabuła dająca do myślenia o otaczającej nas rzeczywistości. Keanu Reeves idealnie pasuje do roli Neo.'),
    
    ('kino_widz', 'Forrest Gump', 'Film, który bawi i wzrusza do łez. Tom Hanks w swojej życiowej formie. Życie jest jak pudełko czekoladek!'),
]

for username, film_title, content in comments_data:
    user = users.get(username)
    try:
        film = Film.objects.get(title=film_title)
        comment, created = Comment.objects.get_or_create(
            user=user,
            film=film,
            content=content
        )
        if created:
            print(f" -> Dodano komentarz od {username} do '{film_title}'")
    except Film.DoesNotExist:
        pass

print("Ulubione...")
favorites_data = [
    ('jan_kowalski', 'Incepcja'),
    ('jan_kowalski', 'Mroczny Rycerz'),
    ('anna_nowak', 'Incepcja'),
    ('anna_nowak', 'Matrix'),
    ('filmomaniak', 'Mroczny Rycerz'),
    ('filmomaniak', 'Matrix'),
    ('kino_widz', 'Skazani na Shawshank'),
    ('kino_widz', 'Forrest Gump'),
]

for username, film_title in favorites_data:
    user = users.get(username)
    try:
        film = Film.objects.get(title=film_title)
        fav, created = Favorite.objects.get_or_create(user=user, film=film)
        if created:
            print(f" -> Dodano '{film_title}' do ulubionych u {username}")
    except Film.DoesNotExist:
        pass

print("Historia oglądania...")
watch_history_data = [
    ('jan_kowalski', 'Incepcja'),
    ('jan_kowalski', 'Mroczny Rycerz'),
    ('jan_kowalski', 'Forrest Gump'),
    ('anna_nowak', 'Incepcja'),
    ('anna_nowak', 'Matrix'),
    ('filmomaniak', 'Incepcja'),
    ('filmomaniak', 'Mroczny Rycerz'),
    ('filmomaniak', 'Matrix'),
    ('kino_widz', 'Skazani na Shawshank'),
    ('kino_widz', 'Forrest Gump'),
    ('kino_widz', 'Incepcja'),
]

for username, film_title in watch_history_data:
    user = users.get(username)
    try:
        film = Film.objects.get(title=film_title)
        if not WatchHistory.objects.filter(user=user, film=film).exists():
            WatchHistory.objects.create(user=user, film=film)
            print(f" -> Zapisano w historii: {username} obejrzał '{film_title}'")
    except Film.DoesNotExist:
        pass

print(f'\nGotowe! Baza danych została zasilona. Użytkownicy: {User.objects.count()}, Komentarze: {Comment.objects.count()}, Oceny: {Rating.objects.count()}')


