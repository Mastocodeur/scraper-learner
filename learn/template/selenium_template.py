"""
Template Selenium
Scraping de pages dynamiques nécessitant un navigateur (JavaScript, authentification, clics, etc.).
Selenium >= 4.6 gère automatiquement le téléchargement du driver Chrome.
"""

import csv
import json
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

URL = "https://example.com"

HEADLESS = True          # False pour voir le navigateur
WAIT_TIMEOUT = 10        # secondes d'attente max pour les éléments
DELAY_BETWEEN_PAGES = 2  # secondes entre les pages


# ---------------------------------------------------------------------------
# Initialisation du driver
# ---------------------------------------------------------------------------

def build_driver() -> webdriver.Chrome:
    """Configure et retourne un driver Chrome."""
    options = Options()

    if HEADLESS:
        options.add_argument("--headless=new")

    # Taille de fenêtre (utile même en headless pour le responsive)
    options.add_argument("--window-size=1920,1080")

    # Anti-détection basique
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # User-Agent personnalisé
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )

    # Performances
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # Désactiver les notifications et popups
    options.add_argument("--disable-notifications")
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })

    driver = webdriver.Chrome(options=options)

    # Masquer le flag webdriver (complément anti-détection)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver


# ---------------------------------------------------------------------------
# Attente d'éléments
# ---------------------------------------------------------------------------

def wait_for(driver: webdriver.Chrome, css_selector: str, timeout: int = WAIT_TIMEOUT):
    """Attend qu'un élément soit présent dans le DOM et le retourne."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
    )


def wait_for_all(driver: webdriver.Chrome, css_selector: str, timeout: int = WAIT_TIMEOUT):
    """Attend que plusieurs éléments soient présents et les retourne."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))
    )


def wait_clickable(driver: webdriver.Chrome, css_selector: str, timeout: int = WAIT_TIMEOUT):
    """Attend qu'un élément soit cliquable et le retourne."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
    )


# ---------------------------------------------------------------------------
# Authentification (optionnel)
# ---------------------------------------------------------------------------

def login(driver: webdriver.Chrome, login_url: str, username: str, password: str) -> None:
    """Se connecte à un site via un formulaire. À adapter selon le site."""
    driver.get(login_url)

    wait_for(driver, "#username").send_keys(username)   # adapter le sélecteur
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
    wait_clickable(driver, "button[type='submit']").click()

    # Attendre que la connexion soit effective (adapter la condition)
    wait_for(driver, ".dashboard, .home, [data-logged-in]")
    print("Connexion réussie")


# ---------------------------------------------------------------------------
# Extraction des données
# ---------------------------------------------------------------------------

def extract_data(driver: webdriver.Chrome) -> list[dict]:
    """Extrait les données depuis la page courante. À adapter selon le site."""
    results = []

    try:
        items = wait_for_all(driver, ".item-class")  # adapter le sélecteur
    except TimeoutException:
        print("Aucun élément trouvé sur cette page")
        return results

    for item in items:
        try:
            title = item.find_element(By.CSS_SELECTOR, "h2").text.strip()
            description = item.find_element(By.CSS_SELECTOR, "p").text.strip()
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

            results.append({
                "title": title,
                "description": description,
                "link": link,
            })
        except NoSuchElementException:
            continue

    return results


# ---------------------------------------------------------------------------
# Scroll infini (si la page charge du contenu en scrollant)
# ---------------------------------------------------------------------------

def scroll_to_bottom(driver: webdriver.Chrome, pause: float = 1.5, max_scrolls: int = 20) -> None:
    """Scrolle jusqu'en bas de la page pour déclencher le chargement lazy."""
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------

def go_to_next_page(driver: webdriver.Chrome) -> bool:
    """Clique sur le bouton 'page suivante'. Retourne False si dernière page."""
    try:
        next_btn = wait_clickable(driver, "a.next, a[rel='next']", timeout=3)
        next_btn.click()
        time.sleep(DELAY_BETWEEN_PAGES)
        return True
    except TimeoutException:
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
    driver = build_driver()
    all_data = []

    try:
        driver.get(URL)
        print(f"Page chargée : {driver.title}")

        # Décommenter si le site nécessite une connexion :
        # login(driver, "https://example.com/login", "user@email.com", "motdepasse")

        page = 1
        while True:
            print(f"Scraping page {page}...")

            # Décommenter si la page utilise le scroll infini :
            # scroll_to_bottom(driver)

            page_data = extract_data(driver)
            all_data.extend(page_data)
            print(f"  → {len(page_data)} éléments récupérés")

            if not go_to_next_page(driver):
                break
            page += 1

    finally:
        driver.quit()

    print(f"\nTotal : {len(all_data)} éléments")
    save_to_csv(all_data, "output.csv")
    save_to_json(all_data, "output.json")


if __name__ == "__main__":
    main()
