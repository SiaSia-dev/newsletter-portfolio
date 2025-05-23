# Structure des fichiers

## Organisation du projet

```
linkedin-newsletter-automation/
├── linkedin_automation.py     # Script principal
├── linkedin_automation_oneshot.py  # Version pour publication ponctuelle
├── requirements.txt           # Dépendances Python
├── .env                       # Variables d'environnement (à créer)
├── linkedin_posts.csv         # Base de données des publications
├── linkedin_publications_reussies.log  # Journal des publications réussies
├── linkedin_publications_echecs.log    # Journal des échecs de publication
├── latest.html                # Newsletter par défaut (exemple)
└── img/                       # Dossier des images
    ├── projet1.jpg
    ├── projet2.png
    └── ...
```

## Format du fichier CSV

Le fichier `linkedin_posts.csv` stocke toutes les publications planifiées avec cette structure :

| Colonne | Description |
|---------|-------------|
| title | Titre du projet |
| description | Description courte |
| text | Texte complet du post LinkedIn |
| image_url | Chemin vers l'image du projet |
| article_url | URL externe (si applicable) |
| scheduled_time | Date et heure planifiées (format YYYY-MM-DD HH:MM:SS) |
| published_time | Date et heure réelles de publication |
| status | État de la publication (pending, published, failed) |
| attempts | Nombre de tentatives de publication |
| post_id | ID du post sur LinkedIn après publication |
| jour_semaine | Jour de la semaine (Lundi, Mardi, etc.) |
| date_formatee | Date formatée (DD/MM/YYYY) |
| heure_formatee | Heure formatée (HH:MM) |

## Format de la newsletter HTML

La newsletter doit suivre cette structure HTML :

```html
<div class="project-card">
  <h2 class="project-title"><a href="#project-1">Titre du projet</a></h2>
  <p class="project-description">Description du projet</p>
  <img class="project-image" src="img/projet.jpg" alt="Description image">
  <!-- Autres éléments du projet -->
</div>

<div id="project-1">
  <h2>Titre complet</h2>
  <p>Premier paragraphe du contenu...</p>
  <p>Deuxième paragraphe...</p>
  <!-- Le contenu complet du projet -->
</div>
```

L'outil extraira automatiquement ces informations pour créer les publications LinkedIn.