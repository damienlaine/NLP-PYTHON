# Mise en situation

Vous venez d'être recruté à LINAGORA et travaillez pour le projet LinTO dont la documentation publique est en grande partie obsolète. (vous n'y trouverez pas grand-chose d'utile. Évitez de vous y attarder).

Afin de simplifier et de rationaliser l'usage des technologies LinTO, votre première mission consiste à factoriser une série de services de NLP qui sont développés sur une même base :

- **Une interface HTTP** pour faire des requêtes synchrones directement
- **Un connecteur Celery** qui permet d'enregistrer le service dans une queue afin qu'il puisse être découvert et consommer des tâches

## Objectifs

- Nous ne voulons plus de plusieurs repositories isolés pour nos services de NLP, mais souhaitons créer un mono-repo qui contient dans des dossiers la charge utile des services de NLP. L'objectif est donc de comprendre le fonctionnement du système afin de le factoriser et le rendre plus maintenable.
- Chaque service doit conserver son propre Dockerfile et sa capacité à être lancé "standalone" en mode "HTTP".
- Le "super-service" doit découvrir automatiquement les services de NLP disponibles dans le système (ce n'est pas entièrement le cas actuellement).
- Le mono-repo, à destination des utilisateurs finaux (développeurs), doit contenir un fichier `docker-compose.yml` et une configuration par défaut `.envdefault` qui permet de lancer d'un seul `docker compose up` le super-service de NLP, les services de NLP, un serveur Redis pour le task broking et une base de données. Les variables `.envdefault` doivent bien sûr être overridables soit en cli python avec des directive (--ma-directive), soit en définisant un fichier `.env` soit en les définissant pour le runtime.
- Migrer le système de base de données de MongoDB à PostgreSQL (et utiliser un ORM).

## Contexte de l'exercice

Dans ce repository, vous trouvez "à plat" plusieurs dossiers qui correspondent normalement à d'autres repositories GitHub existants :

- **linto-platform-nlp-extractive-summarization**, **linto-platform-nlp-keyphrase-extraction**, **linto-platform-nlp-keyword-extraction**, **linto-platform-nlp-named-entity-recognition**, **linto-platform-nlp-topic-modeling** : Sont des exemples de services de NLP qui accomplissent chacun une tâche précise.
- **linto-platform-nlp-services** : Est un "super-service" qui expose une API HTTP asynchrone permettant de demander des traitements de NLP aux services décrits précédemment (lire la documentation du repo pour en savoir plus). Il expose d'autre part d'autres routes, dont la route `/list-services` qui permet de lister les services de NLP disponibles.

## Critères de validation de l'exercice

- Un mono-repo avec un fichier `docker-compose.yml` tel que décrit précédemment.
- Dans ce mono-repo, au moins deux services de NLP de votre choix qui s'enregistrent automatiquement dans le super-service en factorisant au maximum le code (application Flask ou FastAPI, serveur Gunicorn, système de parsing de configuration). Ces services présentent chacun leur Dockerfile et une documentation simple (une ligne pour expliquer comment lancer en CLI Python, une ligne pour expliquer comment build le Docker, une ligne pour expliquer comment le lancer).
- Un template simplifié pour créer de nouveaux services (pensez à utiliser des classes et du polymorphisme, peut-être à en faire un module python à importer).
- Fonctionnalités : Mécanisme de monitoring de l'avancement des étapes de traitement (route `status`). Ajouter quand/si possible des signaux sur l'avancée d'une tâche / gestion d'erreur des tâches.
- Qualité du code : Emphase sur la factorisation (entre le mode HTTP et le mode Celery, refonte du mécanisme de découverte du service pour en faire un système dynamique, capacité de l'API du super-service à étendre sa spécification par exemple en utilisant des manifestes déclaratifs remontés par les services).
- Documentation : Décrire de manière extrêmement concise et tournée vers l'utilisateur final (développeur) le fonctionnement de ce mono-repo.

## Livraison

- Vous livrerez une nouvelle branche dans ce repository, validant les critères de l'exercice.
- La migration de MongoDB vers PostgreSQL est facultative mais fortement appréciée. Si cela revêt pour vous une difficulté ou un manque de connaissance sur ces technos précises, vous pouvez considérer cela comme un levier d'ajustement pour ne pas gréver votre capacité à délivrer des choses impressionnantes, n'hésitez pas à l'activer.
- Vous avez 1 semaine pour réaliser ce projet, qui évalue tout autant des compétences techniques multiples (en développement, en capacité d'auto-formation DevOps/Docker, en gestion de bases de données, en gestion de projets et en documentation...) qu'une capacité nécessaire d'adaptabilité, de résolution de problèmes complexes d'ingénierie en contexte Open Source.

## Note finale du rédacteur/recruteur

- Si pour des raisons personnelles ou professionnelles vous avez besoin de quelques jours supplémentaires, si vous savez pourtant que votre résultat sera remarquable. N'hésitez pas à nous en faire part.
- J'ai défini cet exercice pour vous Mr Idali, j'y ai aussi investi du temps et suis déterminé à trouver le bon candidat.
- La partie Docker n'est pas très compliquée en fait. On ne demande pas grand-chose... ça devrait se régler avec quelques coups de ChatGPT :)
