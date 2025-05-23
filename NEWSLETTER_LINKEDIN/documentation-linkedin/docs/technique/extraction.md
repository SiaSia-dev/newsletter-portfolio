# Extraction de contenu

## Principe de fonctionnement

L'extraction du contenu est une étape clé qui permet de transformer la newsletter HTML en données structurées pour les publications LinkedIn.

## Méthode d'extraction

La méthode `extract_content_from_newsletter()` utilise BeautifulSoup pour parser le HTML et extraire les informations importantes :

```python
def extract_content_from_newsletter(self):
    """Extrait le contenu des projets de la newsletter HTML"""
    try:
        with open(self.newsletter_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Trouver tous les project-card
        project_cards = soup.select('.project-card')
        
        projects = []
        
        for card in project_cards:
            # Extraire les informations de base de la carte
            title_elem = card.select_one('.project-title')
            title = title_elem.get_text().strip() if title_elem else "Sans titre"
            
            # Extraire le lien pour trouver l'ID du projet
            link_elem = title_elem.find('a') if title_elem else None
            project_id = link_elem.get('href') if link_elem else None
            
            description_elem = card.select_one('.project-description')
            description = description_elem.get_text().strip() if description_elem else ""
            
            image_elem = card.select_one('.project-image')
            image_url = image_elem.get('src') if image_elem else ""
            
            # Nettoyer le chemin de l'image
            if image_url:
                image_filename = os.path.basename(image_url)
            
            # Si nous avons un ID de projet, trouver le contenu complet
            full_content = ""
            if project_id:
                project_content = soup.select_one(project_id)
                if project_content:
                    paragraphs = project_content.find_all(['p', 'h2', 'h3', 'li'])
                    full_content = "\n\n".join([p.get_text().strip() for p in paragraphs[:5]])
            
            # Créer un dictionnaire pour ce projet
            project = {
                "title": title,
                "description": description,
                "image_url": image_filename if image_url else "",
                "text": full_content if full_content else description,
                "project_id": project_id
            }
            
            projects.append(project)
        
        print(f"Extraction réussie: {len(projects)} projets trouvés")
        return projects
        
    except Exception as e:
        print(f"Erreur lors de l'extraction du contenu: {str(e)}")
        return []
```

## Structure HTML attendue

L'extracteur s'attend à une structure HTML spécifique :

```html
<!-- Carte du projet avec résumé -->
<div class="project-card">
  <h2 class="project-title"><a href="#project-1">Titre du projet</a></h2>
  <p class="project-description">Description du projet</p>
  <img class="project-image" src="img/projet.jpg" alt="Description image">
</div>

<!-- Contenu détaillé du projet référencé par l'ID -->
<div id="project-1">
  <h2>Titre complet</h2>
  <p>Premier paragraphe du contenu...</p>
  <p>Deuxième paragraphe...</p>
</div>
```

## Données extraites

Pour chaque projet, l'extracteur crée un dictionnaire contenant :

| Champ | Description |
|-------|-------------|
| title | Titre du projet extrait de `.project-title` |
| description | Description courte extraite de `.project-description` |
| image_url | Chemin de l'image extraite de `.project-image` |
| text | Contenu textuel complet (limité à 5 paragraphes) |
| project_id | Identifiant du projet extrait du lien |

## Limitations et considérations

- L'extraction est limitée à 5 paragraphes par projet pour éviter les posts trop longs
- Les chemins d'images sont nettoyés pour ne conserver que le nom du fichier
- En cas d'erreur lors de l'extraction, une liste vide est retournée
- Si un élément est manquant, des valeurs par défaut sont utilisées