L’écosystème Python propose de nombreux outils permettant de réaliser du scraping ou de l’automatisation web.

Ces outils ne répondent pas tous aux mêmes besoins. Certains sont conçus pour analyser du **HTML statique**, tandis que d’autres permettent de **simuler un navigateur** afin d’interagir avec des sites web dynamiques.

Le choix de l’outil dépend généralement de plusieurs facteurs :

- le type de site web à scraper
- la complexité des interactions nécessaires
- la quantité de données à récupérer
- la performance souhaitée
- la facilité de mise en place

Dans cette section, nous allons comparer les principaux modules Python utilisés pour le scraping afin de mieux comprendre leurs différences et leurs cas d’usage.

Les outils présentés dans cette section peuvent être regroupés en **deux grandes catégories**.

La première catégorie correspond aux **briques techniques utilisées dans le scraping**, tandis que la seconde regroupe les **outils de scraping à proprement parler**.

Le workflow classique est : 

    Requête HTTP → récupération du HTML → parsing du HTML → navigation dans le DOM → extraction des données


# Les briques techniques du scraping
La première catégorie regroupe des bibliothèques qui ne réalisent pas directement du scraping, mais qui fournissent les **fonctionnalités fondamentales nécessaires pour récupérer et analyser les données d’une page web**.

Ces modules permettent notamment de :

- envoyer des **requêtes HTTP**
- récupérer le **contenu HTML d’une page**
- analyser et parser la **structure du document HTML**
- manipuler le **DOM**


| Module | Type | Utilisation principale | Particularité | Popularité | Cas d’usage |
|------|------|------|------|------|------|
| `requests` | Client HTTP | envoyer des requêtes HTTP simples | API très simple et largement utilisée | `très élevée` | récupérer le HTML d’une page |
| `httpx` | Client HTTP moderne | requêtes HTTP avec support async | support HTTP/2 et async natif | `élevée` | scraping performant |
| `aiohttp` | Client HTTP asynchrone | effectuer des requêtes HTTP non bloquantes | conçu pour les applications asynchrones | `élevée` | scraping à grande échelle |
| `html5lib` | Parser HTML | parser HTML conforme aux standards | très tolérant aux HTML mal formés et corrige les erreurs | `élevée` | parsing HTML robuste |
| `lxml` | Parser HTML/XML | parsing HTML rapide avec XPath | extrêmement performant | `très élevée` | extraction rapide de données |
| `pyquery` | Manipulation DOM | manipulation du DOM avec syntaxe jQuery | sélecteurs CSS très pratiques | `moyenne` | sélection d’éléments HTML |


Pour être clair : 
- `requests`, `httpx` et `aiohttp` servent à **récupérer les pages web**
- `html5lib` et `lxml` servent à **analyser le HTML**
- `pyquery` permet de **manipuler le DOM**


Le module `html5lib` est particulièrement intéressant car il implémente le même algorithme de parsing que les navigateurs web.  
Il est donc capable d’interpréter et de corriger automatiquement des documents HTML mal formés, ce qui le rend très fiable pour analyser des pages web réelles.

# Les outils de scraping

La seconde catégorie regroupe les outils conçus spécifiquement pour **extraire des données depuis des sites web**.

Ces outils peuvent :

- analyser directement le HTML
- parcourir un site web
- interagir avec des pages dynamiques
- automatiser un navigateur


Ces outils utilisent souvent **les bibliothèques de la première catégorie en interne** pour fonctionner.

Par exemple :

- `BeautifulSoup` peut utiliser `lxml` ou `html5lib` pour parser le HTML
- `Scrapy` utilise des clients HTTP pour récupérer les pages web

| Outil | Catégorie | Scraping statique | Scraping dynamique | Automatisation | Exécute JavaScript | Crawling | Scraping de masse | Difficulté | Rapidité | Cas d’usage |
|------|------|------|------|------|------|------|------|------|------|------|
| `BeautifulSoup` | Parsing HTML | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | `facile` | `très rapide` | extraction de données dans du HTML |
| `Scrapy` | Crawling framework | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | `intermédiaire` | `très rapide` | scraping à grande échelle |
| `Scrapling` | Scraping library | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | `facile` | `rapide` | scraping moderne et adaptatif |
| `MechanicalSoup` | HTTP automation | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | `facile` | `rapide` | automatisation de formulaires web |
| `Selenium` | Browser automation | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | `intermédiaire` | `lent` | interaction avec des sites dynamiques |
| `Playwright` | Browser automation | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | `intermédiaire` | `rapide` | scraping de web apps modernes |
| `Puppeteer` | Browser automation | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | `intermédiaire` | `rapide` | automatisation Chrome / scraping JS |
| `Crawl4AI` | AI crawling | ✅ | ✅ | `partiel` | `partiel` | ✅ | ✅ | `intermédiaire` | `rapide` | extraction de contenu pour LLM |
| `LaVague` | AI automation | ✅ | ✅ | ✅ | `LLM` | ❌ | `expérimental` | `facile` | `variable` | automatisation web pilotée par IA |
| `browser-use` | AI browser agents | ✅ | ✅ | ✅ | `LLM` | ❌ | `expérimental` | `intermédiaire` | `variable` | agents web autonomes |


