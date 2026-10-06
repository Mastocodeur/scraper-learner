Maintenant que nous avons vu les différentes techniques et outils permettant de réaliser du scraping, il est essentiel de s'intéresser au **cadre juridique** qui encadre cette pratique.

# La législation autour du web scraping

Le web scraping consiste à collecter automatiquement des données disponibles sur des sites web.  
Bien que cette pratique soit très répandue dans le domaine de la data, elle soulève plusieurs **questions juridiques et éthiques**.

Contrairement à une idée reçue, le scraping **n’est pas illégal en soi**.  
Cependant, sa légalité dépend de plusieurs facteurs :

- la nature des données collectées
- les conditions d’utilisation du site web
- la manière dont les données sont collectées
- l’usage qui est fait des données extraites

Il est donc important de comprendre **les principaux cadres juridiques** qui peuvent s’appliquer au scraping.

---

## Quand le web scraping est généralement autorisé

Le scraping web est généralement considéré comme acceptable lorsque certaines conditions sont respectées.

Par exemple, il est généralement admis que le scraping peut être réalisé lorsque :

- les données extraites sont **accessibles publiquement**
- les informations ne sont **pas protégées par un système d’authentification**
- l’accès au site ne nécessite **pas de contourner une protection technique**

Dans ce cas, les données sont souvent considérées comme **librement accessibles sur le web**.

Cependant, même dans ces situations, il est important de rester prudent.  
La manière dont les données sont collectées et utilisées peut avoir des implications juridiques.

---

## Les conditions d’utilisation des sites web

La plupart des sites web disposent de **conditions d’utilisation (Terms of Service)** qui encadrent l’usage de leur plateforme.

Ces conditions peuvent par exemple interdire :

- l’utilisation de robots automatisés
- la collecte massive de données
- la reproduction ou la redistribution de contenus

Bien que la technique de scraping ne soit pas illégale en elle-même, son utilisation peut **enfreindre les conditions d’utilisation de certains sites**.

Le non-respect de ces conditions peut entraîner :

- la suspension d’un compte
- le blocage d’une adresse IP
- des actions juridiques dans certains cas

Les conditions d’utilisation relèvent généralement du **droit contractuel**, ce qui signifie qu’elles s’appliquent aux utilisateurs ayant accepté ces conditions.

---

## Le fichier robots.txt

Comme vu dans la [section sur le crawling](02 Crawling, Scraping et Automatisation), de nombreux sites publient un fichier `robots.txt` qui indique aux robots quelles parties du site peuvent être explorées.

D’un point de vue juridique, il est important de noter que le fichier `robots.txt` **n’a pas de valeur juridique contraignante**.  
Il s’agit d’une **convention de bonne conduite**, pas d’une protection légale. Cependant, ne pas le respecter peut être utilisé comme un **élément à charge** dans une procédure judiciaire, car il démontre une volonté de passer outre les indications du propriétaire du site.

---

## Propriété intellectuelle et droit des bases de données

Le scraping peut également entrer en conflit avec le **droit d'auteur** et le **droit sui generis des bases de données**.

En Europe, la **directive 96/9/CE** protège les bases de données ayant nécessité un **investissement substantiel** dans leur constitution, leur vérification ou leur présentation. Extraire une partie substantielle d'une telle base via du scraping peut constituer une violation de ce droit, même si les données sont publiquement accessibles.

Par ailleurs, les contenus présents sur un site web (textes, images, vidéos) peuvent être protégés par le **droit d'auteur**. Les reproduire ou les redistribuer sans autorisation peut constituer une contrefaçon.

---

## Protection des données personnelles (RGPD)

Lorsque le scraping concerne des **données personnelles**, il est soumis au **Règlement Général sur la Protection des Données (RGPD)**.

Les données personnelles incluent par exemple :

- noms
- adresses email
- numéros de téléphone
- informations professionnelles
- profils en ligne

Dans ce cas, les organisations doivent pouvoir justifier :

- la **finalité** du traitement
- la **base légale** de la collecte (consentement, intérêt légitime, etc.)
- la **durée de conservation** des données
- l'**information des personnes** concernées

