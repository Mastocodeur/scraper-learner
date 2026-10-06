Jusqu'à présent, nous avons vu comment extraire des données depuis une ou quelques pages web. Mais dans de nombreux contextes professionnels, le besoin est tout autre : il s'agit de collecter des données sur **des centaines, des milliers, voire des millions de pages**.

Le passage à l'échelle introduit des problématiques qui dépassent le choix d'un outil de scraping. Il faut prendre en compte l'**infrastructure**, la **performance**, la **détection**, le **stockage** et l'**orchestration** des tâches.

Cette section présente les principales problématiques rencontrées lors d'un scraping à grande échelle ainsi que les solutions couramment utilisées.

---

# Les défis du scraping à grande échelle

Lorsqu'on scrape un petit nombre de pages, les contraintes sont généralement faibles. En revanche, à grande échelle, plusieurs problèmes apparaissent :

- les sites web **détectent et bloquent les requêtes automatisées**
- le volume de requêtes peut **surcharger le serveur cible**
- le scraping prend **beaucoup de temps** s'il est exécuté de manière séquentielle
- les données collectées doivent être **stockées, nettoyées et structurées**
- le processus doit être **fiable, reproductible et supervisé**

Chacune de ces problématiques fait l'objet d'une section ci-dessous.

---

# Anti-détection et contournement des protections

## Le problème

Les sites web mettent en place différents mécanismes pour détecter et bloquer les bots :

- analyse du **User-Agent**
- détection de **comportements non humains** (requêtes trop rapides, navigation linéaire)
- vérification de l'empreinte du navigateur (**fingerprinting**)
- systèmes de **CAPTCHA**
- blocage par **adresse IP**
- détection de l'absence de **cookies** ou de **JavaScript**

## Les solutions courantes

### Rotation de User-Agent

