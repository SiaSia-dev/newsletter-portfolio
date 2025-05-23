# Planification

## Principe de fonctionnement

Le système de planification organise les publications de manière automatique sur la semaine, en attribuant un jour à chaque projet extrait de la newsletter.

## Méthode de planification

La méthode `schedule_posts_from_newsletter(start_date=None)` gère la planification :

```python
def schedule_posts_from_newsletter(self, start_date=None):
    """Planifie les publications quotidiennes à partir de la newsletter"""
    
    # Extraction des projets
    projects = self.extract_content_from_newsletter()
    
    # Détermination de la date de début
    if start_date:
        # Utiliser la date spécifiée
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%d/%m/%Y").date()
        next_monday = start_date
    else:
        # Trouver le prochain lundi
        today = datetime.now().date()
        days_to_monday = today.weekday()
        
        if days_to_monday == 0:  # Si c'est déjà lundi
            next_monday = today
        else:
            days_until_next_monday = 7 - days_to_monday
            next_monday = today + timedelta(days=days_until_next_monday)
    
    # Création des publications programmées
    for i, project in enumerate(projects):
        # Calculer la date (un jour après l'autre)
        publish_date = next_monday + timedelta(days=i)
        
        # Heure aléatoire entre 9h et 11h
        hour = random.randint(9, 11)
        minute = random.randint(0, 59)
        publish_datetime = datetime.combine(publish_date, datetime.min.time().replace(hour=hour, minute=minute))
        
        # Création de l'entrée pour le post
        new_post = {
            "title": project['title'],
            "description": project['description'],
            "text": self._format_post_text(project),
            "image_url": project['image_url'],
            "scheduled_time": publish_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending"
            # ... autres champs
        }
        
        # Ajout au DataFrame de posts
        # ...
```

## Algorithme de planification

1. **Détermination de la date de départ** :
   - Si une date est spécifiée par l'utilisateur, elle est utilisée
   - Sinon, le prochain lundi est calculé à partir de la date actuelle

2. **Distribution des publications** :
   - Un projet par jour, du lundi au samedi
   - Maximum de 6 projets par semaine

3. **Randomisation des heures** :
   - Heure aléatoire entre 9h et 11h du matin
   - Minute aléatoire entre 0 et 59

4. **Enregistrement des publications** :
   - Les publications sont stockées dans un fichier CSV
   - L'état initial est "pending" (en attente)

## Format des données de planification

Chaque publication planifiée contient :

| Champ | Description |
|-------|-------------|
| title | Titre du projet |
| description | Description courte |
| text | Texte formaté pour LinkedIn |
| image_url | Chemin de l'image |
| scheduled_time | Date et heure de publication (YYYY-MM-DD HH:MM:SS) |
| status | État ("pending", "published", "failed") |
| jour_semaine | Jour de la semaine en français |
| date_formatee | Date formatée (DD/MM/YYYY) |
| heure_formatee | Heure formatée (HH:MM) |

## Gestion des doublons

Le système vérifie si des projets avec les mêmes titres existent déjà dans le CSV pour éviter les publications en double :

```python
existing_titles = df['title'].tolist()
new_projects = [p for p in projects if p['title'] not in existing_titles]
```