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

# Charger les variables d'environnement
load_dotenv()

class LinkedInNewsletterAutomation:
    def __init__(self, newsletter_path="./latest.html", data_source_path="NEWSLETTER LINKEDIN\data_source", images_folder="/img"):
        # Identifiants API LinkedIn (à stocker dans un fichier .env)
        self.client_id = os.getenv("LINKEDIN_CLIENT_ID")
        self.client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
        self.redirect_uri = os.getenv("LINKEDIN_REDIRECT_URI")
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.refresh_token = os.getenv("LINKEDIN_REFRESH_TOKEN")
        
        # URL de base pour l'API LinkedIn
        self.api_url = "https://api.linkedin.com/v2"
        
        # Chemin vers la source de données (CSV)
        self.data_source_path = data_source_path 
        
        # Chemin vers le fichier HTML de la newsletter
        self.newsletter_path = newsletter_path 
        
        # Dossier contenant les images
        self.images_folder = images_folder or "img"
        
        # Obtenir l'ID de l'organisation (pour les pages d'entreprise)
        self.organization_id = None
        
        # Vérifier si le token est valide, sinon le rafraîchir
        self.check_and_refresh_token()
        
        # Initialiser l'ID de l'organisation
        self.get_organization_id()
    
    def generate_authorization_url(self):
        """Génère l'URL pour l'autorisation OAuth"""
        auth_url = "https://www.linkedin.com/oauth/v2/authorization"
        scope = "r_liteprofile r_emailaddress w_member_social w_organization_social rw_organization_admin"
        
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
        """Récupère l'ID de l'organisation de l'utilisateur"""
        if not self.access_token:
            print("Aucun token d'accès disponible.")
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Récupérer l'ID de l'utilisateur actuel
        response = requests.get(f"{self.api_url}/me", headers=headers)
        if response.status_code != 200:
            print(f"Erreur lors de la récupération de l'ID utilisateur: {response.text}")
            return
        
        user_id = response.json()["id"]
        
        # Récupérer les organisations administrées par l'utilisateur
        response = requests.get(
            f"{self.api_url}/organizationAcls?q=roleAssignee&roleAssignee=urn:li:person:{user_id}",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"Erreur lors de la récupération des organisations: {response.text}")
            return
        
        org_data = response.json()
        
        if "elements" in org_data and len(org_data["elements"]) > 0:
            # Prendre la première organisation
            org_urn = org_data["elements"][0]["organization"]
            self.organization_id = org_urn.split(":")[-1]
            print(f"ID de l'organisation: {self.organization_id}")
        else:
            print("Aucune organisation trouvée pour cet utilisateur.")
    
    def create_data_source(self):
        """Crée une source de données vide si elle n'existe pas déjà"""
        if not os.path.exists(self.data_source_path):
            # Créer un DataFrame vide avec les colonnes nécessaires
            df = pd.DataFrame(columns=[
                "title", 
                "description", 
                "text", 
                "image_url", 
                "article_url", 
                "scheduled_time", 
                "published_time",
                "status",
                "attempts",
                "post_id"
            ])
            
            # Sauvegarder le DataFrame dans un fichier CSV
            df.to_csv(self.data_source_path, index=False)
            print(f"Source de données créée: {self.data_source_path}")
        else:
            # Si le fichier existe, vérifier et ajouter les colonnes manquantes
            df = pd.read_csv(self.data_source_path)
            columns_added = False
            
            # Vérifier et ajouter les colonnes requises si elles n'existent pas
            required_columns = ["published_time", "attempts", "post_id"]
            for column in required_columns:
                if column not in df.columns:
                    df[column] = None if column != "attempts" else 0
                    columns_added = True
            
            # Sauvegarder si des colonnes ont été ajoutées
            if columns_added:
                df.to_csv(self.data_source_path, index=False)
                print(f"Source de données mise à jour avec de nouvelles colonnes: {self.data_source_path}")
            else:
                print(f"Source de données existante: {self.data_source_path}")

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
                
                # Nettoyer le chemin de l'image (supprimer les préfixes comme "img/")
                if image_url:
                    # Extraire juste le nom du fichier
                    image_filename = os.path.basename(image_url)
                
                # Si nous avons un ID de projet, trouver le contenu complet
                full_content = ""
                if project_id:
                    project_content = soup.select_one(project_id)
                    if project_content:
                        # Extraire tous les paragraphes du contenu
                        paragraphs = project_content.find_all(['p', 'h2', 'h3', 'li'])
                        full_content = "\n\n".join([p.get_text().strip() for p in paragraphs[:5]])  # Limiter à 5 paragraphes
                
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
    
    def schedule_posts_from_newsletter(self):
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
        df = pd.read_csv(self.data_source_path)
        
        # Filtrer les projets déjà planifiés (par titre)
        existing_titles = df['title'].tolist()
        new_projects = [p for p in projects if p['title'] not in existing_titles]
        
        if not new_projects:
            print("Tous les projets ont déjà été planifiés")
            return
        
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
        
        for i, project in enumerate(new_projects):
            # Calculer la date de publication (du lundi au samedi)
            publish_date = next_monday + timedelta(days=i)
            
            # Heure de publication: entre 9h et 11h du matin
            hour = random.randint(9, 11)
            minute = random.randint(0, 59)
            publish_datetime = datetime.combine(publish_date, datetime.min.time().replace(hour=hour, minute=minute))
            
            # Préparer le texte du post LinkedIn
            # LinkedIn limite la longueur du texte, alors nous tronquons si nécessaire
            post_text = f"{project['title']}\n\n{project['description']}\n\n"
            
            # Ajouter une partie du contenu principal (en limitant à ~1000 caractères)
            if len(project['text']) > 800:
                post_text += project['text'][:800] + "...\n\n#portfolio #contenu"
            else:
                post_text += project['text'] + "\n\n#portfolio #contenu"
            
            # Créer une entrée pour le nouveau post
            new_post = {
                "title": project['title'],
                "description": project['description'],
                "text": post_text,
                "image_url": project['image_url'],
                "article_url": "",  # Pas d'article externe
                "scheduled_time": publish_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "pending"
            }
            
            # Ajouter le post au DataFrame
            df = pd.concat([df, pd.DataFrame([new_post])], ignore_index=True)
            
            jour_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"][publish_date.weekday()]
            print(f"Post planifié: {project['title']} pour le {jour_semaine} {publish_datetime.strftime('%d/%m/%Y à %H:%M')}")
        
        # Sauvegarder le DataFrame mis à jour
        df.to_csv(self.data_source_path, index=False)
        print(f"{len(new_projects)} nouveaux posts ont été planifiés de lundi à samedi")
    
    def upload_image_to_linkedin(self, image_path):
        """Télécharge une image sur LinkedIn et retourne l'identifiant de l'actif"""
        if not self.check_and_refresh_token():
            print("Token invalide. Impossible de télécharger l'image.")
            return None
        
        # Vérifier si le chemin est relatif à notre dossier d'images
        if not os.path.isabs(image_path):
            # Si le chemin commence par "/" ou "\" mais n'est pas absolu, le nettoyer
            if image_path.startswith('/') or image_path.startswith('\\'):
                image_path = image_path.lstrip('/\\')
            
            # Construire le chemin complet en utilisant le dossier d'images
            image_path = os.path.join(self.images_folder, image_path)
        
        # Vérifier si l'image existe
        if not os.path.exists(image_path):
            print(f"Image non trouvée: {image_path}")
            return None
        
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
            print(f"Erreur lors de l'initialisation du téléchargement: {response.text}")
            return None
        
        # Récupérer les informations de téléchargement
        upload_data = response.json()
        asset_id = upload_data["value"]["asset"]
        upload_url = upload_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        
        # Étape 2: Télécharger l'image
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        
        upload_response = requests.put(
            upload_url,
            data=image_data,
            headers={
                "Authorization": f"Bearer {self.access_token}"
            }
        )
        
        if upload_response.status_code in (200, 201):
            print(f"Image téléchargée avec succès, asset_id: {asset_id}")
            return asset_id
        else:
            print(f"Erreur lors du téléchargement de l'image: {upload_response.text}")
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
            "author": f"urn:li:organization:{self.organization_id}",
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
                log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Post publié: {post_data['title']}\n")
            
            return True
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
            
            return False
    
    def check_pending_posts(self):
        """Vérifie s'il y a des posts en attente à publier"""
        # Charger la source de données
        df = pd.read_csv(self.data_source_path)
        
        # Filtrer les posts en attente
        pending_posts = df[df["status"] == "pending"]
        
        if len(pending_posts) == 0:
            print(f"{datetime.now().strftime('%H:%M:%S')} - Aucun post en attente de publication")
            return
        
        current_time = datetime.now()
        
        posts_processed = 0
        
        for index, post in pending_posts.iterrows():
            scheduled_time = datetime.strptime(post["scheduled_time"], "%Y-%m-%d %H:%M:%S")
            
            # Si le temps programmé est passé, publier le post
            if scheduled_time <= current_time:
                print(f"\n{'-'*50}")
                print(f"TENTATIVE DE PUBLICATION: \"{post['title']}\"")
                print(f"Heure programmée: {scheduled_time.strftime('%d/%m/%Y à %H:%M')}")
                print(f"Heure actuelle: {current_time.strftime('%d/%m/%Y à %H:%M')}")
                print(f"{'-'*50}")
                
                # Publier le post
                success = self.publish_post(post)
                
                # Mettre à jour le statut du post
                if success:
                    df.at[index, "status"] = "published"
                    # Ajouter la date de publication réelle
                    df.at[index, "published_time"] = current_time.strftime("%Y-%m-%d %H:%M:%S")
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
                next_time = datetime.strptime(next_post["scheduled_time"], "%Y-%m-%d %H:%M:%S")
                time_left = next_time - current_time
                
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                if time_left.days < 0:
                    print(f"{datetime.now().strftime('%H:%M:%S')} - ATTENTION: Publication en retard de {abs(time_left.days)} jours")
                else:
                    print(f"{datetime.now().strftime('%H:%M:%S')} - Prochain post prévu dans: {time_left.days} jours, {hours:02d}:{minutes:02d}:{seconds:02d}")
    
    def run_scheduler(self):
        """Exécute le planificateur pour vérifier régulièrement les posts à publier"""
        # Afficher un résumé des posts planifiés
        self.display_scheduled_posts_summary()
        
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
    
    def display_scheduled_posts_summary(self):
        """Affiche un résumé des posts planifiés"""
        try:
            # Charger la source de données
            df = pd.read_csv(self.data_source_path)
            
            # Compter les posts par statut
            pending_count = len(df[df["status"] == "pending"])
            published_count = len(df[df["status"] == "published"])
            failed_count = len(df[df["status"] == "failed"])
            
            print("\n" + "="*50)
            print("RÉSUMÉ DES PUBLICATIONS LINKEDIN")
            print("="*50)
            print(f"Total des posts: {len(df)}")
            print(f"Posts en attente: {pending_count}")
            print(f"Posts publiés: {published_count}")
            print(f"Posts en échec: {failed_count}")
            
            if pending_count > 0:
                print("\nPROCHAINS POSTS PROGRAMMÉS:")
                pending_posts = df[df["status"] == "pending"].sort_values(by="scheduled_time")
                
                for i, post in pending_posts.head(5).iterrows():
                    scheduled_time = datetime.strptime(post["scheduled_time"], "%Y-%m-%d %H:%M:%S")
                    jour_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"][scheduled_time.weekday()]
                    print(f"- {post['title']} → {jour_semaine} {scheduled_time.strftime('%d/%m/%Y à %H:%M')}")
                
                if len(pending_posts) > 5:
                    print(f"...et {len(pending_posts) - 5} autres posts")
            
            print("="*50 + "\n")
            
        except Exception as e:
            print(f"Erreur lors de l'affichage du résumé: {str(e)}")
            # Si le fichier n'existe pas encore, c'est normal
            pass

