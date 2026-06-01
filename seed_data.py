import os
import django
import urllib.request
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'streaming.settings')
django.setup()

from films.models import Film, Category

# Słownik z prawdziwymi plakatami z bazy TMDB
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
    
    try:
        print(f"Pobieranie plakatu do: {filename}...")
        temp_filepath = filepath + '.tmp'
        
        # Pobranie nagłówków User-Agent, aby uniknąć ewentualnego blokowania (403)
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response, open(temp_filepath, 'wb') as out_file:
            out_file.write(response.read())
        
        # Otwarcie pliku przez Pillow i kompresja do JPEG
        with Image.open(temp_filepath) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            # Kompresujemy z jakością 80% dla szybszego ładowania
            img.save(filepath, "JPEG", quality=80, optimize=True)
            
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
            
        size_kb = os.path.getsize(filepath) // 1024
        print(f" -> Zapisano i skompresowano: {filepath} ({size_kb} KB)")
        return f"posters/{filename}"
    except Exception as e:
        print(f" -> Błąd pobierania {filename}: {e}")
        return None

print("Czyszczenie bazy danych...")
Film.objects.all().delete()
Category.objects.all().delete()

print("\nPobieranie plakatów filmowych...")
posters = {}
for filename, url in POSTER_URLS.items():
    posters[filename] = download_and_compress_poster(url, filename)

print("\nTworzenie kategorii...")
cat_action = Category.objects.create(name='Akcja')
cat_drama = Category.objects.create(name='Dramat')
cat_scifi = Category.objects.create(name='Sci-Fi')
cat_comedy = Category.objects.create(name='Komedia')

print("Tworzenie filmów...")
f1 = Film.objects.create(
    title='Incepcja',
    description='Złodziej, który kradnie sekrety korporacyjne za pomocą technologii dzielenia snów, dostaje odwrotne zadanie - zaszczepienie idei w umyśle prezesa firmy.',
    year=2010,
    genre='Sci-Fi',
    duration=148,
    poster=posters.get('incepcja.jpg'),
)
f1.categories.add(cat_scifi, cat_action)

f2 = Film.objects.create(
    title='Mroczny Rycerz',
    description='Batman musi zaakceptować jedną z największych prób psychologicznych i fizycznych, aby walczyć z niesprawiedliwością w Gotham City.',
    year=2008,
    genre='Akcja',
    duration=152,
    poster=posters.get('mroczny_rycerz.jpg'),
)
f2.categories.add(cat_action, cat_drama)

f3 = Film.objects.create(
    title='Skazani na Shawshank',
    description='Dwóch uwięzionych mężczyzn łączy się przez lata, znajdując pocieszenie i odkupienie poprzez akty zwykłej przyzwoitości.',
    year=1994,
    genre='Dramat',
    duration=142,
    poster=posters.get('skazani_na_shawshank.jpg'),
)
f3.categories.add(cat_drama)

f4 = Film.objects.create(
    title='Matrix',
    description='Haker komputerowy dowiaduje się od tajemniczych buntowników o prawdziwej naturze swojej rzeczywistości i o swojej roli w wojnie z jej kontrolerami.',
    year=1999,
    genre='Sci-Fi',
    duration=136,
    poster=posters.get('matrix.jpg'),
)
f4.categories.add(cat_scifi, cat_action)

f5 = Film.objects.create(
    title='Forrest Gump',
    description='Prezydentury Kennedy\'ego i Johnsona, wojna w Wietnamie, afera Watergate i inne wydarzenia historyczne rozwijają się z perspektywy człowieka z Alabamy o IQ 75.',
    year=1994,
    genre='Dramat',
    duration=142,
    poster=posters.get('forrest_gump.jpg'),
)
f5.categories.add(cat_drama, cat_comedy)

print(f'\nSukces! Dodano {Film.objects.count()} filmów i {Category.objects.count()} kategorii w bazie danych.')

