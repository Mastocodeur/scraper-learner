Avant de passer aux outils de scraping, il est important de comprendre **comment un navigateur ou un script communique avec un serveur web** pour récupérer le contenu d'une page.

Cette communication repose sur un protocole appelé **HTTP**.

---

# HTTP et HTTPS

## HTTP (HyperText Transfer Protocol)

Le **HTTP** est le protocole utilisé pour échanger des données sur le web.

Lorsqu'un utilisateur ouvre une page web dans son navigateur, celui-ci envoie une **requête HTTP** au serveur qui héberge le site. Le serveur traite cette requête et renvoie une **réponse HTTP** contenant le contenu demandé (HTML, images, données JSON, etc.).

Ce mécanisme de **requête / réponse** est au cœur du fonctionnement du web et constitue également la base du scraping.

Le flux simplifié est le suivant :

    Client (navigateur ou script) → Requête HTTP → Serveur → Réponse HTTP → Client

## HTTPS (HTTP Secure)

Le **HTTPS** est la version sécurisée du protocole HTTP. Il fonctionne de la même manière, mais les données échangées entre le client et le serveur sont **chiffrées** grâce au protocole **TLS (Transport Layer Security)**.

Le HTTPS permet de garantir :

- la **confidentialité** des données échangées (les données ne peuvent pas être lues par un tiers)
- l'**intégrité** des données (les données ne peuvent pas être modifiées en transit)
- l'**authenticité** du serveur (le client peut vérifier l'identité du serveur grâce à un certificat)

Aujourd'hui, la grande majorité des sites web utilisent HTTPS. On peut le reconnaître grâce au **cadenas** affiché dans la barre d'adresse du navigateur et à l'URL qui commence par `https://`.

Dans le contexte du scraping, la différence entre HTTP et HTTPS est transparente : les bibliothèques Python comme `requests` ou `httpx` gèrent automatiquement le chiffrement HTTPS.

---

# Structure d'une requête HTTP

Une requête HTTP est composée de plusieurs éléments :

| Élément | Description | Exemple |
|---------|-------------|---------|
| **Méthode** | L'action à effectuer | `GET`, `POST` |
| **URL** | L'adresse de la ressource demandée | `https://example.com/page` |
| **Headers** | Informations supplémentaires sur la requête | `User-Agent`, `Accept` |
| **Body** | Données envoyées au serveur (optionnel) | Contenu d'un formulaire |

## Les headers (en-têtes)

Les **headers** sont des métadonnées envoyées avec la requête ou la réponse. Ils permettent de fournir des informations supplémentaires sur la communication.

Quelques headers fréquemment rencontrés :

| Header | Rôle | Exemple |
|--------|------|---------|
| `User-Agent` | Identifie le client (navigateur, script, bot) | `Mozilla/5.0 (Windows NT 10.0; Win64; x64)...` |
| `Accept` | Indique les types de contenu acceptés par le client | `text/html`, `application/json` |
| `Content-Type` | Indique le type de contenu envoyé dans le body | `application/x-www-form-urlencoded` |
| `Authorization` | Contient les informations d'authentification | `Bearer <token>` |
| `Cookie` | Envoie les cookies stockés par le navigateur | `session_id=abc123` |

En scraping, le header `User-Agent` est particulièrement important car certains sites bloquent les requêtes dont le User-Agent ne correspond pas à un navigateur classique.

---

# Les méthodes HTTP

Les méthodes HTTP définissent **le type d'action** que le client souhaite effectuer sur le serveur.

## Les méthodes les plus courantes

| Méthode | Description | Utilisation en scraping |
|---------|-------------|------------------------|
| `GET` | Récupérer une ressource | **Très fréquent** — c'est la méthode utilisée pour récupérer le contenu d'une page web |
| `POST` | Envoyer des données au serveur | **Fréquent** — utilisé pour soumettre des formulaires, envoyer des paramètres de recherche ou s'authentifier |
| `PUT` | Remplacer une ressource existante | Rarement utilisé en scraping |
| `PATCH` | Modifier partiellement une ressource | Rarement utilisé en scraping |
| `DELETE` | Supprimer une ressource | Rarement utilisé en scraping |
| `HEAD` | Récupérer uniquement les headers (sans le body) | Utile pour vérifier l'existence d'une page sans télécharger son contenu |
| `OPTIONS` | Demander les méthodes supportées par le serveur | Rarement utilisé en scraping |

## GET vs POST

En scraping, les deux méthodes les plus utilisées sont **GET** et **POST**.

| Critère | GET | POST |
|---------|-----|------|
| Objectif | Récupérer des données | Envoyer des données |
| Paramètres | Transmis dans l'URL (`?clé=valeur`) | Transmis dans le body de la requête |
| Visibilité | Les paramètres sont visibles dans l'URL | Les paramètres ne sont pas visibles dans l'URL |
| Cas d'usage en scraping | Charger une page web | Soumettre un formulaire, envoyer des filtres de recherche |

