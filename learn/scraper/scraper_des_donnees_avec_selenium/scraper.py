"""
Démo Selenium — Scraping de scrapethissite.com/pages/forms/
Récupère les stats NHL (Hockey Teams) sur toutes les pages et exporte en CSV.
Capture un screenshot de chaque page et compile le tout en GIF animé.
"""

import csv
import glob
import os
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# --- Configuration ---
BASE_URL = "https://www.scrapethissite.com/pages/forms/"
OUTPUT_FILE = "hockey_teams.csv"
SCREENSHOTS_DIR = "screenshots"
GIF_FILE = "scraping.gif"
COLUMNS = ["Team Name", "Year", "Wins", "Losses", "OT Losses", "Win %", "Goals For (GF)", "Goals Against (GA)", "+/-"]

# --- Préparation du dossier screenshots ---
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# --- Lancement du navigateur (fenêtre visible pour la démo) ---
options = Options()
options.add_argument("--window-size=1280,900")
options.add_argument("--disable-search-engine-choice-screen")

driver = webdriver.Chrome(options=options)

# --- Détection du nombre de pages ---
# On charge la première page et on lit les liens de pagination
driver.get(BASE_URL)

# On attend que la pagination soit présente dans le DOM (via CSS selector)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.pagination")))

# On récupère tous les <a> dans la pagination via XPATH
page_links = driver.find_elements(By.XPATH, "//ul[@class='pagination']//li/a")

# On ne garde que les liens dont le texte est un nombre (on ignore « et »)
page_numbers = [int(link.text) for link in page_links if link.text.strip().isdigit()]
total_pages = max(page_numbers)
print(f"Pages détectées : {total_pages}")

# --- Scraping page par page ---
all_teams = []

for page in range(1, total_pages + 1):
    driver.get(f"{BASE_URL}?page_num={page}")

    # On attend qu'au moins une ligne d'équipe apparaisse (via CLASS_NAME)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "team")))

    # Scroll progressif pour effet démo vidéo
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    scroll_pos = 0
    while scroll_pos < total_height - viewport_height:
        scroll_pos += 120
        driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
        time.sleep(0.08)
    time.sleep(0.3)

    # Screenshot de la page courante
    screenshot_path = os.path.join(SCREENSHOTS_DIR, f"page_{page:02d}.png")
    driver.save_screenshot(screenshot_path)

    # Remonter en haut avant extraction
    driver.execute_script("window.scrollTo(0, 0);")

    # On sélectionne toutes les lignes <tr> ayant la classe "team" (via CSS selector)
    rows = driver.find_elements(By.CSS_SELECTOR, "tr.team")

    for row in rows:
        # Extraction de chaque colonne via CLASS_NAME (plus lisible que CSS pour une seule classe)
        name = row.find_element(By.CLASS_NAME, "name").text.strip()
        year = row.find_element(By.CLASS_NAME, "year").text.strip()
        wins = row.find_element(By.CLASS_NAME, "wins").text.strip()
        losses = row.find_element(By.CLASS_NAME, "losses").text.strip()
        ot_losses = row.find_element(By.CLASS_NAME, "ot-losses").text.strip()
        win_pct = row.find_element(By.CLASS_NAME, "pct").text.strip()
        gf = row.find_element(By.CLASS_NAME, "gf").text.strip()
        ga = row.find_element(By.CLASS_NAME, "ga").text.strip()

        # Le +/- est dans un <td> avec la classe "diff" (via XPATH relatif)
        diff = row.find_element(By.XPATH, ".//td[contains(@class, 'diff')]").text.strip()

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

    print(f"  Page {page}/{total_pages} — {len(rows)} équipes récupérées — screenshot OK")
    time.sleep(0.5)

driver.quit()

# --- Export CSV ---
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(all_teams)

print(f"\n{len(all_teams)} équipes exportées dans {OUTPUT_FILE}")

# --- Compilation des screenshots en GIF animé ---
screenshot_files = sorted(glob.glob(os.path.join(SCREENSHOTS_DIR, "page_*.png")))
frames = [Image.open(f) for f in screenshot_files]

# Première frame = base, les autres = append. 800ms par frame, boucle infinie.
frames[0].save(
    GIF_FILE,
    save_all=True,
    append_images=frames[1:],
    duration=800,
    loop=0,
)

print(f"GIF animé créé : {GIF_FILE} ({len(frames)} frames)")
