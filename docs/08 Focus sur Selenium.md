Comme vu dans la section précédente, **Selenium** est l'un des outils de scraping et d'automatisation les plus utilisés en Python. Il permet de contrôler un navigateur web de manière programmatique, ce qui le rend particulièrement adapté au scraping de pages dynamiques.

Cette section propose un focus sur Selenium : son évolution, le rôle des drivers, les méthodes de localisation des éléments et les options de configuration.

# Les évolutions de Selenium

Le module Selenium est probablement l'un des modules Python qui a connu le plus de modifications au cours du temps. 
Ces modifications ont changé la manière de l'utiliser. Il est important d'avoir une vision globale de ces évolutions pour comprendre les différentes problématiques qu'a connu ce module et aussi pouvoir comprendre les différents forums et codes qui circulent sur internet. 

## Selenium 1.x (avant 2011)

La première version de Selenium nécessitait un serveur pour interagir avec les navigateurs. La gestion des drivers n'était pas encore une préoccupation majeure, car Selenium RC interagissait directement avec les navigateurs via JavaScript.

## Selenium 2.x (2011-2016)

Dans cette version, on introduit Selenium WebDriver. Cette version marquait un changement significatif en permettant une interaction directe avec les navigateurs à travers des API spécifiques appelées "drivers". Chaque navigateur (Chrome, Firefox, etc.) nécessitait un driver spécifique pour fonctionner.

Le code pour utiliser un driver et donc se connecter à un site ressemblait à ça : 

    driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

## Selenium 3.x (2016-2021)

Les utilisateurs devaient encore télécharger manuellement les drivers et définir le chemin dans le code. 
 
Cependant, des outils tiers comme `webdriver-manager` ou `chromedriver-autoinstaller` ont commencé à émerger, facilitant la gestion automatique des drivers.

Vers la fin de cette période (version 3.141.0 notamment), des bibliothèques comme `WebDriverManager` en Java ou `webdriver_manager` en Python ont commencé à gagner en popularité. Elles permettaient de télécharger automatiquement le bon driver sans que l'utilisateur ait à gérer manuellement les chemins d'accès :

    from webdriver_manager.chrome import ChromeDriverManager
    driver = webdriver.Chrome(ChromeDriverManager().install())

## Selenium 4.x (dès 2021)

Selenium 4 a apporté de nombreuses améliorations, y compris une API mise à jour et des fonctionnalités pour les tests sans serveur.

La version 4.6.0 de Selenium, publiée en octobre 2022, a introduit une fonctionnalité majeure qui automatise entièrement la gestion des drivers. Selenium télécharge et configure automatiquement le bon driver pour le navigateur spécifié, sans besoin d'une bibliothèque externe. Le code devient : 

    from selenium import webdriver
    driver = webdriver.Chrome()

