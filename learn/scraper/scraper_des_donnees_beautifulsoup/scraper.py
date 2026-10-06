"""
Démo BeautifulSoup — Scraping de scrapethissite.com/pages/forms/
Même résultat que les versions Selenium/Playwright, mais sans navigateur.
requests récupère le HTML brut, BeautifulSoup le parse.
"""

import csv
import time

import requests
from bs4 import BeautifulSoup

# --- Configuration ---
BASE_URL = "https://www.scrapethissite.com/pages/forms/"
OUTPUT_FILE = "hockey_teams.csv"
COLUMNS = ["Team Name", "Year", "Wins", "Losses", "OT Losses", "Win %", "Goals For (GF)", "Goals Against (GA)", "+/-"]

# --- Session HTTP ---
# Une session réutilise la connexion TCP (plus rapide que requests.get à chaque fois)
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (DataSchool Demo Bot)"})

# ============================================================
# 1. Détection du nombre de pages
# ============================================================
response = session.get(BASE_URL)
response.raise_for_status()  # lève une exception si erreur HTTP (404, 500…)

# On parse le HTML avec BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# On cherche tous les <a> dans la pagination
# find_all retourne une liste d'éléments Tag
page_links = soup.select("ul.pagination li a")

# .string retourne le texte direct d'un tag (None si le tag contient des sous-éléments)
# .get_text() retourne tout le texte, même imbriqué — plus robuste ici
page_numbers = []
for link in page_links:
    texte = link.get_text(strip=True)
    if texte.isdigit():
        page_numbers.append(int(texte))

total_pages = max(page_numbers)
print(f"Pages détectées : {total_pages}")

# ============================================================
# 2. Scraping page par page
# ============================================================
all_teams = []

for num in range(1, total_pages + 1):
    response = session.get(BASE_URL, params={"page_num": num})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # find_all("tr", class_="team") — cherche tous les <tr> avec class="team"
    rows = soup.find_all("tr", class_="team")

    for row in rows:
        # find("td", class_="name") — cherche le premier <td> avec class="name" dans la row
        all_teams.append(
            {
                "Team Name": row.find("td", class_="name").get_text(strip=True),
                "Year": row.find("td", class_="year").get_text(strip=True),
                "Wins": row.find("td", class_="wins").get_text(strip=True),
                "Losses": row.find("td", class_="losses").get_text(strip=True),
                "OT Losses": row.find("td", class_="ot-losses").get_text(strip=True),
                "Win %": row.find("td", class_="pct").get_text(strip=True),
                "Goals For (GF)": row.find("td", class_="gf").get_text(strip=True),
                "Goals Against (GA)": row.find("td", class_="ga").get_text(strip=True),
                "+/-": row.find("td", class_="diff").get_text(strip=True),
            }
        )

    print(f"  Page {num}/{total_pages} — {len(rows)} équipes récupérées")
    time.sleep(0.3)

# --- Export CSV ---
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(all_teams)

print(f"\nTerminé ! {len(all_teams)} équipes exportées dans {OUTPUT_FILE}")