Le non-respect du RGPD peut entraîner des sanctions importantes. La CNIL peut prononcer des amendes pouvant aller jusqu'à **20 millions d'euros** ou **4 % du chiffre d'affaires annuel mondial**.

C'est d'ailleurs sur ce fondement que la société Nestor a été sanctionnée (voir la section [Cas juridiques célèbres](#cas-juridiques-célèbres-autour-du-scraping)).

---

## Concurrence déloyale

En droit de la concurrence, certaines pratiques de scraping peuvent être qualifiées **d’acte de concurrence déloyale**.

Cela peut notamment être le cas lorsque :

- une entreprise collecte massivement les données d’un concurrent
- ces données sont ensuite utilisées pour reproduire un service
- l’activité du site cible est perturbée par les requêtes automatisées

Dans ces situations, les tribunaux peuvent considérer que le scraping constitue une **atteinte à l’activité économique d’un concurrent**.

---

# Cas juridiques célèbres autour du scraping

Plusieurs affaires judiciaires ont contribué à clarifier la légalité du scraping.

## Nestor (France, RGPD)

Un exemple notable en France concerne la société **Nestor**.

La CNIL a condamné cette société à une **amende de 20 000 euros** pour avoir constitué une base de prospects en ayant recours à une pratique de web scraping à partir de données accessibles sur le réseau social professionnel LinkedIn.

Dans ce cas, le problème ne venait pas uniquement du scraping lui-même, mais surtout de **l’utilisation des données collectées à des fins de prospection commerciale**.

Pour plus de détails :

- [Le cas Nestor (1)](https://www.alerionavocats.com/condamnation-societe-nestor-prospection-commerciale-fondee-interet-legitime-responsable-traitement-enseignements-tirer/)
- [Le cas Nestor (2)](https://www.plravocats.fr/blog/data-protection-rgpd/la-societe-nestor-sanctionee-par-la-cnil)

---

## LinkedIn vs hiQ Labs

L’un des cas les plus célèbres est l’affaire **LinkedIn contre hiQ Labs** aux États-Unis.

hiQ utilisait un système de scraping pour collecter des données publiques sur les profils LinkedIn afin de produire des analyses sur le marché du travail.

LinkedIn a tenté de bloquer cette pratique en invoquant :

- l’accès non autorisé à ses systèmes
- la violation de ses conditions d’utilisation

Les tribunaux américains ont finalement estimé que **le scraping de données publiques accessibles sans authentification n’était pas nécessairement illégal**.

Cette décision a été largement commentée dans le monde du scraping et de la data.

Pour plus de détails : [LinkedIn vs hiQ Labs](https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn)

---

## Ryanair vs PR Aviation

Dans cette affaire européenne, la compagnie aérienne Ryanair a poursuivi une entreprise qui récupérait automatiquement les prix des billets via scraping.

La justice européenne a reconnu que les **conditions d’utilisation d’un site pouvaient interdire le scraping**, même lorsque les données étaient accessibles publiquement.


---

# Bonnes pratiques

Même lorsque le scraping est légal, certaines bonnes pratiques permettent de limiter les risques :

- respecter les conditions d’utilisation des sites
- vérifier la nature des données collectées
- éviter de scraper des données personnelles sensibles
- limiter la fréquence des requêtes (rate limiting)
- éviter de surcharger les serveurs, car un volume de requêtes trop important peut s'apparenter à une attaque **DDoS** (Distributed Denial of Service) et entraîner des poursuites

Le **rate limiting** consiste par exemple à limiter le nombre de requêtes envoyées à un site sur une période donnée afin de ne pas perturber son fonctionnement.

Ces pratiques relèvent souvent d’une approche appelée **polite scraping**.

---

# Conclusion

Le web scraping est une technique très utilisée dans l’écosystème de la data, mais son utilisation doit être encadrée par une bonne compréhension des aspects juridiques.

Dans la pratique, la légalité du scraping dépend souvent :

- du type de données collectées
- du mode d’accès aux données
- de l’usage qui est fait des données

Il est donc recommandé d’adopter une approche **responsable et respectueuse des règles du web**.

Dans la section suivante, nous passerons à la pratique avec une démonstration de scraping.