Par exemple :

- une requête **GET** vers `https://example.com/search?q=scraping` récupère les résultats de recherche pour le mot "scraping"
- une requête **POST** vers `https://example.com/login` avec un body contenant `username=user&password=pass` permet de s'authentifier sur un site

---

# Les codes de statut HTTP

Lorsqu'un serveur reçoit une requête HTTP, il renvoie une **réponse** accompagnée d'un **code de statut**. Ce code indique si la requête a été traitée avec succès ou si une erreur est survenue.

Les codes de statut sont regroupés en **cinq catégories** :

| Catégorie | Plage | Signification |
|-----------|-------|---------------|
| **1xx** | 100–199 | Information — la requête a été reçue et est en cours de traitement |
| **2xx** | 200–299 | Succès — la requête a été traitée avec succès |
| **3xx** | 300–399 | Redirection — la ressource a été déplacée |
| **4xx** | 400–499 | Erreur client — la requête est incorrecte ou non autorisée |
| **5xx** | 500–599 | Erreur serveur — le serveur n'a pas pu traiter la requête |

## Codes les plus fréquents

### Codes de succès (2xx)

| Code | Nom | Description |
|------|-----|-------------|
| `200` | OK | La requête a réussi. C'est la réponse standard pour une page web chargée correctement |
| `201` | Created | La ressource a été créée avec succès (souvent après un POST) |
| `204` | No Content | La requête a réussi mais il n'y a pas de contenu à renvoyer |

### Codes de redirection (3xx)

| Code | Nom | Description |
|------|-----|-------------|
| `301` | Moved Permanently | La ressource a été déplacée définitivement vers une nouvelle URL |
| `302` | Found | La ressource a été temporairement déplacée vers une autre URL |
| `304` | Not Modified | La ressource n'a pas été modifiée depuis la dernière requête |

### Codes d'erreur client (4xx)

| Code | Nom | Description |
|------|-----|-------------|
| `400` | Bad Request | La requête est mal formulée |
| `401` | Unauthorized | L'authentification est nécessaire pour accéder à la ressource |
| `403` | Forbidden | L'accès à la ressource est interdit |
| `404` | Not Found | La ressource demandée n'existe pas |
| `429` | Too Many Requests | Le client a envoyé trop de requêtes dans un laps de temps donné (rate limiting) |

### Codes d'erreur serveur (5xx)

| Code | Nom | Description |
|------|-----|-------------|
| `500` | Internal Server Error | Le serveur a rencontré une erreur interne |
| `502` | Bad Gateway | Le serveur a reçu une réponse invalide d'un serveur en amont |
| `503` | Service Unavailable | Le serveur est temporairement indisponible (maintenance, surcharge) |

## Codes importants en scraping

Dans le contexte du scraping, certains codes méritent une attention particulière :

- **`200`** : la requête a réussi, le contenu de la page est disponible dans la réponse
- **`403`** : le serveur refuse la requête — cela peut indiquer que le site a détecté un bot ou que l'accès est restreint
- **`404`** : la page n'existe pas ou l'URL est incorrecte
- **`429`** : le serveur signale un trop grand nombre de requêtes — il est alors nécessaire de ralentir le rythme du scraping (rate limiting)
- **`500` / `503`** : le serveur rencontre un problème — cela peut être temporaire ou lié à une surcharge causée par les requêtes du scraper

Une bonne pratique consiste à **vérifier le code de statut de chaque réponse** avant d'essayer d'extraire les données, afin de détecter rapidement les erreurs et d'adapter le comportement du scraper.

---

# Lien avec le scraping

Lorsqu'on réalise un scraping statique, le processus repose directement sur des requêtes HTTP :

1. Le script envoie une requête **GET** vers l'URL de la page cible
2. Le serveur renvoie une réponse avec le **code de statut** et le **contenu HTML**
3. Si le code est **200**, le HTML peut être analysé et les données extraites

Ce workflow est celui utilisé par les bibliothèques comme `requests` ou `httpx` combinées à `BeautifulSoup`.

Pour le scraping dynamique, les outils comme `Selenium` ou `Playwright` automatisent un navigateur complet qui gère lui-même les requêtes HTTP. Le scraper n'a alors pas besoin de manipuler directement les requêtes, mais il est tout de même utile de comprendre ce mécanisme pour diagnostiquer les problèmes éventuels.

Maintenant que nous avons vu comment les pages web sont structurées (HTML) et comment elles sont récupérées (requêtes HTTP), nous allons voir dans la section suivante comment les outils et les techniques de scraping ont évolué au fil du temps.
