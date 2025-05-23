# API

## Classe principale: LinkedInNewsletterAutomation

La classe `LinkedInNewsletterAutomation` est le cœur de l'application. Elle gère l'extraction du contenu, la planification et la publication des posts.

## Méthodes principales

### `schedule_posts_from_newsletter(start_date=None)`

Planifie les publications quotidiennes à partir de la newsletter.

```python
def schedule_posts_from_newsletter(self, start_date=None):
    """
    Planifie les publications quotidiennes à partir de la newsletter.
    
    Args:
        start_date (str ou datetime.date, optionnel): Date de début pour les publications.
            Format attendu si c'est une chaîne: "DD/MM/YYYY".
            Si non spécifié, les publications commenceront à partir du prochain lundi.
    
    Returns:
        None
    """
```

### `extract_content_from_newsletter()`

Extrait le contenu des projets de la newsletter HTML en utilisant BeautifulSoup.

```python
def extract_content_from_newsletter(self):
    """
    Extrait le contenu des projets de la newsletter HTML.
    
    Returns:
        list: Liste des projets extraits avec leurs informations.
    """
```

### `publish_post(post_data)`

Publie un post sur LinkedIn.

```python
def publish_post(self, post_data):
    """
    Publie un post sur LinkedIn.
    
    Args:
        post_data (dict): Données du post à publier.
        
    Returns:
        bool: True si la publication a réussi, False sinon.
    """
```

### `run_scheduler()`

Exécute le planificateur pour vérifier régulièrement les posts à publier.

```python
def run_scheduler(self):
    """
    Exécute le planificateur pour vérifier régulièrement les posts à publier.
    """
```

### Autres méthodes importantes

- `upload_image_to_linkedin(image_path)` : Télécharge une image sur LinkedIn
- `display_posts_markdown_summary()` : Affiche un résumé des publications planifiées
- `check_and_refresh_token()` : Vérifie si le token est valide, sinon le rafraîchit
- `check_pending_posts()` : Vérifie s'il y a des posts en attente à publier

## Structure des données

### Format des projets extraits

```python
{
    "title": "Titre du projet",
    "description": "Description courte du projet",
    "image_url": "chemin/vers/image.jpg",
    "text": "Contenu textuel complet du projet",
    "project_id": "#id-du-projet"
}
```

### Format des posts planifiés

```python
{
    "title": "Titre du post",
    "description": "Description",
    "text": "Texte formaté du post LinkedIn",
    "image_url": "chemin/vers/image.jpg",
    "article_url": "",
    "scheduled_time": "2025-05-20 10:30:00",
    "status": "pending",
    "jour_semaine": "Lundi",
    "date_formatee": "20/05/2025",
    "heure_formatee": "10:30"
}
```