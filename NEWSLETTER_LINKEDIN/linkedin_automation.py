"""
Automatisation des Publications LinkedIn à partir d'une Newsletter HTML
Ce script permet d'extraire le contenu d'une newsletter HTML et de programmer des publications quotidiennes sur LinkedIn.
"""

import os
import json
import time
import requests
import pandas as pd
from datetime import datetime, timedelta
import schedule
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re
import random

# Accroches pour les posts LinkedIn
ACCROCHES = [
    "📰 Newsletter : Après l'automatisation de la création d'une newsletter hebdomadaire, on extrait et programme la publication de ces contenus sur LinkedIn tout au long de la semaine",
    "🔄 Automatisation de contenu : De la newsletter au post LinkedIn, comment optimiser le cycle de publication de contenu",
    "📋 COPE (Create Once, Publish Everywhere) : Notre newsletter hebdomadaire se transforme automatiquement en posts LinkedIn",
    "🤖 Automatisation marketing : Comment transformer une newsletter en série de posts LinkedIn sans effort supplémentaire",
    "⚙️ Workflow optimisé : Notre newsletter alimente désormais automatiquement notre présence LinkedIn",
    "📢 Diffusion multicanal : Découvrez comment notre newsletter devient source de contenu pour LinkedIn"
]

# Charger les variables d'environnement
load_dotenv()