# Exemple d'utilisation
if __name__ == "__main__":
    import argparse
    
    # Créer un parser pour les arguments en ligne de commande
    parser = argparse.ArgumentParser(description='Automatisation des publications LinkedIn à partir d\'une newsletter')
    parser.add_argument('--newsletter', help='Chemin vers le fichier HTML de la newsletter', default='newsletter_20250516.html')
    parser.add_argument('--data', help='Chemin vers le fichier CSV de données', default='linkedin_posts.csv')
    parser.add_argument('--images', help='Chemin vers le dossier contenant les images', default='img')
    parser.add_argument('--test', action='store_true', help='Mode test (planifier sans publier)')
    args = parser.parse_args()
    
    # Créer une instance de l'automatisation LinkedIn avec les paramètres spécifiés
    linkedin = LinkedInNewsletterAutomation(
        newsletter_path=args.newsletter,
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
    
    # Extraction et planification des posts à partir de la newsletter
    linkedin.schedule_posts_from_newsletter()
    
    # En mode test, ne pas lancer le planificateur
    if args.test:
        print("Mode test activé. Planification effectuée sans lancement du planificateur.")
    else:
        # Démarrer le planificateur
        print("Démarrage du planificateur. Appuyez sur Ctrl+C pour arrêter.")
        linkedin.run_scheduler()
