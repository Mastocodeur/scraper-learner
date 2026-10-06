# DataSchool : Scraping & Automatisation

Support de la DataSchool animée par **Rémy Gasmi** sur le **web scraping** et l'**automatisation** avec Python.

Ce dépôt regroupe des démos prêtes à exécuter pour apprendre à extraire des données du web et à automatiser des interactions dans un navigateur.

---

## Contenu du dépôt

### Scraping — `demo/scraper/`

Quatre scripts qui font la même chose (scraper les stats NHL depuis [scrapethissite.com](https://www.scrapethissite.com/pages/forms/)) avec quatre bibliothèques différentes, pour comparer les approches :

| Dossier | Bibliothèque | Approche |
|---------|-------------|----------|
| `scraper_des_donnees_beautifulsoup/` | **BeautifulSoup** + requests | HTML statique, pas de navigateur |
| `scraper_des_donnees_avec_selenium/` | **Selenium** | Navigateur piloté (Chrome) |
| `scraper_des_donnees_playwright/` | **Playwright** | Navigateur piloté (alternative moderne à Selenium) |
| `scraper_des_donnees_scrapling/` | **Scrapling** | Framework de scraping adaptatif |

Chaque script produit un fichier `hockey_teams.csv` avec les données extraites. Les versions Selenium et Playwright génèrent aussi des captures d'écran et un GIF animé du scraping.

### Automatisation — `demo/automatiser/`

Un script Selenium qui remplit automatiquement le formulaire d'inscription étudiant sur [demoqa.com](https://demoqa.com/automation-practice-form) avec un profil fictif.

---

## Installation

**Prérequis** : Python 3.12+ et [uv](https://docs.astral.sh/uv/).

```bash
# Cloner le dépôt
git clone https://git.equancy.cloud/rgasmi/dataschool-scraping-et-automatisation.git
cd data_school

# Créer l'environnement virtuel
uv venv

# Installer les dépendances (+ les navigateurs Playwright)
uv sync && uv run playwright install
```

---

## Sites pour s'entraîner au scraping

| # | Site | Description |
|---|------|-------------|
| 1 | [books.toscrape.com](http://books.toscrape.com) | Faux catalogue de livres avec pagination, catégories et prix |
| 2 | [quotes.toscrape.com](http://quotes.toscrape.com) | Citations avec auteurs et tags, inclut une version JS pour tester le scraping dynamique |
| 3 | [httpbin.org](https://httpbin.org) | Outil de test HTTP : headers, cookies, redirections, auth |
| 4 | [webscraper.io/test-sites](https://webscraper.io/test-sites) | Plusieurs sites de test (e-commerce, tables, AJAX) conçus pour l'apprentissage |
| 5 | [the-internet.herokuapp.com](https://the-internet.herokuapp.com) | Collection de pages couvrant login, drag & drop, iframes, uploads, etc. |
| 6 | [scrapethissite.com](https://www.scrapethissite.com) | Exercices progressifs de scraping avec des datasets variés |
| 7 | [toscrape.com](http://toscrape.com) | Hub regroupant plusieurs sites d'entraînement (books, quotes, login…) |
| 8 | [fake-json-api.mock.beeceptor.com](https://fake-json-api.mock.beeceptor.com) | API REST fictive pour tester le scraping d'endpoints JSON |
| 9 | [demoqa.com](https://demoqa.com) | Site de test pour l'automatisation : formulaires, modals, widgets interactifs |
| 10 | [practicetestautomation.com](https://practicetestautomation.com) | Scénarios de test d'automatisation : login, exceptions, pages protégées |
