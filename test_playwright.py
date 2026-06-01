from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://127.0.0.1:8000/')
    elements = page.query_selector_all('a')
    for el in elements:
        print(el.get_attribute('href'))
    browser.close()