Le **User-Agent** est un header envoyé avec chaque requête HTTP qui identifie le navigateur utilisé. Si toutes les requêtes proviennent du même User-Agent (ou d'un User-Agent générique), le site peut facilement identifier un bot.

La rotation de User-Agent consiste à **changer aléatoirement le User-Agent à chaque requête** afin de simuler des navigateurs différents.

En Python, il existe des bibliothèques comme `fake-useragent` qui permettent de générer des User-Agents aléatoires :

```python
from fake_useragent import UserAgent
ua = UserAgent()
headers = {'User-Agent': ua.random}
```

### Rotation de proxies

Lorsqu'un grand nombre de requêtes provient de la **même adresse IP**, le site peut bloquer cette adresse.

Un **proxy** est un serveur intermédiaire qui transmet les requêtes à la place du client. En utilisant un pool de proxies, chaque requête peut être envoyée depuis une **adresse IP différente**, ce qui rend la détection beaucoup plus difficile.

Il existe plusieurs types de proxies :

| Type | Description | Fiabilité | Coût |
|------|-------------|-----------|------|
| Proxies gratuits | Proxies publics, souvent lents et instables | faible | gratuit |
| Proxies datacenter | Hébergés dans des datacenters, rapides mais parfois détectés | moyenne | faible |
| Proxies résidentiels | Utilisent des adresses IP de fournisseurs d'accès réels | élevée | élevé |
| Proxies rotatifs | Changent automatiquement d'IP à chaque requête | élevée | variable |

Des services comme **Bright Data**, **Oxylabs** ou **SmartProxy** proposent des pools de proxies résidentiels et rotatifs adaptés au scraping.

### Rotation des headers

Au-delà du User-Agent, d'autres headers peuvent être variés pour rendre les requêtes plus naturelles :

- `Accept-Language` (changer la langue)
- `Referer` (simuler une navigation depuis une autre page)
- `Accept-Encoding`

### Délais aléatoires entre les requêtes

Un comportement humain n'est jamais parfaitement régulier. Ajouter des **délais aléatoires** entre chaque requête permet de simuler un comportement plus naturel et d'éviter de déclencher les systèmes de rate limiting.

```python
import time
import random

time.sleep(random.uniform(1, 5))  # Pause aléatoire entre 1 et 5 secondes
```

### Résolution de CAPTCHAs

Certains sites affichent des **CAPTCHAs** pour vérifier que le visiteur est un humain. À grande échelle, il existe des services permettant de résoudre automatiquement ces CAPTCHAs :

- **2Captcha**
- **Anti-Captcha**
- **CapSolver**

Ces services utilisent soit des travailleurs humains, soit de l'intelligence artificielle pour résoudre les CAPTCHAs et renvoyer la solution au script de scraping.

---

# Rate limiting et gestion du rythme

## Le problème

Le **rate limiting** est un mécanisme utilisé par les serveurs web pour **limiter le nombre de requêtes** qu'un client peut envoyer sur une période donnée. Lorsque cette limite est dépassée, le serveur renvoie généralement un code de statut **429 (Too Many Requests)** et peut bloquer temporairement ou définitivement l'adresse IP.

Au-delà du blocage, envoyer trop de requêtes peut **surcharger le serveur cible**, ce qui peut être assimilé à une attaque **DDoS** et entraîner des conséquences juridiques (voir la section [Législation](11 Législation)).

## Les solutions

### Limiter le nombre de requêtes par seconde

La méthode la plus simple consiste à **réduire le rythme** des requêtes. Par exemple, ne pas dépasser 1 requête par seconde ou adapter le rythme en fonction de la tolérance du site.

### Respecter le fichier robots.txt

Comme vu dans la section sur le [crawling](02 Crawling, Scraping et Automatisation), le fichier `robots.txt` peut contenir une directive `Crawl-delay` qui indique le délai minimum recommandé entre deux requêtes :

```
User-agent: *
Crawl-delay: 10
```

Dans cet exemple, le site recommande d'attendre **10 secondes** entre chaque requête.

### Gestion des erreurs et des retries

À grande échelle, certaines requêtes échoueront inévitablement (erreurs réseau, timeouts, erreurs serveur). Il est important de mettre en place un système de **retry** (nouvelle tentative) avec un **backoff exponentiel** : si une requête échoue, on attend un délai croissant avant de réessayer.

```
1ère tentative → échec → attendre 2s
2ème tentative → échec → attendre 4s
3ème tentative → échec → attendre 8s
```

Cette approche permet de ne pas aggraver une situation de surcharge du serveur.

---

# Performance et parallélisation

## Le problème

Scraper des milliers de pages de manière **séquentielle** (une requête après l'autre) peut prendre un temps considérable. Par exemple, si chaque requête prend 2 secondes et qu'il y a 10 000 pages à scraper, le processus prendrait plus de **5 heures**.

## Les solutions

### Requêtes asynchrones

Les requêtes **asynchrones** permettent d'envoyer plusieurs requêtes **en parallèle** sans attendre la réponse de chacune avant d'envoyer la suivante.

En Python, les bibliothèques `aiohttp` et `httpx` (en mode async) permettent d'effectuer des requêtes asynchrones. Cela peut réduire considérablement le temps total d'exécution.

| Approche | Fonctionnement | Rapidité |
|----------|---------------|----------|
| Séquentielle | Une requête à la fois | lente |
| Asynchrone | Plusieurs requêtes simultanées | rapide |
| Multi-thread | Plusieurs threads exécutent des requêtes en parallèle | rapide |

### Scraping distribué

Pour les volumes les plus importants, le scraping peut être **distribué sur plusieurs machines**. Chaque machine prend en charge un sous-ensemble des pages à scraper, et les résultats sont ensuite agrégés.

Des frameworks comme **Scrapy** permettent de distribuer le travail grâce à des files d'attente partagées. Combiné à un outil comme **Scrapyd** ou **Scrapy Cloud** (proposé par Zyte), il est possible de déployer et piloter des spiders sur plusieurs serveurs.

### Mise en cache

La **mise en cache** consiste à stocker localement les pages déjà récupérées afin de ne pas les re-télécharger lors d'une exécution ultérieure. Cela permet de :

- réduire le nombre de requêtes envoyées au serveur
- accélérer les reprises après interruption
- limiter la consommation de bande passante

Scrapy propose un système de cache intégré (`HttpCacheMiddleware`) qui stocke les réponses sur le disque.

---

# Stockage et traitement des données

## Le problème

À grande échelle, les données extraites peuvent représenter des **volumes importants**. Il est nécessaire de prévoir un système de stockage adapté et de mettre en place des étapes de nettoyage et de transformation.

## Les formats de stockage

| Format | Avantages | Inconvénients | Cas d'usage |
|--------|-----------|---------------|-------------|
| CSV | Simple, lisible, universel | Peu adapté aux données imbriquées | Exports simples |
| JSON | Supporte les structures imbriquées | Fichiers volumineux | Données semi-structurées |
| Base de données SQL | Requêtes puissantes, intégrité des données | Mise en place plus complexe | Données structurées, volumes importants |
| Base de données NoSQL | Flexibilité du schéma, scalabilité | Moins adapté aux requêtes complexes | Données hétérogènes |

## Les pipelines de données

Dans un projet de scraping à grande échelle, les données passent généralement par plusieurs étapes après leur extraction :

1. **Extraction** : les données brutes sont récupérées depuis les pages web
2. **Nettoyage** : suppression des doublons, correction des formats, gestion des valeurs manquantes
3. **Transformation** : structuration des données dans le format souhaité
4. **Chargement** : insertion des données dans le système de stockage final

Ce processus est souvent désigné par l'acronyme **ETL (Extract, Transform, Load)**.

Scrapy intègre un système de **pipelines** qui permet de définir ces étapes de traitement directement dans le framework.

---

# Orchestration et planification

## Le problème

Un scraping à grande échelle n'est généralement pas une opération ponctuelle. Il doit souvent être **exécuté régulièrement** (quotidiennement, hebdomadairement) et de manière **fiable**.

## Les solutions

### Planification des tâches

Plusieurs outils permettent de planifier l'exécution automatique de scripts de scraping :

| Outil | Type | Description |
|-------|------|-------------|
| `cron` (Linux) | Planificateur système | Permet de planifier l'exécution de scripts à intervalles réguliers |
| `Task Scheduler` (Windows) | Planificateur système | Équivalent Windows de cron |
| `Airflow` | Orchestrateur | Outil open source permettant de définir, planifier et surveiller des workflows complexes |
| `Prefect` | Orchestrateur | Alternative moderne à Airflow, plus simple à configurer |
| `Celery` | File de tâches | Permet de distribuer et planifier des tâches asynchrones en Python |

### Monitoring et alertes

À grande échelle, il est essentiel de **surveiller le bon déroulement** du scraping et d'être alerté en cas de problème :

- taux de succès des requêtes
- nombre de pages scrapées vs attendues
- détection d'erreurs récurrentes (403, 429, 503)
- temps d'exécution anormal

Des outils de monitoring comme **Grafana** ou simplement des **logs structurés** permettent de suivre ces métriques.

### Gestion des interruptions

Un scraping de grande envergure peut être interrompu pour différentes raisons (panne réseau, erreur serveur, redémarrage de la machine). Il est important de prévoir un mécanisme de **reprise** afin de ne pas recommencer le processus depuis le début.

Cela passe généralement par :

- un suivi des URLs déjà traitées (dans un fichier ou une base de données)
- un système de **checkpoints** permettant de reprendre là où le processus s'est arrêté

---

# Focus : Scrapy, le framework de référence pour le scraping à grande échelle

Parmi tous les outils présentés dans cette formation, **Scrapy** occupe une place particulière lorsqu'il s'agit de scraping à grande échelle. C'est un **framework Python open source** spécialement conçu pour le crawling et le scraping de grands volumes de données.

Contrairement à des bibliothèques comme `BeautifulSoup` ou `requests`, qui se concentrent sur une étape spécifique du processus (parsing ou requêtes HTTP), Scrapy intègre nativement l'ensemble de la chaîne :

| Fonctionnalité | Description |
|----------------|-------------|
| **Crawling** | Parcours automatique des liens d'un site, gestion de la profondeur et des filtres d'URL |
| **Requêtes asynchrones** | Envoi de multiples requêtes simultanées sans bloquer l'exécution |
| **Middlewares** | Interception et modification des requêtes et réponses (rotation de User-Agent, gestion des proxies, gestion des cookies) |
| **Pipelines** | Traitement des données après extraction (nettoyage, dédoublonnage, stockage en base de données ou fichier) |
| **Cache HTTP** | Stockage local des réponses pour éviter de re-télécharger les pages déjà visitées |
| **Respect du robots.txt** | Prise en charge native du fichier `robots.txt` et de la directive `Crawl-delay` |
| **Export intégré** | Export des données en CSV, JSON, JSON Lines ou XML en une seule commande |

Scrapy est également conçu pour être **déployé sur des serveurs**. Combiné à des outils comme **Scrapyd** (serveur de déploiement) ou **Scrapy Cloud** (proposé par Zyte), il est possible de distribuer le scraping sur plusieurs machines et de piloter les spiders à distance.

C'est cette combinaison de fonctionnalités — performance, modularité et scalabilité — qui fait de Scrapy **le framework de référence pour les projets de scraping à grande échelle en Python**.

---

# Les aspirateurs de sites web : une autre forme de scraping à grande échelle

Comme vu dans la section sur les [outils no-code](09 Outils No-code et Low-code), les **aspirateurs de sites web** (comme HTTrack) permettent de télécharger tout ou partie d'un site afin d'en créer une copie locale.

Par nature, ces outils constituent une forme de scraping à grande échelle : ils parcourent et téléchargent automatiquement un **volume important de pages et de ressources** (HTML, images, fichiers).

Ils partagent donc certaines problématiques décrites dans cette section :

- le **volume de données** téléchargées peut être considérable
- le rythme des requêtes doit être maîtrisé pour ne pas **surcharger le serveur**
- le respect du fichier `robots.txt` et des conditions d'utilisation du site reste de mise

Cependant, les aspirateurs de sites se distinguent des outils de scraping classiques sur un point important : ils ne cherchent pas à **extraire des données structurées** mais plutôt à **copier l'intégralité du contenu accessible**. Pour cette raison, ils sont souvent utilisés en complément d'outils comme Scrapy, qui permettent ensuite de cibler et d'extraire les informations pertinentes depuis les pages récupérées.

---

# Autres outils adaptés au scraping à grande échelle

Au-delà de Scrapy et des aspirateurs de sites, d'autres outils sont particulièrement adaptés au passage à l'échelle :

| Outil | Forces pour le scraping à grande échelle |
|-------|------------------------------------------|
| `aiohttp` / `httpx` | Requêtes asynchrones permettant un débit élevé |
| `Playwright` | Automatisation de navigateur performante avec support du mode headless |
| `Apify` | Plateforme cloud avec infrastructure intégrée (proxies, stockage, orchestration) |
| `Zyte` | Solution industrielle avec API d'extraction et gestion des anti-bots |
| `Crawl4AI` | Crawling et extraction optimisés pour les grands volumes de données |

---

# Résumé

Le passage à l'échelle en scraping ne se résume pas à augmenter le nombre de requêtes. Il implique de répondre à un ensemble de problématiques complémentaires :

| Problématique | Enjeu | Solutions |
|---------------|-------|----------|
| Anti-détection | Éviter d'être bloqué par le site | Rotation de proxies, User-Agents, délais aléatoires |
| Rate limiting | Respecter les limites du serveur | Délais, backoff exponentiel, respect du robots.txt |
| Performance | Réduire le temps total d'exécution | Requêtes asynchrones, scraping distribué, mise en cache |
| Stockage | Gérer le volume de données collectées | Bases de données, pipelines ETL |
| Orchestration | Automatiser et fiabiliser le processus | Planification, monitoring, gestion des reprises |

La maîtrise de ces aspects permet de passer d'un script de scraping ponctuel à un **système de collecte de données robuste et industrialisé**.

Dans la section suivante, nous aborderons le **cadre juridique** qui encadre ces pratiques.
