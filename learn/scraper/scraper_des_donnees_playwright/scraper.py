"""
Démo Playwright — Scraping de scrapethissite.com/pages/forms/
Même résultat que la version Selenium, mais avec Playwright.
Récupère les stats NHL sur toutes les pages, exporte en CSV, et génère un GIF.
"""

import csv
import glob
import os

from PIL import Image
from playwright.sync_api import sync_playwright

# --- Configuration ---
BASE_URL = "https://www.scrapethissite.com/pages/forms/"
OUTPUT_FILE = "hockey_teams.csv"
SCREENSHOTS_DIR = "screenshots"
GIF_FILE = "scraping.gif"
COLUMNS = ["Team Name", "Year", "Wins", "Losses", "OT Losses", "Win %", "Goals For (GF)", "Goals Against (GA)", "+/-"]

# --- Préparation du dossier screenshots ---
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# --- Lancement du navigateur ---
# Playwright gère son propre navigateur (pas besoin de chromedriver)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})

    # ============================================================
    # 1. Détection du nombre de pages
    # ============================================================
    page.goto(BASE_URL)

    # Playwright attend automatiquement le chargement du DOM
    # On peut quand même attendre un élément précis avec wait_for_selector
    page.wait_for_selector("ul.pagination")

    # Récupérer les numéros de page via locator (l'API moderne de Playwright)
    links = page.locator("ul.pagination li a").all()
    page_numbers = [int(link.text_content()) for link in links if link.text_content().strip().isdigit()]
    total_pages = max(page_numbers)
    print(f"Pages détectées : {total_pages}")

    # ============================================================
    # 2. Scraping page par page
    # ============================================================
    all_teams = []

    for num in range(1, total_pages + 1):
        page.goto(f"{BASE_URL}?page_num={num}")
        page.wait_for_selector("tr.team")

        # Screenshot de la page courante
        screenshot_path = os.path.join(SCREENSHOTS_DIR, f"page_{num:02d}.png")
        page.screenshot(path=screenshot_path)

        # Sélection de toutes les lignes du tableau via locator
        rows = page.locator("tr.team").all()

        for row in rows:
            # inner_text() est l'équivalent Playwright de .text en Selenium
            all_teams.append(
                {
                    "Team Name": row.locator("td.name").inner_text().strip(),
                    "Year": row.locator("td.year").inner_text().strip(),
                    "Wins": row.locator("td.wins").inner_text().strip(),
                    "Losses": row.locator("td.losses").inner_text().strip(),
                    "OT Losses": row.locator("td.ot-losses").inner_text().strip(),
                    "Win %": row.locator("td.pct").inner_text().strip(),
                    "Goals For (GF)": row.locator("td.gf").inner_text().strip(),
                    "Goals Against (GA)": row.locator("td.ga").inner_text().strip(),
                    "+/-": row.locator("td.diff").inner_text().strip(),
                }
            )

        print(f"  Page {num}/{total_pages} — {len(rows)} équipes récupérées — screenshot OK")

    browser.close()

# --- Export CSV ---
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(all_teams)

print(f"\n{len(all_teams)} équipes exportées dans {OUTPUT_FILE}")

# --- Compilation des screenshots en GIF animé ---
screenshot_files = sorted(glob.glob(os.path.join(SCREENSHOTS_DIR, "page_*.png")))
frames = [Image.open(f) for f in screenshot_files]

frames[0].save(
    GIF_FILE,
    save_all=True,
    append_images=frames[1:],
    duration=800,
    loop=0,
)

print(f"GIF animé créé : {GIF_FILE} ({len(frames)} frames)")