Pour suivre les évolutions de ce module Python et rester à jour sur son scraping : [Les différentes mises à jour de Selenium](https://github.com/SeleniumHQ/selenium/blob/trunk/py/CHANGES)

---

# Les drivers

Pour fonctionner, Selenium a besoin d'un **driver** : un programme intermédiaire qui fait le lien entre le code Python et le navigateur web.

Concrètement, lorsque le script Python envoie une instruction (par exemple "ouvre cette page" ou "clique sur ce bouton"), c'est le driver qui traduit cette instruction en action dans le navigateur.

Chaque navigateur possède son propre driver :

| Navigateur | Driver |
|------------|--------|
| Google Chrome | ChromeDriver |
| Mozilla Firefox | GeckoDriver |
| Microsoft Edge | EdgeDriver |
| Safari | SafariDriver |

Le driver doit être **compatible avec la version du navigateur installé** sur la machine. Une incompatibilité de version est l'une des erreurs les plus fréquentes rencontrées avec Selenium.

Comme vu dans la section précédente sur les évolutions de Selenium :

- **Avant Selenium 4.6** : il fallait télécharger manuellement le driver ou utiliser une bibliothèque tierce comme `webdriver-manager`
- **Depuis Selenium 4.6** : Selenium gère automatiquement le téléchargement et la configuration du driver adapté au navigateur

En résumé :

    Code Python → Selenium → Driver → Navigateur → Page web

---

# Les différentes façons de localiser des éléments web


Il existe plusieurs méthodes pour identifier des éléments dans le DOM (Document Object Model) d'une page web avec Selenium :

- **ID** :  L'attribut `id` est unique pour chaque élément, ce qui en fait un moyen rapide et précis de localiser un élément.

- **NAME** : L'attribut `name` est souvent utilisé dans les formulaires et permet de cibler des éléments basés sur leur nom.

- **XPATH** :  `XPath` est un langage qui permet de naviguer dans la structure du document XML/HTML pour trouver un élément selon son emplacement relatif dans l'arbre DOM.

- **LINK_TEXT** : Cette méthode localise un lien (balise `<a>`) en fonction du texte visible qu'il contient.

- **PARTIAL_LINK_TEXT** : Similaire à LINK_TEXT, mais permet de localiser un lien en utilisant une partie seulement du texte visible.

- **TAG_NAME** : Permet de cibler les éléments par leur nom de balise HTML, comme `<div>`, `<input>`, etc.

- **CLASS_NAME** : Cette méthode localise les éléments en fonction de la valeur de leur attribut `class`, utile pour cibler des éléments avec un style ou une fonctionnalité spécifique.

- **CSS_SELECTOR** : Un sélecteur CSS permet de cibler des éléments en utilisant des règles similaires à celles utilisées en CSS pour le style des éléments.

Chacune de ces méthodes offre un niveau de précision et de flexibilité différent, en fonction du contexte et de la structure de la page web à analyser.



# Formulaire chrome_options

Lors de la création d'une instance de navigateur avec Selenium, il est possible de définir des **options de configuration** qui modifient le comportement du navigateur. Ces options sont particulièrement utiles en scraping, par exemple pour lancer le navigateur sans interface graphique, désactiver le chargement des images afin d'accélérer le scraping, ou encore modifier le User-Agent pour réduire la détection.

Voici une fiche pour répertorier toutes les options possibles de notre driver Chrome.

## Guide de codage
La structure du code est toujours la même : 
- Création d'une instance des options Chrome : 

    `chrome_options = Options()`
- Définition des options Chrome : 

    `chrome_options.add_argument(...)`
- Création d'une nouvelle instance du navigateur Chrome avec les options spécifiées : 

    `driver = webdriver.Chrome(options=chrome_options)`
- Définition de l'URL que l'on veut scraper et injection dans le driver :

    `url = "https://professeur-layton.fandom.com/fr/wiki/La_travers%C3%A9e_(1)"`

    `driver.get(url)`

Précision  : 
- `webdriver.Chrome` initialise le navigateur Chrome via le WebDriver de Selenium.
- `options=chrome_options` permet de passer les options définies précédemment à cette instance de Chrome.

Voici donc les différentes options possibles : 

## --- OPTIONS GÉNÉRALES ---

#### Désactiver l'invite de sélection du moteur de recherche au premier lancement
    chrome_options.add_argument('--disable-search-engine-choice-screen') 

#### Lancer Chrome en mode headless (sans interface graphique)
    chrome_options.add_argument('--headless')

Le mode **headless** est l'une des options les plus utilisées en scraping. Il permet d'exécuter Chrome sans ouvrir de fenêtre visible, ce qui est plus rapide et consomme moins de ressources. C'est le mode à privilégier lorsque le scraping est exécuté sur un serveur ou en tâche planifiée.

#### Désactiver l'accélération matérielle GPU (souvent nécessaire en mode headless)
    chrome_options.add_argument('--disable-gpu')

Cette option est généralement combinée avec `--headless`, car l'accélération GPU n'a pas de sens sans interface graphique et peut provoquer des erreurs sur certains systèmes.

#### Démarrer Chrome avec une fenêtre de taille spécifique
    chrome_options.add_argument('--window-size=1920,1080')

Définir une taille de fenêtre est important, y compris en mode headless. Certains sites web adaptent leur contenu en fonction de la taille de la fenêtre (responsive design). Sans cette option, le navigateur headless peut avoir une fenêtre très petite et ne pas afficher tous les éléments.

#### Démarrer Chrome maximisé
    chrome_options.add_argument('--start-maximized')

#### Ouvrir Chrome en mode incognito (navigation privée)
    chrome_options.add_argument('--incognito')

Le mode incognito permet de naviguer sans cookies ni cache préexistants, ce qui garantit que chaque session de scraping part d'un état propre.

#### Désactiver la sandbox de Chrome (moins sécurisé)
    chrome_options.add_argument('--no-sandbox')

La sandbox est un mécanisme de sécurité de Chrome qui isole les processus. Cette option est souvent nécessaire dans les environnements Docker ou Linux où la sandbox peut bloquer l'exécution. À éviter en dehors de ces cas.

#### Utiliser un profil utilisateur personnalisé (permet de conserver les cookies, l'historique, etc. associés au profil)
    chrome_options.add_argument('--user-data-dir=/path/to/your/custom/profile')



## --- SÉCURITÉ ET VIE PRIVÉE ---

#### Désactiver la sécurité du web, par exemple, pour accéder à des pages avec des erreurs SSL
    chrome_options.add_argument('--disable-web-security')

#### Désactiver l'isolation des sites (peut améliorer les performances mais réduit la sécurité)
    chrome_options.add_argument('--disable-site-isolation-trials')

#### Désactiver les infobars telles que "Chrome est contrôlé par un logiciel de test automatisé"
    chrome_options.add_argument('--disable-infobars')

#### Désactiver les extensions installées dans Chrome
    chrome_options.add_argument('--disable-extensions')

Utile pour alléger le navigateur et éviter que des extensions interfèrent avec le scraping.

#### Bloquer les popups indésirables, tels que les fenêtres publicitaires et autres fenêtres intempestives
    chrome_options.add_argument("--disable-popup-blocking")

#### Désactiver les notifications du navigateur
    chrome_options.add_argument('--disable-notifications')

Les notifications (demandes de permission, alertes) peuvent interrompre le déroulement d'un script de scraping. Cette option les empêche d'apparaître.

#### Activer la navigation en toute sécurité, pour bloquer les contenus malveillants
    chrome_options.add_argument('--safebrowsing-disable-download-protection')

## --- PERFORMANCE ET RENDEMENT ---

#### Désactiver les fonctionnalités spécifiques de Chrome pour améliorer les performances
    chrome_options.add_argument('--disable-features=NetworkService,Notifications')

#### Désactiver le préchargement DNS pour accélérer le chargement des pages
    chrome_options.add_argument('--disable-dns-prefetch')

#### Désactiver le service réseau (réduit l'utilisation des ressources réseau)
    chrome_options.add_argument('--disable-network-service')

#### Activer ou désactiver la compression Brotli (peut affecter la performance du réseau)
    chrome_options.add_argument('--disable-brotli')

## --- AFFICHAGE ET RENDU ---

#### Désactiver WebGL pour éviter certaines animations ou graphiques lourds
    chrome_options.add_argument('--disable-webgl')

#### Désactiver le rendu logiciel, ce qui peut améliorer les performances graphiques
    chrome_options.add_argument('--disable-software-rasterizer')

#### Désactiver le chargement des images pour accélérer le chargement des pages
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')

Option très utile en scraping lorsque seul le texte ou la structure HTML est nécessaire. Désactiver les images réduit significativement le temps de chargement et la bande passante consommée.

#### Ouvrir un port pour le débogage à distance
    chrome_options.add_argument('--remote-debugging-port=9222')

Permet de se connecter au navigateur depuis un autre outil (par exemple Chrome DevTools) pour observer en temps réel ce que fait le script. Utile pendant la phase de développement du scraper.

## --- DÉTECTION D'AUTOMATISATION ---

De nombreux sites web mettent en place des mécanismes pour détecter les navigateurs automatisés et bloquer les bots. Les options ci-dessous permettent de **réduire les signaux de détection**, rendant le navigateur plus difficile à distinguer d'un utilisateur réel.

#### Désactiver les fonctionnalités qui révèlent que le navigateur est contrôlé par un outil d'automatisation
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

Par défaut, Chrome expose une propriété JavaScript `navigator.webdriver` qui vaut `true` lorsque le navigateur est piloté par Selenium. Cette option désactive ce signal.

#### Empêcher l'utilisation de l'extension d'automatisation par défaut de Chrome
    chrome_options.add_experimental_option("useAutomationExtension", False)

#### Exclure certains commutateurs (comme 'enable-automation') qui révèlent que le navigateur est automatisé
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

Ces deux options sont généralement utilisées **ensemble** pour supprimer les traces d'automatisation visibles par les scripts anti-bot du site.

## --- AUTRES OPTIONS UTILES ---

#### Spécifier un User-Agent personnalisé
    chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"')

Le **User-Agent** est une chaîne envoyée avec chaque requête HTTP qui identifie le navigateur et le système d'exploitation. Modifier le User-Agent permet de simuler un navigateur différent ou d'éviter d'être identifié comme un bot. En mode headless notamment, le User-Agent par défaut contient parfois la mention "HeadlessChrome", ce qui peut déclencher un blocage.

#### Désactiver les rapports de plantage de Chrome
    chrome_options.add_argument('--disable-crash-reporter')

#### Désactiver la gestion automatique des signets (favoris)
    chrome_options.add_argument('--disable-bookmark-autocomplete')

#### Désactiver les popups de confirmation d'impression
    chrome_options.add_argument('--kiosk-printing')

#### Désactiver le chargement des scripts JavaScript
    chrome_options.add_argument('--disable-javascript')

**Attention** : cette option est incompatible avec le scraping dynamique. Si la page cible charge ses données via JavaScript, les désactiver empêchera l'accès aux données. À utiliser uniquement pour du scraping de pages purement statiques.

#### Désactiver l'audio pour éviter les sons lors de l'automatisation
    chrome_options.add_argument('--mute-audio')

---

Selenium n'est pas le seul outil permettant d'automatiser un navigateur. Dans la section suivante, nous verrons les **outils no-code** qui permettent de réaliser du scraping sans écrire de code.