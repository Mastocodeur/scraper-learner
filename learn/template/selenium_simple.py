"""
Selenium — version séquentielle
Commandes enchaînées pour scraper une page dynamique (JavaScript, clics, formulaires).
Selenium >= 4.6 télécharge le driver Chrome automatiquement.
"""

import csv
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ---------------------------------------------------------------------------
# 1. Configurer et ouvrir le navigateur
# ---------------------------------------------------------------------------

options = Options()
options.add_argument("--headless=new")          # commenter pour voir le navigateur
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)   # attente max de 10 secondes pour les éléments

# ---------------------------------------------------------------------------
# 2. Naviguer vers une page
# ---------------------------------------------------------------------------

driver.get("https://example.com")
print(driver.title)         # titre de la page
print(driver.current_url)   # URL courante

# ---------------------------------------------------------------------------
# 3. Attendre qu'un élément soit présent
# ---------------------------------------------------------------------------

# Attendre un seul élément (bloque jusqu'à ce qu'il apparaisse)
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product")))

# Attendre que plusieurs éléments soient présents
elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product")))

# Attendre qu'un élément soit cliquable
btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.submit")))

# ---------------------------------------------------------------------------
# 4. Trouver des éléments
# ---------------------------------------------------------------------------

# Un seul élément (lève une exception si absent)
header = driver.find_element(By.CSS_SELECTOR, "h1")
nav = driver.find_element(By.ID, "main-nav")

# Plusieurs éléments (retourne une liste vide si aucun)
items = driver.find_elements(By.CSS_SELECTOR, ".product-card")
links = driver.find_elements(By.TAG_NAME, "a")

# ---------------------------------------------------------------------------
# 5. Extraire le contenu
# ---------------------------------------------------------------------------

# Texte visible d'un élément
title = header.text
title_stripped = header.text.strip()

# Attribut HTML
href = driver.find_element(By.CSS_SELECTOR, "a.cta").get_attribute("href")
src = driver.find_element(By.CSS_SELECTOR, "img").get_attribute("src")

# Contenu HTML interne (équivalent de innerHTML)
inner_html = element.get_attribute("innerHTML")

# Boucle sur plusieurs éléments
data = []
for item in items:
    title = item.find_element(By.CSS_SELECTOR, "h2").text.strip()
    price = item.find_element(By.CSS_SELECTOR, ".price").text.strip()
    link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    data.append({"title": title, "price": price, "link": link})

print(data)

# ---------------------------------------------------------------------------
# 6. Interagir avec la page
# ---------------------------------------------------------------------------

# Cliquer sur un élément
driver.find_element(By.CSS_SELECTOR, "button#accept-cookies").click()

# Remplir un champ texte
driver.find_element(By.CSS_SELECTOR, "input#search").send_keys("python scraping")

# Effacer un champ puis le remplir
field = driver.find_element(By.CSS_SELECTOR, "input#search")
field.clear()
field.send_keys("nouveau texte")

# Soumettre un formulaire (touche Entrée)
field.send_keys(Keys.RETURN)

# ---------------------------------------------------------------------------
# 7. Scroller
# ---------------------------------------------------------------------------

# Scroller jusqu'en bas de la page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1.5)

# Scroller vers un élément spécifique
driver.execute_script("arguments[0].scrollIntoView();", element)

# Scroller en boucle (scroll infini)
for _ in range(10):
    previous_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1.5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == previous_height:
        break   # plus de contenu à charger

# ---------------------------------------------------------------------------
# 8. Exécuter du JavaScript directement
# ---------------------------------------------------------------------------

# Retourner une valeur depuis la page
page_title = driver.execute_script("return document.title;")
scroll_position = driver.execute_script("return window.scrollY;")

# ---------------------------------------------------------------------------
# 9. Changer de page / onglet
# ---------------------------------------------------------------------------

# Revenir en arrière
driver.back()

# Aller de l'avant
driver.forward()

# Naviguer vers une nouvelle URL
driver.get("https://example.com/page-2")

# ---------------------------------------------------------------------------
# 10. Fermer le navigateur
# ---------------------------------------------------------------------------

driver.quit()

# ---------------------------------------------------------------------------
# 11. Export CSV
# ---------------------------------------------------------------------------

with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "link"])
    writer.writeheader()
    writer.writerows(data)

# ---------------------------------------------------------------------------
# 12. Export JSON
# ---------------------------------------------------------------------------

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
