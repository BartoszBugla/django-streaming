from playwright.sync_api import sync_playwright
import os
import time

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
BASE_URL = 'http://127.0.0.1:8000'

def take_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()

        page.goto(f'{BASE_URL}/')
        page.wait_for_load_state('domcontentloaded')
        time.sleep(1)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, '01_strona_glowna.png'), full_page=True)
        print('Strona glowna - OK')

        page.click('a[href^="/film/"]')
        page.wait_for_load_state('domcontentloaded')
        time.sleep(1)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, '02_szczegoly_filmu.png'), full_page=True)
        print('Szczegoly filmu - OK')

        page.goto(f'{BASE_URL}/szukaj/?q=Matrix')
        page.wait_for_load_state('domcontentloaded')
        time.sleep(1)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, '03_wyszukiwarka.png'), full_page=True)
        print('Wyszukiwarka - OK')

        page.goto(f'{BASE_URL}/konto/logowanie/')
        page.wait_for_load_state('domcontentloaded')
        time.sleep(1)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, '04_logowanie.png'), full_page=True)
        print('Logowanie - OK')

        page.goto(f'{BASE_URL}/konto/rejestracja/')
        page.wait_for_load_state('domcontentloaded')
        time.sleep(1)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, '05_rejestracja.png'), full_page=True)
        print('Rejestracja - OK')

        page.goto(f'{BASE_URL}/konto/logowanie/')
        page.wait_for_load_state('domcontentloaded')
        time.sleep(1)
        page.fill('#username', 'admin')
        page.fill('#password', 'admin123')
        page.click('button[type="submit"]')
        page.wait_for_load_state('domcontentloaded')
        time.sleep(1)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, '06_zalogowany_glowna.png'), full_page=True)
        print('URL po logowaniu: ', page.url)

        page.click('a[href^="/film/"]')
        page.wait_for_load_state('domcontentloaded')
        time.sleep(1)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, '07_szczegoly_zalogowany.png'), full_page=True)
        print('Szczegoly filmu (zalogowany) - OK')

        page.goto(f'{BASE_URL}/ulubione/')
        page.wait_for_load_state('domcontentloaded')
        time.sleep(1)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, '08_ulubione.png'), full_page=True)
        print('Ulubione - OK')

        page.goto(f'{BASE_URL}/historia/')
        page.wait_for_load_state('domcontentloaded')
        time.sleep(1)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, '09_historia.png'), full_page=True)
        print('Historia - OK')

        page.goto(f'{BASE_URL}/konto/profil/')
        page.wait_for_load_state('domcontentloaded')
        time.sleep(1)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, '10_profil.png'), full_page=True)
        print('Profil - OK')

        browser.close()
        print('Wszystkie screenshoty zapisane w screenshots/')

if __name__ == '__main__':
    take_screenshots()
