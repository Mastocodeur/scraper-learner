"""
Template BeautifulSoup + Requests
Scraping de pages statiques (contenu directement dans le HTML).
"""

import csv
import json
import time

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

URL = "https://example.com"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
}

DELAY_BETWEEN_REQUESTS = 2  # secondes


# ---------------------------------------------------------------------------
# Requête HTTP
# ---------------------------------------------------------------------------

def get_page(url: str) -> BeautifulSoup | None:
    """Télécharge une page et retourne un objet BeautifulSoup."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # lève une exception si 4xx/5xx
        return BeautifulSoup(response.text, "lxml")
    except requests.exceptions.HTTPError as e:
        print(f"Erreur HTTP {e.response.status_code} sur {url}")
    except requests.exceptions.ConnectionError:
        print(f"Impossible de se connecter à {url}")
    except requests.exceptions.Timeout:
        print(f"Timeout sur {url}")
    return None


# ---------------------------------------------------------------------------
# Extraction des données
# ---------------------------------------------------------------------------

def extract_data(soup: BeautifulSoup) -> list[dict]:
    """Extrait les données depuis la soupe HTML. À adapter selon le site."""
    results = []

    # Exemple : récupérer tous les titres h2 et leurs liens associés
    for item in soup.select("h2"):  # adapter le sélecteur CSS
        title = item.get_text(strip=True)
        link_tag = item.find_parent("a") or item.find("a")
        link = link_tag["href"] if link_tag else None

        results.append({
            "title": title,
            "link": link,
        })

    return results


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------

def get_next_page_url(soup: BeautifulSoup) -> str | None:
    """Retourne l'URL de la page suivante, ou None si dernière page."""
    next_btn = soup.select_one("a.next, a[rel='next']")  # adapter le sélecteur
    if next_btn and next_btn.get("href"):
        return next_btn["href"]
    return None


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
    url = URL

    while url:
        print(f"Scraping : {url}")
        soup = get_page(url)

        if soup is None:
            break

        page_data = extract_data(soup)
        all_data.extend(page_data)
        print(f"  → {len(page_data)} éléments récupérés")

        url = get_next_page_url(soup)

        if url:
            time.sleep(DELAY_BETWEEN_REQUESTS)

    print(f"\nTotal : {len(all_data)} éléments")
    save_to_csv(all_data, "output.csv")
    save_to_json(all_data, "output.json")


if __name__ == "__main__":
    main()
