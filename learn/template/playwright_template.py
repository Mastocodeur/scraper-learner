"""
Template Playwright (synchrone)
Scraping de pages dynamiques — alternative moderne à Selenium.
Plus rapide, API plus claire, meilleur support des pages SPA.

Installation :
    pip install playwright
    playwright install chromium
"""

import contextlib
import csv
import json
import time

from playwright.sync_api import Browser, Page, sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeout

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

URL = "https://example.com"

HEADLESS = True           # False pour voir le navigateur
TIMEOUT = 10_000          # millisecondes (Playwright utilise des ms)
DELAY_BETWEEN_PAGES = 2   # secondes


# ---------------------------------------------------------------------------
# Initialisation du navigateur
# ---------------------------------------------------------------------------

def build_browser_context(playwright):
    """Configure et retourne un contexte de navigation avec anti-détection basique."""
    browser: Browser = playwright.chromium.launch(headless=HEADLESS)

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

    return browser, context


# ---------------------------------------------------------------------------
# Authentification (optionnel)
# ---------------------------------------------------------------------------

def login(page: Page, login_url: str, username: str, password: str) -> None:
    """Se connecte à un site via un formulaire. À adapter selon le site."""
    page.goto(login_url)

    page.fill("#username", username)    # adapter le sélecteur
    page.fill("#password", password)
    page.click("button[type='submit']")

    # Attendre que la connexion soit effective (adapter le sélecteur)
    page.wait_for_selector(".dashboard, .home", timeout=TIMEOUT)
    print("Connexion réussie")


# ---------------------------------------------------------------------------
# Extraction des données
# ---------------------------------------------------------------------------

def extract_data(page: Page) -> list[dict]:
    """Extrait les données depuis la page courante. À adapter selon le site."""
    results = []

    try:
        page.wait_for_selector(".item-class", timeout=TIMEOUT)  # adapter le sélecteur
    except PlaywrightTimeout:
        print("Aucun élément trouvé sur cette page")
        return results

    items = page.query_selector_all(".item-class")

    for item in items:
        try:
            title_el = item.query_selector("h2")
            desc_el = item.query_selector("p")
            link_el = item.query_selector("a")

            results.append({
                "title": title_el.inner_text().strip() if title_el else None,
                "description": desc_el.inner_text().strip() if desc_el else None,
                "link": link_el.get_attribute("href") if link_el else None,
            })
        except Exception:
            continue

    return results


# ---------------------------------------------------------------------------
# Intercepter les requêtes réseau (scraping via XHR/API)
# ---------------------------------------------------------------------------

def extract_from_api(page: Page, api_url_fragment: str) -> list:
    """
    Intercepte les réponses réseau contenant api_url_fragment
    et retourne les données JSON directement depuis l'API du site.
    Plus robuste que parser le HTML pour les sites dynamiques.
    """
    captured = []

    def handle_response(response):
        if api_url_fragment in response.url:
            with contextlib.suppress(Exception):
                captured.append(response.json())

    page.on("response", handle_response)
    page.reload()
    page.wait_for_load_state("networkidle")
    page.remove_listener("response", handle_response)

    return captured


# ---------------------------------------------------------------------------
# Scroll infini (si la page charge du contenu en scrollant)
# ---------------------------------------------------------------------------

def scroll_to_bottom(page: Page, pause: float = 1.5, max_scrolls: int = 20) -> None:
    """Scrolle jusqu'en bas pour déclencher le chargement lazy."""
    for _ in range(max_scrolls):
        previous_height = page.evaluate("document.body.scrollHeight")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(pause)
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == previous_height:
            break


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------

def go_to_next_page(page: Page) -> bool:
    """Clique sur le bouton 'page suivante'. Retourne False si dernière page."""
    try:
        next_btn = page.query_selector("a.next, a[rel='next']")
        if next_btn is None:
            return False
        next_btn.click()
        page.wait_for_load_state("domcontentloaded")
        time.sleep(DELAY_BETWEEN_PAGES)
        return True
    except PlaywrightTimeout:
        return False


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def save_to_csv(data: list[dict], filename: str = "output.csv") -> None:
    if not data:
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"{len(data)} lignes exportées dans {filename}")


def save_to_json(data: list[dict], filename: str = "output.json") -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{len(data)} éléments exportés dans {filename}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    all_data = []

    with sync_playwright() as playwright:
        browser, context = build_browser_context(playwright)
        page = context.new_page()

        try:
            page.goto(URL, wait_until="domcontentloaded")
            print(f"Page chargée : {page.title()}")

            # Décommenter si le site nécessite une connexion :
            # login(page, "https://example.com/login", "user@email.com", "motdepasse")

            page_num = 1
            while True:
                print(f"Scraping page {page_num}...")

                # Décommenter si la page utilise le scroll infini :
                # scroll_to_bottom(page)

                # Option A : extraire depuis le HTML
                page_data = extract_data(page)

                # Option B : intercepter l'API (décommenter et adapter) :
                # page_data = extract_from_api(page, "/api/items")

                all_data.extend(page_data)
                print(f"  → {len(page_data)} éléments récupérés")

                if not go_to_next_page(page):
                    break
                page_num += 1

        finally:
            context.close()
            browser.close()

    print(f"\nTotal : {len(all_data)} éléments")
    save_to_csv(all_data, "output.csv")
    save_to_json(all_data, "output.json")


if __name__ == "__main__":
    main()
