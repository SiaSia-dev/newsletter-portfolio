import os
import yaml
import re

def extract_paths_from_nav(nav_item, paths=None):
    """Extrait récursivement tous les chemins de fichiers de la structure nav."""
    if paths is None:
        paths = []
    
    if isinstance(nav_item, list):
        for item in nav_item:
            extract_paths_from_nav(item, paths)
    elif isinstance(nav_item, dict):
        for _, value in nav_item.items():
            extract_paths_from_nav(value, paths)
    elif isinstance(nav_item, str) and nav_item.endswith('.md'):
        paths.append(nav_item)
    
    return paths

def create_default_content(file_path):
    """Crée un contenu par défaut basé sur le nom du fichier."""
    # Extraire le nom du fichier sans extension
    title = os.path.basename(file_path).replace('.md', '')
    # Convertir les tirets en espaces et mettre en majuscule chaque mot
    title = ' '.join(word.capitalize() for word in title.split('-'))
    
    # Générer un contenu par défaut
    content = f"# {title}\n\nContenu pour {title}. Remplacez ce texte par votre documentation.\n\n"
    
    # Ajouter du contenu supplémentaire simplifié en fonction du type de page
    if "installation" in file_path.lower():
        content += """## Installation

Instructions d'installation de l'application LinkedIn Automation.

## Configuration

Instructions de configuration.
"""
    elif "api" in file_path.lower():
        content += """## Vue d'ensemble de l'API

Cette page documente les principales méthodes de l'API `LinkedInNewsletterAutomation`.

## Méthodes principales

### `schedule_posts_from_newsletter(start_date=None)`

Planifie les publications quotidiennes à partir de la newsletter.

### `extract_content_from_newsletter()`

Extrait le contenu des projets de la newsletter HTML.

### `publish_post(post_data)`

Publie un post sur LinkedIn.

### `run_scheduler()`

Exécute le planificateur pour vérifier régulièrement les posts à publier.
"""
    elif "architecture" in file_path.lower():
        content += """## Architecture générale

L'application est construite autour de la classe principale `LinkedInNewsletterAutomation` qui orchestre l'ensemble du processus.

## Composants principaux

1. **Authentification LinkedIn**: Gestion des tokens OAuth
2. **Extracteur de contenu**: Analyse de la newsletter HTML
3. **Planificateur**: Organisation des publications
4. **Moteur de publication**: Interface avec l'API LinkedIn
5. **Système de persistence**: Stockage des données dans un fichier CSV
"""
    
    return content

# Chemin du fichier de configuration MkDocs
mkdocs_config_path = 'mkdocs.yml'

# Lire le fichier de configuration
with open(mkdocs_config_path, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# Extraire tous les chemins de fichiers de la section 'nav'
if 'nav' in config:
    file_paths = extract_paths_from_nav(config['nav'])
    
    print(f"Création de {len(file_paths)} fichiers de documentation...")
    
    # Créer chaque fichier
    for file_path in file_paths:
        # Chemin complet incluant le dossier docs/
        full_path = os.path.join('docs', file_path)
        # Créer les dossiers intermédiaires si nécessaires
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Vérifier si le fichier existe déjà
        if os.path.exists(full_path):
            print(f"Le fichier {file_path} existe déjà, pas de modification")
        else:
            # Créer le fichier avec un contenu par défaut
            with open(full_path, 'w', encoding='utf-8') as file:
                file.write(create_default_content(file_path))
            print(f"Fichier créé: {file_path}")
    
    print("Création des fichiers de documentation terminée!")
else:
    print("Erreur: Aucune section 'nav' trouvée dans le fichier de configuration")