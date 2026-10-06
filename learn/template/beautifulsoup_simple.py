"""
BeautifulSoup + Requests — version séquentielle
Commandes enchaînées pour scraper une page statique.
"""

import csv
import json

import requests
from bs4 import BeautifulSoup

URL = "https://example.com"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )
}

# ---------------------------------------------------------------------------
# 1. Requête HTTP
# ---------------------------------------------------------------------------

response = requests.get(URL, headers=HEADERS, timeout=10)
print(response.status_code)   # 200 = OK, 403 = bloqué, 429 = trop de requêtes
print(response.text[:500])    # aperçu du HTML brut

# ---------------------------------------------------------------------------
# 2. Parser le HTML
# ---------------------------------------------------------------------------

soup = BeautifulSoup(response.text, "lxml")

# ---------------------------------------------------------------------------
# 3. Sélectionner des éléments
# ---------------------------------------------------------------------------

# Par balise
titles = soup.find_all("h2")

# Par classe CSS
items = soup.select(".product-card")   # tous les éléments avec class="product-card"
first = soup.select_one(".product-card")  # uniquement le premier

# Par id
header = soup.select_one("#main-header")

# Par attribut
links = soup.find_all("a", href=True)  # tous les liens qui ont un href

# Combinaisons : balise + classe
specific = soup.select("div.container > ul > li")

# ---------------------------------------------------------------------------
# 4. Extraire le contenu
# ---------------------------------------------------------------------------

# Texte d'un élément
title_text = soup.select_one("h1").get_text(strip=True)

# Attribut d'une balise
href = soup.select_one("a")["href"]
src = soup.select_one("img")["src"]

# Boucle sur plusieurs éléments
data = []
for item in soup.select(".product-card"):
    title = item.select_one("h2").get_text(strip=True)
    price = item.select_one(".price").get_text(strip=True)
    link = item.select_one("a")["href"]
    data.append({"title": title, "price": price, "link": link})

print(data)

# ---------------------------------------------------------------------------
# 5. Pagination — récupérer la page suivante
# ---------------------------------------------------------------------------

next_page = soup.select_one("a.next, a[rel='next']")
if next_page:
    next_url = next_page["href"]
    response2 = requests.get(next_url, headers=HEADERS, timeout=10)
    soup2 = BeautifulSoup(response2.text, "lxml")

# ---------------------------------------------------------------------------
# 6. Export CSV
# ---------------------------------------------------------------------------

with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "link"])
    writer.writeheader()
    writer.writerows(data)

# ---------------------------------------------------------------------------
# 7. Export JSON
# ---------------------------------------------------------------------------

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