class LinkedInNewsletterAutomation:
    def __init__(self, newsletter_path=None, data_source_path=None, images_folder=None):
        # Charger les variables d'environnement
        load_dotenv()
        
        # Utiliser les valeurs de .env ou des paramètres
        self.newsletter_path = newsletter_path or os.getenv("NEWSLETTER_PATH")
        self.data_source_path = data_source_path or os.getenv("DATA_SOURCE_PATH", "linkedin_posts.csv")
        self.images_folder = images_folder or os.getenv("IMAGES_FOLDER")
        
        # Vérifier si les chemins essentiels sont définis
        if not self.newsletter_path or not self.images_folder:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.newsletter_path = self.newsletter_path or os.path.join(script_dir, "latest.html")
            self.images_folder = self.images_folder or os.path.join(script_dir, "img")
            print(f"Attention: Utilisation des chemins par défaut qui pourraient ne pas exister:")
            print(f"- Newsletter: {self.newsletter_path}")
            print(f"- Images: {self.images_folder}")
        
        # Créer les dossiers nécessaires pour le CSV
        if self.data_source_path and os.path.dirname(self.data_source_path):
            os.makedirs(os.path.dirname(self.data_source_path), exist_ok=True)
        
        # Identifiants API LinkedIn (à stocker dans un fichier .env)
        self.client_id = os.getenv("LINKEDIN_CLIENT_ID")
        self.client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
        self.redirect_uri = os.getenv("LINKEDIN_REDIRECT_URI")
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.refresh_token = os.getenv("LINKEDIN_REFRESH_TOKEN")
        
        # URL de base pour l'API LinkedIn
        self.api_url = "https://api.linkedin.com/v2"
        
        # Chemin vers la source de données (CSV)
        self.data_source_path = data_source_path or "linkedin_posts.csv"
        
        # Chemin vers le fichier HTML de la newsletter
        self.newsletter_path = newsletter_path 
        
        # Dossier contenant les images
        self.images_folder = images_folder or "img"
        
        # S'assurer que le dossier de données existe
        data_dir = os.path.dirname(self.data_source_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
            print(f"Dossier créé: {data_dir}")
        
        # Obtenir l'ID de l'organisation (pour les pages d'entreprise)
        self.organization_id = None
        
        # Vérifier si le token est valide, sinon le rafraîchir
        self.check_and_refresh_token()
        
        # Initialiser l'ID de l'organisation
        self.get_organization_id()
    
    def generate_authorization_url(self):
        """Génère l'URL pour l'autorisation OAuth"""
        auth_url = "https://www.linkedin.com/oauth/v2/authorization"
        scope = "r_liteprofile r_emailaddress w_member_social w_organization_social"
        
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": scope,
            "state": "random_state_string"  # Pour la sécurité CSRF
        }
        
        url_params = "&".join([f"{key}={value}" for key, value in params.items()])
        return f"{auth_url}?{url_params}"
    
    def get_access_token(self, authorization_code):
        """Obtient un token d'accès à partir du code d'autorisation"""
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        
        payload = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        response = requests.post(token_url, data=payload)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.refresh_token = token_data.get("refresh_token")
            
            # Sauvegarder les tokens dans le fichier .env
            self.save_tokens_to_env()
            
            return token_data
        else:
            print(f"Erreur lors de l'obtention du token: {response.text}")
            return None
    
    def refresh_access_token(self):
        """Rafraîchit le token d'accès"""
        if not self.refresh_token:
            print("Aucun refresh token disponible.")
            return False
        
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        response = requests.post(token_url, data=payload)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data["access_token"]
            if "refresh_token" in token_data:
                self.refresh_token = token_data["refresh_token"]
            
            # Sauvegarder les tokens dans le fichier .env
            self.save_tokens_to_env()
            
            return True
        else:
            print(f"Erreur lors du rafraîchissement du token: {response.text}")
            return False
    
    def save_tokens_to_env(self):
        """Sauvegarde les tokens dans le fichier .env"""
        env_file = ".env"
        
        # Lire le contenu actuel du fichier
        if os.path.exists(env_file):
            with open(env_file, "r") as file:
                lines = file.readlines()
        else:
            lines = []
        
        # Mettre à jour ou ajouter les tokens
        new_lines = []
        updated_access = False
        updated_refresh = False
        
        for line in lines:
            if line.startswith("LINKEDIN_ACCESS_TOKEN="):
                new_lines.append(f"LINKEDIN_ACCESS_TOKEN={self.access_token}\n")
                updated_access = True
            elif line.startswith("LINKEDIN_REFRESH_TOKEN=") and self.refresh_token:
                new_lines.append(f"LINKEDIN_REFRESH_TOKEN={self.refresh_token}\n")
                updated_refresh = True
            else:
                new_lines.append(line)
        
        if not updated_access:
            new_lines.append(f"LINKEDIN_ACCESS_TOKEN={self.access_token}\n")
        
        if not updated_refresh and self.refresh_token:
            new_lines.append(f"LINKEDIN_REFRESH_TOKEN={self.refresh_token}\n")
        
        # Écrire le contenu mis à jour
        with open(env_file, "w") as file:
            file.writelines(new_lines)
    
    def check_and_refresh_token(self):
        """Vérifie si le token est valide, sinon le rafraîchit"""
        if not self.access_token:
            print("Aucun token d'accès disponible. Veuillez vous authentifier.")
            return False
        
        # Faire une requête pour vérifier si le token est valide
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{self.api_url}/me", headers=headers)
        
        if response.status_code != 200:
            print("Le token a expiré. Tentative de rafraîchissement...")
            return self.refresh_access_token()
        
        return True
    
    def get_organization_id(self):
        """Récupère l'ID de l'organisation de l'utilisateur ou utilise un ID par défaut"""
        if not self.access_token:
            print("Aucun token d'accès disponible.")
            return
        
        # Vérifier si l'ID de l'organisation est défini dans les variables d'environnement
        org_id_from_env = os.getenv("LINKEDIN_ORGANIZATION_ID")
        if org_id_from_env:
            self.organization_id = org_id_from_env
            print(f"ID de l'organisation depuis .env: {self.organization_id}")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Récupérer les informations du profil de l'utilisateur
        try:
            response = requests.get(f"{self.api_url}/me", headers=headers)
            if response.status_code != 200:
                print(f"Erreur lors de la récupération de l'ID utilisateur: {response.text}")
                # Si nous ne pouvons pas obtenir l'ID de l'utilisateur, utiliser un ID personnel par défaut
                self.organization_id = None
                print("Aucun ID d'organisation trouvé. Les publications seront faites en tant qu'utilisateur personnel.")
                return
            
            user_id = response.json()["id"]
            # Utiliser l'ID utilisateur comme fallback si aucune organisation n'est trouvée
            self.organization_id = user_id
            print(f"Utilisation de l'ID utilisateur personnel: {user_id}")
            
            # Tenter de récupérer les organisations, mais gérer l'erreur gracieusement
            try:
                # Méthode alternative pour obtenir les organisations
                # Notez que cette approche peut également échouer selon les permissions
                response = requests.get(
                    f"{self.api_url}/organizationsPage",
                    headers=headers
                )
                
                if response.status_code == 200:
                    org_data = response.json()
                    if "elements" in org_data and len(org_data["elements"]) > 0:
                        # Prendre la première organisation
                        self.organization_id = org_data["elements"][0]["organization"]
                        print(f"ID de l'organisation: {self.organization_id}")
            except Exception as e:
                print(f"Note: Impossible de récupérer les organisations, utilisation de l'ID utilisateur personnel: {str(e)}")
        except Exception as e:
            print(f"Erreur lors de la récupération des informations utilisateur: {str(e)}")
            print("Les publications seront faites en tant qu'utilisateur personnel.")
    
    def create_data_source(self):
        """Crée une source de données vide si elle n'existe pas déjà"""
        if not os.path.exists(self.data_source_path):
            # Créer un DataFrame vide avec les colonnes nécessaires et les types appropriés
            df = pd.DataFrame({
                "title": pd.Series(dtype='object'), 
                "description": pd.Series(dtype='object'), 
                "text": pd.Series(dtype='object'), 
                "image_url": pd.Series(dtype='object'), 
                "scheduled_time": pd.Series(dtype='object'), 
                "published_time": pd.Series(dtype='object'),
                "status": pd.Series(dtype='object'),
                "attempts": pd.Series(dtype='int'),
                "post_id": pd.Series(dtype='object')  
            })
            
            # Sauvegarder le DataFrame dans un fichier CSV
            df.to_csv(self.data_source_path, index=False)
            print(f"Source de données créée: {self.data_source_path}")
        else:
            # Si le fichier existe, vérifier et ajouter les colonnes manquantes
            df = pd.read_csv(self.data_source_path, sep=';', on_bad_lines='skip')
            columns_added = False
            
            # Vérifier et ajouter les colonnes requises si elles n'existent pas
            required_columns = {"published_time": 'object', "attempts": 'int', "post_id": 'object'}
            for column, dtype in required_columns.items():
                if column not in df.columns:
                    if column == "attempts":
                        df[column] = 0
                    else:
                        df[column] = None
                        # Convertir explicitement au bon type
                        df[column] = df[column].astype(dtype)
                    columns_added = True
            
            # Sauvegarder si des colonnes ont été ajoutées
            if columns_added:
                df.to_csv(self.data_source_path, index=False)
                print(f"Source de données mise à jour avec de nouvelles colonnes: {self.data_source_path}")
            else:
                print(f"Source de données existante: {self.data_source_path}")

    def extract_content_from_newsletter(self):
        """Extrait le contenu COMPLET des projets de la newsletter HTML"""
        try:
            print(f"Tentative d'ouverture du fichier: {self.newsletter_path}")
            
            try:
                with open(self.newsletter_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                    print(f"Fichier lu avec succès en utf-8, {len(html_content)} caractères")
            except UnicodeDecodeError as e:
                print(f"Erreur d'encodage: {str(e)}")
                print("Tentative avec latin-1...")
                with open(self.newsletter_path, 'r', encoding='latin-1') as file:
                    html_content = file.read()
                    print(f"Fichier lu avec succès en latin-1, {len(html_content)} caractères")
            
        
            
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
                
                # Nettoyer le chemin de l'image (supprimer les préfixes comme "img/")
                if image_url:
                    # Extraire juste le nom du fichier
                    image_filename = os.path.basename(image_url)
                    print(f"Image détectée pour '{title}': {image_filename}")
                else:
                    image_filename = ""
                    print(f"Attention: Aucune image trouvée pour '{title}'")
                
                # Si nous avons un ID de projet, trouver le contenu complet SANS LIMITATION
                full_content = ""
                if project_id:
                    project_content = soup.select_one(project_id)
                    if project_content:
                        # Extraire tous les paragraphes du contenu sans limite
                        paragraphs = project_content.find_all(['p', 'h2', 'h3', 'li'])
                        full_content = "\n\n".join([p.get_text().strip() for p in paragraphs])
                        
                        # Si aucun contenu n'est trouvé, utiliser le contenu brut du projet
                        if not full_content and project_content.get_text():
                            full_content = project_content.get_text().strip()
                
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
            print("Contenu complet extrait sans limitation de paragraphes")
            return projects
            
        except Exception as e:
            print(f"Erreur lors de l'extraction du contenu: {str(e)}")
            return []
    
    def schedule_posts_from_newsletter(self, start_date=None):
        """Planifie les publications quotidiennes à partir de la newsletter (du lundi au samedi)"""
        projects = self.extract_content_from_newsletter()
        
        if not projects:
            print("Aucun projet trouvé pour la planification")
            return
        
        # Limiter à 6 projets maximum (pour une semaine lundi-samedi)
        if len(projects) > 6:
            print(f"Plus de 6 projets trouvés. Limitation aux 6 premiers.")
            projects = projects[:6]
        
        # Charger ou créer la source de données
        self.create_data_source()
        df = pd.read_csv(self.data_source_path, sep=';')
        
        # Filtrer les projets déjà planifiés (par titre)
        existing_titles = df['title'].tolist()
        new_projects = [p for p in projects if p['title'] not in existing_titles]
        
        if not new_projects:
            print("Tous les projets ont déjà été planifiés")
            return
        
        # Si start_date est fourni, utiliser cette date comme point de départ
        if start_date:
            try:
                # Convertir la chaîne de date en objet date
                if isinstance(start_date, str):
                    start_date = datetime.strptime(start_date, "%d/%m/%Y").date()
                next_monday = start_date
                print(f"Publication programmée à partir du {next_monday.strftime('%d/%m/%Y')}")
            except Exception as e:
                print(f"Erreur lors de la conversion de la date: {str(e)}")
                return
        else:
            # Trouver le prochain lundi (si aujourd'hui c'est lundi, on prend aujourd'hui)
            today = datetime.now().date()
            days_to_monday = today.weekday()  # 0 pour lundi, 6 pour dimanche
            
            if days_to_monday == 0:  # Si c'est déjà lundi
                next_monday = today
            else:
                # Calculer le prochain lundi
                days_until_next_monday = 7 - days_to_monday
                next_monday = today + timedelta(days=days_until_next_monday)
            
            print(f"Publication programmée à partir du lundi {next_monday.strftime('%d/%m/%Y')}")
        
        # Liens requis à ajouter dans chaque post
        portfolio_link = "https://siasia-dev.github.io/portfolio-newsletter/latest.html"
        cope_article_link = "https://www.linkedin.com/posts/alexiafontaine_cope-automatisation-publication-activity-7330679825759629312-NRxC?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEDfj0gBaOFTY0lVtTs3t1ahlxyJYQYs1Nk"
        
        for i, project in enumerate(new_projects):
            # Calculer la date de publication (du lundi au samedi)
            publish_date = next_monday + timedelta(days=i)
            
            # Heure de publication: entre 9h et 11h du matin
            hour = random.randint(9, 11)
            minute = random.randint(0, 59)
            publish_datetime = datetime.combine(publish_date, datetime.min.time().replace(hour=hour, minute=minute))
            
            # Déterminer le jour de la semaine en français
            jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
            jour_semaine = jours_semaine[publish_date.weekday()]
            
            # Formater la date et l'heure pour l'affichage
            date_formatee = publish_datetime.strftime('%d/%m/%Y')
            heure_formatee = publish_datetime.strftime('%H:%M')
            
            # Sélectionner une accroche différente pour chaque post
            accroche = ACCROCHES[i % len(ACCROCHES)]

            # Ajouter des émojis aléatoires pour rendre le post plus attractif
            emojis = ["✨", "🚀", "🔍", "💡", "⭐", "🌟", "📱", "💻", "📊", "📈", "🎯"]
            random_emoji1, random_emoji2 = random.sample(emojis, 2)
            enhanced_title = f"{random_emoji1} {project['title']} {random_emoji2}"

            # Construire l'en-tête du post avec l'accroche
            post_header = f"{accroche}\n\n{enhanced_title}"

            # Préparer le texte du post LinkedIn avec les liens requis
            portfolio_link_text = f"\n\n➡️ Consultez notre newsletter complète: {portfolio_link}"
            cope_link_text = f"\n\n🔍 Découvrez notre démarche COPE d'automatisation des publications: {cope_article_link}"
            hashtags = "\n\n#portfolio #contenu #automatisation #linkedin #newsletter #cope"

            # Calculer l'espace disponible pour le contenu principal
            max_content_length = 3000 - len(post_header) - len(project['description']) - len(portfolio_link_text) - len(cope_link_text) - len(hashtags) - 30

            # Construire le post avec TOUT le contenu extrait (sans limitation)
            post_text = f"{post_header}\n\n{project['description']}\n\n{project['text']}"

            print(f"Post complet créé pour '{project['title']}' ({len(post_text)} caractères)")

            # Ajouter le contenu principal en respectant la limite
            post_text  # ← Ajoute TOUT le contenu
            if len(project['text']) > max_content_length:
                print(f"⚠️ Le contenu principal pour '{project['title']}' dépasse la limite LinkedIn")  # ← Juste un AVERTISSEMENT
            else:
                print(f"Contenu complet intégré pour '{project['title']}'")  # ← Juste un MESSAGE

            # Ajouter les liens et hashtags
            post_text += portfolio_link_text + cope_link_text + hashtags
            
            # Créer une entrée pour le nouveau post
            new_post = {
                "title": project['title'],
                "description": project['description'],
                "text": post_text,
                "image_url": project['image_url'],
                "scheduled_time": publish_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "pending",
                "jour_semaine": jour_semaine,
                "date_formatee": date_formatee,
                "heure_formatee": heure_formatee,
                "post_id" :""
            }
            
            # Ajouter le post au DataFrame
            df = pd.concat([df, pd.DataFrame([new_post])], ignore_index=True)
            
            print(f"Post planifié: {project['title']} pour le {jour_semaine} {date_formatee} à {heure_formatee}")
        
        # Sauvegarder le DataFrame mis à jour
        df.to_csv(self.data_source_path, index=False)
        print(f"{len(new_projects)} nouveaux posts ont été planifiés de lundi à samedi")

    def upload_image_to_linkedin(self, image_path):
        """Télécharge une image sur LinkedIn et retourne l'identifiant de l'actif"""
        if not self.check_and_refresh_token():
            print("Token invalide. Impossible de télécharger l'image.")
            return None
        
        # Enregistrer le chemin original
        original_path = image_path
        
        # Essayer différentes variations du chemin pour trouver l'image
        paths_to_try = [
            image_path,  # Chemin tel quel
            os.path.join(self.images_folder, os.path.basename(image_path)),  # img/filename.ext
            os.path.join(self.images_folder, image_path),  # img/path/filename.ext
            os.path.join(".", self.images_folder, os.path.basename(image_path)),  # ./img/filename.ext
            os.path.join(os.path.dirname(self.newsletter_path), "img", os.path.basename(image_path)),  # newsletter_dir/img/filename.ext
            os.path.join(os.path.dirname(self.newsletter_path), os.path.basename(image_path))  # newsletter_dir/filename.ext
        ]
        
        # Afficher tous les chemins testés
        print(f"Recherche de l'image '{os.path.basename(image_path)}' dans:")
        for i, path in enumerate(paths_to_try):
            print(f"  {i+1}. {path}" + (" ✅" if os.path.exists(path) else " ❌"))
        
        found_path = None
        for path in paths_to_try:
            if os.path.exists(path):
                found_path = path
                print(f"✅ Image trouvée: {found_path}")
                break
        
        if not found_path:
            print(f"❌ Image non trouvée après plusieurs tentatives: {original_path}")
            
            # Chercher n'importe quelle image dans le dossier img comme solution de repli
            if os.path.exists(self.images_folder) and os.path.isdir(self.images_folder):
                print(f"Recherche d'une image de remplacement dans: {self.images_folder}")
                for file in os.listdir(self.images_folder):
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        found_path = os.path.join(self.images_folder, file)
                        print(f"✅ Utilisation d'une image de remplacement: {found_path}")
                        break
            
            if not found_path:
                print("❌ Aucune image disponible. Le post sera publié sans image.")
                return None
        
        # Faire plusieurs tentatives d'upload
        for attempt in range(3):
            try:
                if attempt > 0:
                    print(f"Tentative {attempt+1}/3 d'upload de l'image...")
                
                headers = {
                    "Authorization": f"Bearer {self.access_token}",
                    "X-Restli-Protocol-Version": "2.0.0"
                }
                
                # Étape 1: Initialiser le téléchargement de l'image
                register_upload_url = f"{self.api_url}/assets?action=registerUpload"
                register_upload_body = {
                    "registerUploadRequest": {
                        "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                        "owner": f"urn:li:person:{self.organization_id}",
                        "serviceRelationships": [
                            {
                                "relationshipType": "OWNER",
                                "identifier": "urn:li:userGeneratedContent"
                            }
                        ]
                    }
                }
                
                response = requests.post(
                    register_upload_url,
                    headers=headers,
                    json=register_upload_body
                )
                
                if response.status_code != 200:
                    print(f"❌ Erreur lors de l'initialisation du téléchargement: {response.text}")
                    continue  # Essayer à nouveau
                
                # Récupérer les informations de téléchargement
                upload_data = response.json()
                asset_id = upload_data["value"]["asset"]
                upload_url = upload_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
                
                # Étape 2: Télécharger l'image
                with open(found_path, "rb") as image_file:
                    image_data = image_file.read()
                
                upload_response = requests.put(
                    upload_url,
                    data=image_data,
                    headers={
                        "Authorization": f"Bearer {self.access_token}"
                    }
                )
                
                if upload_response.status_code in (200, 201):
                    print(f"✅ Image téléchargée avec succès, asset_id: {asset_id}")
                    return asset_id
                else:
                    print(f"❌ Erreur lors du téléchargement de l'image: {upload_response.text}")
                    continue  # Essayer à nouveau
                    
            except Exception as e:
                print(f"❌ Exception lors du téléchargement de l'image: {str(e)}")
                continue  # Essayer à nouveau
        
        # Si toutes les tentatives échouent
        print("❌ Échec de toutes les tentatives d'upload d'image. Le post sera publié sans image.")
        return None

    def publish_post(self, post_data):
        """Publie un post sur LinkedIn"""
        if not self.check_and_refresh_token():
            print("Token invalide. Impossible de publier le post.")
            return False
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        # Créer le contenu du post
        post_content = {
            "author": f"urn:li:person:{self.organization_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": post_data["text"]
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        # Ajouter une image si disponible
        image_added = False
        if post_data["image_url"]:
            # Tenter de télécharger l'image sur LinkedIn
            asset_id = self.upload_image_to_linkedin(post_data["image_url"])
            
            if asset_id:
                post_content["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
                post_content["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                    {
                        "status": "READY",
                        "description": {
                            "text": post_data["title"]
                        },
                        "media": asset_id,
                        "title": {
                            "text": post_data["title"]
                        }
                    }
                ]
                image_added = True
            else:
                print(f"Impossible de télécharger l'image: {post_data['image_url']}")
        
        # Envoyer la requête pour créer le post
        response = requests.post(
            f"{self.api_url}/ugcPosts",
            headers=headers,
            json=post_content
        )
        
        # Analyser la réponse
        if response.status_code in (200, 201):
            # Récupérer l'ID du post publié si disponible
            post_id = None
            response_data = response.json()
            if "id" in response_data:
                post_id = response_data["id"]
            
            # Afficher un rapport détaillé
            print(f"\n✅ PUBLICATION RÉUSSIE: \"{post_data['title']}\"")
            print(f"   Date: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
            
            if post_id:
                print(f"   ID du post: {post_id}")
            
            if image_added:
                print(f"   Image incluse: Oui")
            else:
                print(f"   Image incluse: Non")
            
            print(f"   Longueur du texte: {len(post_data['text'])} caractères")
            print(f"   Réponse API: {response.status_code}")
            
            # Ouvrir le fichier journal pour enregistrer les succès
            with open("linkedin_publications_reussies.log", "a", encoding="utf-8") as log_file:
                if post_id:
                    log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Post publié: {post_data['title']} - ID: {post_id}\n")
                else:
                    log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Post publié: {post_data['title']}\n")
            
            return True, post_id
        else:
            # Afficher les détails de l'échec
            print(f"\n❌ ÉCHEC DE PUBLICATION: \"{post_data['title']}\"")
            print(f"   Date: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
            print(f"   Code d'erreur: {response.status_code}")
            
            try:
                error_details = response.json()
                print(f"   Détails: {json.dumps(error_details, indent=2)}")
            except:
                print(f"   Réponse: {response.text}")
            
            # Ouvrir le fichier journal pour enregistrer les échecs
            with open("linkedin_publications_echecs.log", "a", encoding="utf-8") as log_file:
                log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Échec publication: {post_data['title']} - Erreur: {response.status_code}\n")
            
            return False, None
    
    def check_pending_posts(self):
        """Vérifie s'il y a des posts en attente à publier"""
        # Charger la source de données
        try:
            df = pd.read_csv(self.data_source_path, on_bad_lines='skip', engine='python')
            
            # DEBUG - Afficher ce que pandas a vraiment lu
            print(f"📊 Shape du DataFrame: {df.shape}")
            print(f"📊 Colonnes trouvées: {list(df.columns)}")
            print(f"📊 Premières lignes:")
            print(df.head())
            
        except Exception as e:
            print(f"❌ Erreur lecture: {e}")
            return
        
        # Vérifier si 'status' existe vraiment
        if 'status' not in df.columns:
            print("❌ Colonne 'status' manquante")
            return
        
        # Filtrer les posts en attente
        pending_posts = df[
            (df["status"] == "pending") & 
            (pd.isna(df["published_time"]) | (df["published_time"] == ""))
        ]
        
        if len(pending_posts) == 0:
            print(f"{datetime.now().strftime('%H:%M:%S')} - Aucun post en attente de publication")
            return
        
        current_time = datetime.now()
        
        posts_processed = 0
        
        for index, post in pending_posts.iterrows():
            # Essayer différents formats de date pour la compatibilité
            scheduled_time = None
            date_formats = [
                "%Y-%m-%d %H:%M:%S",    # Format standard: 2025-05-26 09:07:00
                "%d/%m/%Y %H:%M",       # Format français: 26/05/2025 09:07
                "%Y-%m-%d %H:%M",       # Format sans secondes: 2025-05-26 09:07
            ]
            
            for date_format in date_formats:
                try:
                    scheduled_time = datetime.strptime(post["scheduled_time"], date_format)
                    break
                except ValueError:
                    continue
            
            if scheduled_time is None:
                print(f"❌ Format de date non reconnu pour le post '{post['title']}': {post['scheduled_time']}")
                continue
            
            # Si le temps programmé est passé, publier le post
            if scheduled_time <= current_time:
                print(f"\n{'-'*50}")
                print(f"TENTATIVE DE PUBLICATION: \"{post['title']}\"")
                print(f"Heure programmée: {scheduled_time.strftime('%d/%m/%Y à %H:%M')}")
                print(f"Heure actuelle: {current_time.strftime('%d/%m/%Y à %H:%M')}")
                print(f"{'-'*50}")
                
                # Publier le post
                success, post_id = self.publish_post(post)
                
                # Mettre à jour le statut du post
                if success:
                    df.at[index, "status"] = "published"
                    # Ajouter la date de publication réelle
                    df.at[index, "published_time"] = current_time.strftime("%Y-%m-%d %H:%M:%S")
                    # Ajouter l'ID du post
                    if post_id:
                        df.at[index, "post_id"] = post_id
                else:
                    df.at[index, "status"] = "failed"
                    # Compter les tentatives
                    if "attempts" not in df.columns:
                        df["attempts"] = 0
                    
                    df.at[index, "attempts"] = (df.at[index, "attempts"] if not pd.isna(df.at[index, "attempts"]) else 0) + 1
                    
                    # Si moins de 3 tentatives, remettre en "pending" pour réessayer plus tard
                    if df.at[index, "attempts"] < 3:
                        df.at[index, "status"] = "pending"
                        print(f"Tentative {int(df.at[index, 'attempts'])} échouée, nouvelle tentative prévue ultérieurement")
                                        
                posts_processed += 1
                
                # Sauvegarder les modifications après chaque post
                df.to_csv(self.data_source_path, index=False)
        
        # Générer un résumé de statut si aucun post n'a été traité
        if posts_processed == 0:
            # Calculer le temps restant avant la prochaine publication
            if len(pending_posts) > 0:
                next_post = pending_posts.iloc[0]
                
                # Utiliser la même logique de parsing pour le prochain post
                next_time = None
                for date_format in date_formats:
                    try:
                        next_time = datetime.strptime(next_post["scheduled_time"], date_format)
                        break
                    except ValueError:
                        continue
                
                if next_time:
                    time_left = next_time - current_time
                    
                    hours, remainder = divmod(time_left.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    
                    if time_left.days < 0:
                        print(f"{datetime.now().strftime('%H:%M:%S')} - ATTENTION: Publication en retard de {abs(time_left.days)} jours")
                    else:
                        print(f"{datetime.now().strftime('%H:%M:%S')} - Prochain post prévu dans: {time_left.days} jours, {hours:02d}:{minutes:02d}:{seconds:02d}")
                else:
                    print(f"{datetime.now().strftime('%H:%M:%S')} - Erreur: impossible de parser la date du prochain post")
   
    def run_scheduler(self):
        """Exécute le planificateur pour vérifier régulièrement les posts à publier"""
        # Afficher un résumé des posts planifiés
        self.display_posts_markdown_summary()  # Remplacer display_scheduled_posts_summary par display_posts_markdown_summary
        
        # Vérifier les posts en attente toutes les 30 minutes
        schedule.every(30).minutes.do(self.check_pending_posts)
        
        # Faire une vérification immédiate au démarrage
        self.check_pending_posts()
        
        print(f"\nPlanificateur démarré à {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
        print("Vérification des posts toutes les 30 minutes.")
        print("Appuyez sur Ctrl+C pour arrêter le planificateur.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Attendre 1 minute avant la prochaine vérification
        except KeyboardInterrupt:
            print("\nPlanificateur arrêté par l'utilisateur.")

    def display_posts_markdown_summary(self):
        """Affiche un résumé des publications planifiées au format Markdown"""
        try:
            # Charger la source de données - essayer d'abord avec le séparateur par défaut
            try:
                df = pd.read_csv(self.data_source_path, on_bad_lines='skip')
            except:
                # Si ça échoue, essayer avec le séparateur ';'
                df = pd.read_csv(self.data_source_path, sep=';', on_bad_lines='skip')
            
            # Filtrer les posts en attente
            pending_posts = df[df["status"] == "pending"].sort_values(by="scheduled_time")
            
            if len(pending_posts) == 0:
                print("Aucun post en attente de publication")
                return
            
            # Afficher le résumé au format Markdown
            print("\n# Résumé des publications planifiées\n")
            print("| Titre | Jour | Date | Heure |")
            print("|-------|------|------|-------|")
            
            # Formats de date possibles
            date_formats = [
                "%Y-%m-%d %H:%M:%S",    # Format standard: 2025-05-26 09:07:00
                "%d/%m/%Y %H:%M",       # Format français: 26/05/2025 09:07
                "%Y-%m-%d %H:%M",       # Format sans secondes: 2025-05-26 09:07
            ]
            
            for _, post in pending_posts.iterrows():
                # Utiliser les valeurs formatées stockées dans le CSV si disponibles
                jour = post.get("jour_semaine", "")
                date = post.get("date_formatee", "")
                heure = post.get("heure_formatee", "")
                
                # Si les valeurs formatées ne sont pas disponibles, les calculer
                if not jour or not date or not heure:
                    scheduled_time = None
                    
                    # Essayer différents formats de date
                    for date_format in date_formats:
                        try:
                            scheduled_time = datetime.strptime(post["scheduled_time"], date_format)
                            break
                        except ValueError:
                            continue
                    
                    if scheduled_time:
                        jour = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"][scheduled_time.weekday()]
                        date = scheduled_time.strftime('%d/%m/%Y')
                        heure = scheduled_time.strftime('%H:%M')
                    else:
                        # Si on ne peut pas parser la date, afficher les valeurs brutes
                        jour = "Format invalide"
                        date = str(post["scheduled_time"])
                        heure = ""
                
                print(f"| {post['title']} | {jour} | {date} | {heure} |")
            
            print(f"\n**Total**: {len(pending_posts)} posts planifiés\n")
        
        except Exception as e:
            print(f"Erreur lors de l'affichage du résumé: {str(e)}")


# Exemple d'utilisation
if __name__ == "__main__":
    import argparse
    
    # Créer un parser pour les arguments en ligne de commande
    parser = argparse.ArgumentParser(description='Automatisation des publications LinkedIn à partir d\'une newsletter')
    parser.add_argument('--newsletter', help='Chemin vers le fichier HTML de la newsletter', default='latest.html')
    parser.add_argument('--data', help='Chemin vers le fichier CSV de données', default='linkedin_posts.csv')
    parser.add_argument('--images', help='Chemin vers le dossier contenant les images', default='img')
    parser.add_argument('--test', action='store_true', help='Mode test (planifier sans publier)')
    parser.add_argument('--start-date', help='Date de début pour les publications (format: DD/MM/YYYY)', default=None)
    parser.add_argument('--custom-newsletter', help='Chemin vers une newsletter spécifique à utiliser pour cette exécution', default=None)
    parser.add_argument('--scheduler-only', action='store_true', help='Lancer uniquement le planificateur sans replanifier les posts')
    args = parser.parse_args()
    
    # Créer une instance de l'automatisation LinkedIn avec les paramètres spécifiés
    linkedin = LinkedInNewsletterAutomation(
        newsletter_path=args.custom_newsletter or args.newsletter,
        data_source_path=args.data,
        images_folder=args.images
    )
    
    # Pour la première utilisation, générer l'URL d'autorisation
    if not linkedin.access_token:
        auth_url = linkedin.generate_authorization_url()
        print(f"Veuillez visiter cette URL pour autoriser l'application: {auth_url}")
        
        # Après l'autorisation, LinkedIn redirigera vers votre redirect_uri avec un code
        auth_code = input("Entrez le code d'autorisation: ")
        linkedin.get_access_token(auth_code)
    
    # Si on veut juste lancer le planificateur sans replanifier les posts
    if args.scheduler_only:
        print("Mode planificateur uniquement. Les posts existants seront publiés selon leur planning.")
        # Afficher un résumé des posts planifiés
        linkedin.display_posts_markdown_summary()
        # Lancer le planificateur
        linkedin.run_scheduler()
    else:
        # Extraction et planification des posts à partir de la newsletter
        linkedin.schedule_posts_from_newsletter(args.start_date)
        
        # Afficher un résumé au format Markdown des publications planifiées
        linkedin.display_posts_markdown_summary()
        
        # En mode test, ne pas lancer le planificateur
        if args.test:
            print("Mode test activé. Planification effectuée sans lancement du planificateur.")
        else:
            # Démarrer le planificateur
            print("Démarrage du planificateur. Appuyez sur Ctrl+C pour arrêter.")
            linkedin.run_scheduler()