La colonne "Exécution JavaScript" indique si l’outil est capable d’exécuter le JavaScript d’une page web.  
Cette capacité est nécessaire pour scraper des sites modernes dont le contenu est généré dynamiquement dans le navigateur.

Certains outils comme `MechanicalSoup` permettent d’automatiser des interactions simples avec des sites web (formulaires, authentification) sans exécuter JavaScript.  
À l’inverse, des outils comme `Puppeteer`, `Selenium` ou `Playwright` utilisent un navigateur complet afin d’exécuter le JavaScript et interagir avec des applications web modernes.

---

## Focus sur les outils clés

### BeautifulSoup

`BeautifulSoup` est la bibliothèque la plus utilisée pour le **scraping statique** en Python. Elle permet de naviguer dans le DOM d’une page HTML, de rechercher des éléments par balise, classe, identifiant ou sélecteur CSS, et d’en extraire le contenu.

Elle ne gère ni les requêtes HTTP ni l’exécution de JavaScript : elle se concentre uniquement sur le **parsing et l’extraction**. C’est pourquoi elle est presque toujours utilisée en combinaison avec un client HTTP comme `requests` (voir la section [Illustration](#illustration--comment-ces-modules-travaillent-ensemble)).

Sa prise en main est très rapide, ce qui en fait un excellent point d’entrée pour débuter en scraping.

### Scrapy

`Scrapy` est un **framework complet** conçu pour le crawling et le scraping à grande échelle. Contrairement à BeautifulSoup qui ne gère qu’une seule étape (le parsing), Scrapy intègre nativement l’ensemble de la chaîne : requêtes HTTP, navigation entre les pages, extraction des données, nettoyage et export.

Il repose sur une architecture de **spiders** (scripts qui définissent comment parcourir un site et quelles données extraire) et de **pipelines** (étapes de traitement appliquées aux données après extraction).

Scrapy est détaillé dans la section [Le Scraping à grande échelle](10 Le Scraping à grande échelle).

### Scrapling

`Scrapling` est une bibliothèque Python apparue en **2024** qui se positionne comme une alternative moderne à BeautifulSoup. Elle propose une API simple et intuitive pour le parsing HTML, mais se distingue par plusieurs fonctionnalités avancées :

- **sélecteurs adaptatifs** : Scrapling est capable de retrouver un élément même si la structure HTML de la page a changé entre deux exécutions (modification de classes, réorganisation du DOM). Cela rend les scrapers plus **robustes dans le temps**
- **support du scraping dynamique** : contrairement à BeautifulSoup, Scrapling peut utiliser un navigateur headless en interne pour récupérer le contenu de pages dont le HTML est généré par JavaScript
- **performances optimisées** : Scrapling utilise des parsers performants et intègre des optimisations pour le traitement de grands volumes de données

Scrapling combine ainsi la **simplicité de BeautifulSoup** avec des fonctionnalités qui répondent aux problématiques actuelles du scraping (pages dynamiques, structures HTML instables).

### Selenium et Playwright

`Selenium` et `Playwright` sont deux outils d’**automatisation de navigateur**. Ils permettent de piloter un vrai navigateur (Chrome, Firefox, Edge, etc.) de manière programmatique : ouvrir des pages, cliquer sur des éléments, remplir des formulaires, faire défiler la page et attendre le chargement de contenu dynamique.

Leur principal atout est leur capacité à **exécuter le JavaScript** de la page, ce qui les rend indispensables pour scraper des sites modernes dont le contenu est généré dynamiquement.

Les deux outils remplissent un rôle similaire, mais présentent des différences notables :

| Critère | Selenium | Playwright |
|---------|----------|------------|
| Ancienneté | 2004, très mature | 2020, plus récent |
| Navigateurs | Chrome, Firefox, Edge, Safari | Chromium, Firefox, WebKit |
| Performance | Plus lent (un seul navigateur à la fois par défaut) | Plus rapide (support natif du parallélisme) |
| API | Verbeuse, beaucoup de documentation disponible | Plus concise et moderne |
| Attentes | Gestion manuelle des waits (explicit/implicit) | Attentes automatiques (auto-wait) |
| Communauté | Très large, historique | En forte croissance |

Selenium est détaillé dans la section [Focus sur Selenium](08 Focus sur Selenium).

### MechanicalSoup

`MechanicalSoup` est une bibliothèque légère qui combine `requests` et `BeautifulSoup` pour permettre d’**automatiser des interactions simples** avec des sites web : soumettre des formulaires, suivre des liens, gérer des sessions avec cookies.

Il ne lance pas de navigateur et n’exécute pas JavaScript. Il est donc limité aux sites statiques mais reste très pratique pour les cas simples nécessitant une authentification ou une navigation de page en page.

### Crawl4AI

`Crawl4AI` est un outil open source apparu en **2023**, conçu spécifiquement pour le **crawling et l’extraction de contenu destiné aux modèles d’IA (LLM)**.

Son objectif principal est de transformer le contenu de pages web en un format directement exploitable par un modèle de langage : texte nettoyé, Markdown structuré, ou données JSON. Il se distingue des outils classiques par plusieurs caractéristiques :

- **extraction orientée contenu** : Crawl4AI se concentre sur le contenu utile de la page (texte principal, articles, données) en filtrant automatiquement les éléments non pertinents (menus, publicités, footers)
- **support du scraping dynamique** : il peut utiliser un navigateur headless pour gérer les pages dont le contenu est généré par JavaScript
- **crawling intégré** : il est capable de parcourir automatiquement les liens d’un site pour extraire le contenu de plusieurs pages

Crawl4AI s’inscrit dans la tendance récente des outils qui ne cherchent plus seulement à extraire des données brutes, mais à **préparer le contenu pour l’ingestion par des systèmes d’intelligence artificielle**.

---

## Les outils de scraping pilotés par l’IA

L’émergence des **modèles de langage (LLM)** a donné naissance à une nouvelle catégorie d’outils qui ne se contentent plus d’exécuter des instructions prédéfinies : ils utilisent l’IA pour **comprendre les pages web et interagir avec elles de manière autonome**.

### LaVague

`LaVague` est un framework open source qui permet de piloter un navigateur web à partir d’**instructions en langage naturel**. Au lieu d’écrire des sélecteurs CSS ou XPath pour localiser des éléments, l’utilisateur décrit l’action souhaitée en texte libre (par exemple : "clique sur le bouton de connexion", "remplis le champ email avec cette adresse").

Un modèle de langage (LLM) interprète cette instruction, analyse la page web et détermine l’action à exécuter dans le navigateur. Cela rend l’automatisation web accessible sans connaissance technique approfondie du HTML ou du DOM.

### browser-use

`browser-use` est une bibliothèque Python qui permet de créer des **agents web autonomes** capables de naviguer sur le web pour accomplir des tâches complexes. Contrairement à LaVague qui exécute des instructions une par une, browser-use confie un **objectif global** à un agent IA qui planifie et exécute lui-même les étapes nécessaires.

Par exemple, un agent browser-use pourrait recevoir l’objectif "trouve les 10 hôtels les moins chers à Paris pour le 15 juin sur Booking.com" et naviguer de manière autonome sur le site pour accomplir cette tâche.

### Limites des outils IA

Ces outils représentent une avancée significative mais restent aujourd’hui **expérimentaux** pour plusieurs raisons :

- leur fiabilité dépend de la qualité du modèle de langage utilisé
- les résultats peuvent varier d’une exécution à l’autre (comportement non déterministe)
- le coût d’utilisation est plus élevé (appels API vers des LLM)
- les performances sont variables (temps de réponse du modèle)
- ils ne sont pas encore adaptés au scraping de masse

Ils sont néanmoins très prometteurs pour les cas où la **flexibilité** prime sur la **reproductibilité** et où les pages web évoluent fréquemment.

---

Les deux catégories sont donc **complémentaires** :

- les bibliothèques de la première catégorie fournissent les **briques techniques**
- les outils de la seconde catégorie permettent de **construire des solutions complètes de scraping**



# Illustration : comment ces modules travaillent ensemble

Dans la pratique, les outils de scraping fonctionnent rarement seuls.  
Ils s’appuient généralement sur plusieurs bibliothèques qui interviennent à différentes étapes du processus.

## Scraping statique : requests + BeautifulSoup

Le cas le plus courant en scraping statique consiste à combiner `requests` (pour récupérer la page) et `BeautifulSoup` (pour en extraire les données).

Le workflow typique est le suivant :

| Étape | Responsable | Rôle |
|-------|-------------|------|
| 1. Envoi de la requête HTTP | `requests` | Envoie une requête GET vers l’URL cible et récupère la réponse du serveur |
| 2. Récupération du HTML | `requests` | La réponse contient le code HTML de la page |
| 3. Parsing du HTML | Parser (`lxml`, `html5lib` ou `html.parser`) | Transforme le HTML brut en une structure d’arbre exploitable |
| 4. Navigation et extraction | `BeautifulSoup` | Navigue dans l’arbre, localise les éléments cibles et extrait les données |

Ce pipeline illustre bien pourquoi plusieurs bibliothèques doivent être combinées pour construire une solution de scraping complète. Chaque bibliothèque prend en charge **une responsabilité précise**.

## Scraping dynamique : Selenium ou Playwright

Pour les pages dynamiques, le workflow est différent. L’outil d’automatisation prend en charge **l’ensemble du processus** :

| Étape | Responsable | Rôle |
|-------|-------------|------|
| 1. Lancement du navigateur | `Selenium` ou `Playwright` | Ouvre un navigateur réel (Chrome, Firefox, etc.) |
| 2. Chargement de la page | Navigateur | Le navigateur charge la page et exécute le JavaScript |
| 3. Interactions | `Selenium` ou `Playwright` | Simule des actions utilisateur si nécessaire (clics, scroll, attentes) |
| 4. Extraction des données | `Selenium` ou `Playwright` | Localise les éléments dans le DOM via des sélecteurs et extrait leur contenu |

Dans ce cas, une seule bibliothèque gère à la fois les requêtes, le rendu JavaScript et l’extraction. Il n’est pas nécessaire d’utiliser `requests` ou `BeautifulSoup` en complément, bien que certains développeurs combinent Selenium avec BeautifulSoup pour bénéficier de sa syntaxe d’extraction plus pratique.

## Le rôle du parser

Lorsqu’on utilise `BeautifulSoup`, il est nécessaire de choisir un **parser** pour interpréter le HTML.

    Un parser est un composant qui analyse un document HTML ou XML et le transforme en une structure exploitable par un programme.

Concrètement, le parser lit le contenu HTML et le convertit en une **structure d’arbre appelée DOM**, composée d’objets Python.  
`BeautifulSoup` peut ensuite naviguer dans cet arbre afin de **rechercher, filtrer et extraire les données** présentes dans le document.

Autrement dit, le parser est responsable de **comprendre et structurer le HTML**, tandis que `BeautifulSoup` permet ensuite de **naviguer dans cette structure**.

### Parsers compatibles avec BeautifulSoup

Plusieurs parsers peuvent être utilisés avec `BeautifulSoup`.

| Parser | Description | Avantages | Inconvénients |
|------|------|------|------|
| `html.parser` | Parser HTML intégré à Python | facile à utiliser, aucune installation supplémentaire | moins rapide et moins tolérant aux erreurs |
| `lxml` | Parser externe très performant | très rapide, support HTML et XML | nécessite une dépendance externe |
| `lxml-xml` | Version XML du parser `lxml` | très performant pour analyser du XML | nécessite une dépendance externe |
| `html5lib` | Parser conforme aux standards HTML5 | très tolérant aux HTML mal formés | plus lent que les autres parsers |

### Quel parser choisir ?

Dans la pratique :

- `lxml` est souvent choisi pour sa **rapidité**
- `html5lib` est privilégié pour sa **robustesse face aux HTML mal formés**
- `html.parser` reste une solution simple lorsqu’on ne souhaite pas installer de dépendance externe

Nous verrons dans la section ateliers comment indiquer le parser à utiliser par BeautifulSoup.

# Scraping via API

Le scraping ne consiste pas toujours à analyser directement le HTML d’une page web.  
Dans de nombreux cas, les données sont en réalité récupérées par le site via des **API (Application Programming Interface)**.

    Une API permet à une application de récupérer ou d’envoyer des données vers un serveur via des requêtes HTTP, généralement au format JSON.

Lorsqu’un site web charge des données dynamiquement (par exemple un fil d’actualité, des résultats de recherche ou un tableau de données), il est fréquent que ces informations soient récupérées via une API.

Dans ces situations, il peut être **plus simple et plus fiable d'interroger directement l'API** plutôt que de scraper le HTML.

## Exemples d’API publiques

De nombreuses plateformes proposent des API permettant d’accéder à leurs données :

- `X (Twitter) API`
- `Reddit API`
- `GitHub API`
- `OpenWeather API`
- `Google Maps API`

Certaines institutions publient également des **API ouvertes** dans le cadre de politiques d’open data :

- API de données gouvernementales
- API de transport public
- API de données météorologiques
- API de données économiques

Par exemple, en France, la plateforme **data.gouv.fr** propose de nombreuses API publiques permettant d’accéder à des données administratives ou statistiques.

## Identifier les API utilisées par un site web

Il est souvent possible d’identifier les appels API utilisés par un site web grâce aux **outils de développement du navigateur**.

Pour cela :

1. Ouvrir les outils de développement (clic droit > Inspecter ou `F12`)
2. Aller dans l’onglet **Network** (Réseau)
3. Filtrer les requêtes **XHR / Fetch** pour ne voir que les appels API
4. Naviguer sur la page ou effectuer une action (recherche, clic, scroll)
5. Observer les requêtes qui apparaissent dans la liste
6. Cliquer sur une requête pour voir son **URL**, ses **headers** et surtout la **réponse** renvoyée par le serveur

Si la réponse contient des données au format **JSON** bien structurées, il est souvent possible de reproduire cette même requête directement depuis un script Python avec `requests` ou `httpx`, sans avoir besoin de parser le HTML.

Cette technique est particulièrement utile sur les sites dynamiques : plutôt que de lancer un navigateur avec Selenium pour attendre le chargement JavaScript, on peut **appeler directement l’API interne** du site et récupérer les données brutes.

## Avantages d’utiliser une API

Lorsqu’une API est disponible, l’utiliser présente plusieurs avantages :

- récupération des données **plus simple**
- données souvent **déjà structurées**
- **moins fragile** qu’un scraping HTML
- **plus rapide**

## Limites

Cependant, les API présentent parfois certaines limitations :

- authentification nécessaire
- quotas de requêtes
- accès restreint à certaines données

Dans certains cas, lorsque l’API n’est pas accessible ou ne fournit pas toutes les informations nécessaires, il reste alors nécessaire d’utiliser des techniques de **scraping HTML**.

# Pour aller plus loin : outils historiques

L’écosystème du scraping web a vu passer de nombreux outils qui ont contribué à son évolution. Certains ne sont plus les solutions de référence aujourd’hui, mais il est utile de les connaître car ils sont encore mentionnés dans des forums, des tutoriels et des projets existants.

| Outil | Année | Approche | Rôle historique | Remplacé par |
|------|------|------|------|------|
| `Splash` | 2014 | Moteur de rendu JavaScript léger, utilisé avec Scrapy | Permettait de rendre des pages JavaScript sans lancer un navigateur complet | `Playwright`, navigateurs headless modernes |
| `Helium` | 2017 | Surcouche simplifiée de Selenium | Rendait l’automatisation de navigateur plus accessible grâce à une API simplifiée | `Selenium 4.x` et `Playwright` qui proposent désormais des APIs plus complètes |
| `Requests-HTML` | 2018 | Combinait requêtes HTTP, parsing HTML et exécution JavaScript dans une seule bibliothèque | Tentait d’unifier scraping statique et dynamique | `Playwright` ; le projet est peu maintenu |

Ces outils illustrent trois approches différentes qui ont marqué l’histoire du scraping :

- **simplifier** l’automatisation du navigateur (`Helium`)
- **rendre du JavaScript côté serveur** sans navigateur complet (`Splash`)
- **unifier** scraping statique et dynamique dans un même outil (`Requests-HTML`)

L’écosystème a depuis convergé vers des solutions plus complètes. Aujourd’hui, les bibliothèques les plus utilisées reposent sur **l’automatisation complète d’un navigateur**, capable d’exécuter JavaScript et d’interagir avec des applications web modernes.

Parmi ces outils, **Selenium** occupe une place particulière et a longtemps été l’une des solutions de référence pour l’automatisation du web (voir section suivante).


# Quel outil choisir ?

Face à la diversité des outils présentés, le choix dépend principalement de **trois critères** : le type de page à scraper, le volume de données et le niveau de complexité souhaité.

| Situation | Outil recommandé |
|-----------|-----------------|
| Page statique simple (blog, article, données publiques) | `requests` + `BeautifulSoup` |
| Page statique avec structure HTML instable | `Scrapling` |
| Page dynamique (contenu chargé en JavaScript) | `Selenium` ou `Playwright` |
| Scraping de masse sur un site entier | `Scrapy` |
| Extraction de contenu pour un modèle d’IA | `Crawl4AI` |
| Automatisation simple (formulaire, login) sans JavaScript | `MechanicalSoup` |
| Site proposant une API accessible | Appel direct à l’API avec `requests` ou `httpx` |

Dans la pratique, il est fréquent de **combiner plusieurs outils** au sein d’un même projet selon les besoins de chaque étape.

