"""
Démo Scrapling — Scraping de scrapethissite.com/pages/forms/
Même résultat que les versions Selenium/Playwright/BeautifulSoup, mais avec Scrapling.

Scrapling est un framework de scraping adaptatif :
  - Pas besoin de navigateur (comme BeautifulSoup)
  - API inspirée de Scrapy (css, xpath, find_all)
  - Détection intelligente des changements de structure
  - Anti-bot intégré (Cloudflare, etc.)
"""

import csv
import time

from scrapling.fetchers import Fetcher

# --- Configuration ---
BASE_URL = "https://www.scrapethissite.com/pages/forms/"
OUTPUT_FILE = "hockey_teams.csv"
COLUMNS = ["Team Name", "Year", "Wins", "Losses", "OT Losses", "Win %", "Goals For (GF)", "Goals Against (GA)", "+/-"]

# ============================================================
# 1. Première requête pour détecter le nombre de pages
# ============================================================
# Fetcher.get() fait une requête HTTP simple (pas de navigateur)
# Retourne un objet Adaptor avec des méthodes css(), xpath(), find_all()
page = Fetcher.get(BASE_URL)

# css() fonctionne comme en Scrapy : on peut extraire le texte avec ::text
# getall() retourne une liste de résultats (comme Scrapy)
page_links = page.css("ul.pagination li a")

# On filtre pour ne garder que les numéros de page (pas « et »)
page_numbers = []
for link in page_links:
    # .text récupère le contenu textuel du tag
    texte = link.text.strip()
    if texte.isdigit():
        page_numbers.append(int(texte))

total_pages = max(page_numbers)
print(f"Pages détectées : {total_pages}")

# ============================================================
# 2. Scraping page par page
# ============================================================
all_teams = []

for num in range(1, total_pages + 1):
    # On passe les paramètres directement dans l'URL
    page = Fetcher.get(f"{BASE_URL}?page_num={num}")

    # find_all() — style BeautifulSoup, cherche par tag + attribut
    # Scrapling supporte les deux styles : css()/xpath() ET find()/find_all()
    rows = page.find_all("tr", {"class": "team"})

    for row in rows:
        # find() retourne le premier élément correspondant (style BeautifulSoup)
        name = row.find("td", {"class": "name"}).text.strip()
        year = row.find("td", {"class": "year"}).text.strip()
        wins = row.find("td", {"class": "wins"}).text.strip()
        losses = row.find("td", {"class": "losses"}).text.strip()
        ot_losses = row.find("td", {"class": "ot-losses"}).text.strip()

        # css() — style Scrapy, sélecteur CSS classique
        win_pct = row.css("td.pct")[0].text.strip()
        gf = row.css("td.gf")[0].text.strip()

        # xpath() — style XPath, pour montrer la troisième syntaxe
        ga = row.xpath(".//td[contains(@class, 'ga')]")[0].text.strip()
        diff = row.xpath(".//td[contains(@class, 'diff')]")[0].text.strip()

        all_teams.append(
            {
                "Team Name": name,
                "Year": year,
                "Wins": wins,
                "Losses": losses,
                "OT Losses": ot_losses,
                "Win %": win_pct,
                "Goals For (GF)": gf,
                "Goals Against (GA)": ga,
                "+/-": diff,
            }
        )

    print(f"  Page {num}/{total_pages} — {len(rows)} équipes récupérées")
    time.sleep(0.3)

# ============================================================
# 3. Export CSV
# ============================================================
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(all_teams)

print(f"\nTerminé ! {len(all_teams)} équipes exportées dans {OUTPUT_FILE}")
