"""
Playwright — version séquentielle
Commandes enchaînées pour scraper une page dynamique.

Installation :
    pip install playwright
    playwright install chromium
"""

import contextlib
import csv
import json
import time

from playwright.sync_api import sync_playwright

playwright = sync_playwright().start()

# ---------------------------------------------------------------------------
# 1. Ouvrir le navigateur
# ---------------------------------------------------------------------------

browser = playwright.chromium.launch(headless=True)  # False pour voir le navigateur

context = browser.new_context(
    viewport={"width": 1920, "height": 1080},
    user_agent=(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    locale="fr-FR",
)

# Anti-détection : masquer le flag webdriver
context.add_init_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
)

page = context.new_page()

# ---------------------------------------------------------------------------
# 2. Naviguer vers une page
# ---------------------------------------------------------------------------

page.goto("https://example.com")
print(page.title())        # titre de la page
print(page.url)            # URL courante

# Attendre que le réseau soit calme (utile pour les SPA)
page.wait_for_load_state("networkidle")

# ---------------------------------------------------------------------------
# 3. Attendre qu'un élément soit présent
# ---------------------------------------------------------------------------

# Attendre un sélecteur CSS (bloque jusqu'à apparition, timeout 10s par défaut)
page.wait_for_selector(".product")

# Attendre avec un timeout personnalisé (en ms)
page.wait_for_selector(".product", timeout=5000)

# ---------------------------------------------------------------------------
# 4. Trouver des éléments
# ---------------------------------------------------------------------------

# Un seul élément
header = page.query_selector("h1")

# Plusieurs éléments (retourne une liste vide si aucun)
items = page.query_selector_all(".product-card")

# Locators (approche recommandée par Playwright — plus robuste)
header_locator = page.locator("h1")
items_locator = page.locator(".product-card")

# ---------------------------------------------------------------------------
# 5. Extraire le contenu
# ---------------------------------------------------------------------------

# Texte d'un élément
title = header.inner_text()
title_stripped = header.inner_text().strip()

# Attribut HTML
href = page.query_selector("a.cta").get_attribute("href")
src = page.query_selector("img").get_attribute("src")

# Contenu HTML interne
inner_html = header.inner_html()

# Directement depuis un sélecteur (sans passer par query_selector)
title_direct = page.inner_text("h1")
href_direct = page.get_attribute("a.cta", "href")

# Boucle sur plusieurs éléments
data = []
for item in items:
    title = item.query_selector("h2").inner_text().strip()
    price = item.query_selector(".price").inner_text().strip()
    link = item.query_selector("a").get_attribute("href")
    data.append({"title": title, "price": price, "link": link})

print(data)

# ---------------------------------------------------------------------------
# 6. Interagir avec la page
# ---------------------------------------------------------------------------

# Cliquer sur un élément
page.click("button#accept-cookies")

# Remplir un champ texte (efface et remplit)
page.fill("input#search", "python scraping")

# Appuyer sur une touche
page.keyboard.press("Enter")

# Cliquer et taper (sans effacer d'abord)
page.click("input#search")
page.keyboard.type("nouveau texte")

# Sélectionner une option dans un <select>
page.select_option("select#country", "FR")

# Cocher une case
page.check("input[type='checkbox']#terms")

# ---------------------------------------------------------------------------
# 7. Scroller
# ---------------------------------------------------------------------------

# Scroller jusqu'en bas
page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(1.5)

# Scroller vers un élément
page.query_selector(".target-element").scroll_into_view_if_needed()

# Scroll infini
for _ in range(10):
    previous_height = page.evaluate("document.body.scrollHeight")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1.5)
    new_height = page.evaluate("document.body.scrollHeight")
    if new_height == previous_height:
        break

# ---------------------------------------------------------------------------
# 8. Intercepter les requêtes réseau (scraping via l'API interne du site)
# ---------------------------------------------------------------------------

# Capturer les réponses JSON que le site charge en arrière-plan
captured_responses = []

def handle_response(response):
    if "/api/products" in response.url:   # adapter le fragment d'URL
        with contextlib.suppress(Exception):
            captured_responses.append(response.json())

page.on("response", handle_response)
page.reload()
page.wait_for_load_state("networkidle")
page.remove_listener("response", handle_response)

print(captured_responses)

# ---------------------------------------------------------------------------
# 9. Prendre une capture d'écran
# ---------------------------------------------------------------------------

page.screenshot(path="screenshot.png", full_page=True)

# ---------------------------------------------------------------------------
# 10. Changer de page
# ---------------------------------------------------------------------------

# Cliquer sur un lien "page suivante"
next_btn = page.query_selector("a.next")
if next_btn:
    next_btn.click()
    page.wait_for_load_state("domcontentloaded")

# Naviguer directement vers une URL
page.goto("https://example.com/page-2")

# ---------------------------------------------------------------------------
# 11. Fermer le navigateur
# ---------------------------------------------------------------------------

context.close()
browser.close()
playwright.stop()

# ---------------------------------------------------------------------------
# 12. Export CSV
# ---------------------------------------------------------------------------

with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "link"])
    writer.writeheader()
    writer.writerows(data)

# ---------------------------------------------------------------------------
# 13. Export JSON
# ---------------------------------------------------------------------------

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
