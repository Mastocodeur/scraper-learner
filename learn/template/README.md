# Templates de scraping

Trois templates prêts à l'emploi pour démarrer rapidement un projet de scraping.

## Quel template choisir ?

| Situation | Template recommandé |
|-----------|-------------------|
| Le contenu est visible dans le code source HTML (clic droit > Afficher le source) | `beautifulsoup_template.py` |
| Le contenu est chargé par JavaScript, nécessite des clics ou une connexion | `selenium_template.py` ou `playwright_template.py` |
| Tu veux la solution la plus moderne et la plus rapide | `playwright_template.py` |
| Tu es familier avec Selenium ou le projet l'utilise déjà | `selenium_template.py` |

## Fichiers

### `beautifulsoup_template.py`
- Bibliothèques : `requests` + `BeautifulSoup`
- Usage : sites statiques, pages dont le HTML contient directement les données
- Points forts : simple, léger, rapide
- Inclut : requête HTTP avec headers, extraction CSS, pagination, export CSV/JSON

### `selenium_template.py`
- Bibliothèque : `selenium` >= 4.6 (driver Chrome auto-géré)
- Usage : pages dynamiques, authentification, clics, scroll infini
- Points forts : mature, documentation abondante
- Inclut : options anti-détection, wait explicite, login, scroll, pagination, export CSV/JSON

### `playwright_template.py`
- Bibliothèque : `playwright` (installer avec `playwright install chromium`)
- Usage : pages dynamiques, SPA, interception des requêtes réseau
- Points forts : plus rapide que Selenium, API plus claire, interception XHR native
- Inclut : contexte anti-détection, login, scroll, pagination, interception API, export CSV/JSON

## Utilisation

1. Copier le fichier template dans ton projet
2. Modifier `URL` et les sélecteurs CSS dans `extract_data()`
3. Activer/désactiver les sections commentées selon les besoins (pagination, scroll, login)
4. Lancer le script

## Installation des dépendances

```bash
# BeautifulSoup
pip install requests beautifulsoup4 lxml

# Selenium
pip install selenium

# Playwright
pip install playwright
playwright install chromium
```
