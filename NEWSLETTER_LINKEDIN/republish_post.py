"""
Outil avancé de republication des posts LinkedIn
Ce script permet de republier des posts LinkedIn tronqués avec leur image et les liens requis
"""

import os
import pandas as pd
import json
import requests
from datetime import datetime
import sys
import random
import re



# Essai d'importation de dotenv avec gestion d'erreur
try:
    from dotenv import load_dotenv
    # Charger les variables d'environnement depuis .env
    load_dotenv()
    print("Fichier .env chargé avec succès")
except ImportError:
    print("Package python-dotenv non trouvé. Installation recommandée: pip install python-dotenv")
    # Continuer sans dotenv

# Définir les liens qui doivent être systématiquement ajoutés
PORTFOLIO_LINK = "https://siasia-dev.github.io/portfolio-newsletter/latest.html"
COPE_ARTICLE_LINK = "https://www.linkedin.com/posts/alexiafontaine_cope-automatisation-publication-activity-7330679825759629312-NRxC?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEDfj0gBaOFTY0lVtTs3t1ahlxyJYQYs1Nk"

def manual_read_env_file():
    """Lit manuellement le fichier .env"""
    try:
        env_path = '.env'
        if os.path.exists(env_path):
            print(f"Lecture manuelle du fichier .env: {env_path}")
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ[key] = value
                        print(f"Variable chargée: {key}")
            return True
        else:
            print(f"Fichier .env non trouvé à l'emplacement: {os.path.abspath(env_path)}")
            return False
    except Exception as e:
        print(f"Erreur lors de la lecture manuelle du fichier .env: {str(e)}")
        return False

# Tenter de lire manuellement le fichier .env
if 'LINKEDIN_ACCESS_TOKEN' not in os.environ:
    manual_read_env_file()

def get_linkedin_profile_id(access_token):
    """Récupère l'ID du profil LinkedIn à partir du token d'accès"""
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("https://api.linkedin.com/v2/me", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("id")
        else:
            print(f"Erreur lors de la récupération de l'ID profil: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception lors de la récupération de l'ID profil: {str(e)}")
        return None

def upload_image_to_linkedin(image_path, access_token, person_id, img_folder="img"):
    """Télécharge une image sur LinkedIn et retourne l'identifiant de l'actif"""
    try:
        # Construire le chemin complet si nécessaire
        original_path = image_path
        
        # Essayer différentes variations du chemin
        paths_to_try = [
            image_path,  # Chemin tel quel
            os.path.join(img_folder, os.path.basename(image_path)),  # img/filename.ext
            os.path.join(img_folder, image_path),  # img/path/filename.ext
            os.path.join(".", img_folder, os.path.basename(image_path))  # ./img/filename.ext
        ]
        
        found_path = None
        for path in paths_to_try:
            if os.path.exists(path):
                found_path = path
                break
        
        if not found_path:
            print(f"Image non trouvée après plusieurs tentatives: {original_path}")
            # Chercher n'importe quelle image dans le dossier img comme fallback
            if os.path.exists(img_folder) and os.path.isdir(img_folder):
                for file in os.listdir(img_folder):
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        found_path = os.path.join(img_folder, file)
                        print(f"Utilisation d'une image de remplacement: {found_path}")
                        break
            
            if not found_path:
                return None
        
        print(f"Téléchargement de l'image: {found_path}")
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        # Étape 1: Initialiser le téléchargement de l'image
        register_upload_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
        register_upload_body = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": f"urn:li:person:{person_id}",
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
        with open(found_path, "rb") as image_file:
            image_data = image_file.read()
        
        upload_response = requests.put(
            upload_url,
            data=image_data,
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
        
        if upload_response.status_code in (200, 201):
            print(f"Image téléchargée avec succès, asset_id: {asset_id}")
            return asset_id
        else:
            print(f"Erreur lors du téléchargement de l'image: {upload_response.text}")
            return None
            
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def republish_linkedin_post(post_title, csv_path="linkedin_posts.csv", newsletter_url=None, 
                           access_token=None, person_id=None, img_folder="img", 
                           custom_content=None, include_image=True):
    """Republie un post LinkedIn avec son image d'origine et un contenu corrigé"""
    
    # URL par défaut si non fournie
    if newsletter_url is None:
        newsletter_url = PORTFOLIO_LINK
    
    try:
        # Vérifier si le fichier CSV existe
        if not os.path.exists(csv_path):
            print(f"Le fichier CSV n'existe pas: {csv_path}")
            return False
        
        # Charger les données
        df = pd.read_csv(csv_path, sep=';')
        
        # Trouver le post par son titre
        matching_posts = df[df['title'] == post_title]
        
        if len(matching_posts) == 0:
            print(f"Aucun post trouvé avec le titre: {post_title}")
            return False
        
        # Récupérer le post
        post = matching_posts.iloc[0].copy()
        
        # Information sur le post original
        print(f"\n--- INFORMATIONS SUR LE POST ORIGINAL ---")
        print(f"Titre: {post['title']}")
        print(f"Description: {post['description']}")
        print(f"Longueur du texte: {len(post['text'])} caractères")
        print(f"Status: {post['status']}")
        if 'image_url' in post and post['image_url']:
            print(f"Image: {post['image_url']}")
        
        # 1. Préparer le contenu
        title = post['title']
        description = post['description']

         # Choisir une accroche aléatoire
        # Accroches pour les posts LinkedIn
        ACCROCHES = [
            "📰 Newsletter : Après l'automatisation de la création d'une newsletter hebdomadaire, on extrait et programme la publication de ces contenus sur LinkedIn tout au long de la semaine",
            "🔄 Automatisation de contenu : De la newsletter au post LinkedIn, comment optimiser le cycle de publication de contenu",
            "📋 COPE (Create Once, Publish Everywhere) : Notre newsletter hebdomadaire se transforme automatiquement en posts LinkedIn",
            "🤖 Automatisation marketing : Comment transformer une newsletter en série de posts LinkedIn sans effort supplémentaire",
            "⚙️ Workflow optimisé : Notre newsletter alimente désormais automatiquement notre présence LinkedIn",
            "📢 Diffusion multicanal : Découvrez comment notre newsletter devient source de contenu pour LinkedIn"
        ]

        accroche = random.choice(ACCROCHES)
        
        # Ajouter des émojis aléatoires pour rendre le post plus attractif
        emojis = ["✨", "🚀", "🔍", "💡", "⭐", "🌟", "📱", "💻", "📊", "📈", "🎯"]
        random_emoji1, random_emoji2 = random.sample(emojis, 2)
        enhanced_title = f"{random_emoji1} {title} {random_emoji2}"

        # Construire l'en-tête du post avec l'accroche
        post_header = f"{accroche}\n\n{enhanced_title}"
        
        # Extraire le contenu principal du texte existant
        if custom_content:
            main_content = custom_content
        else:
            # Si le texte original contient déjà les éléments de formatage, les extraire
            original_text = post['text']
            
            # Essayer d'extraire le contenu principal si c'est une publication standardisée
            main_content = original_text
            
            # Nettoyer les sauts de ligne multiples
            while "\n\n\n" in main_content:
                main_content = main_content.replace("\n\n\n", "\n\n")

        # 2. Préparer les liens requis (à placer AVANT le nettoyage)
        portfolio_link = f"\n\n➡️ Consultez notre newsletter complète: {newsletter_url}"
        cope_link = f"\n\n🔍 Découvrez notre démarche COPE d'automatisation des publications: {COPE_ARTICLE_LINK}"
        hashtags = "\n\n#portfolio #contenu #automatisation #linkedin #newsletter"

        
        # Définir des modèles regex pour rechercher des éléments similaires
        accroche_pattern = r"^(📰|🔄|📋|🤖|⚙️|📢).*?\n\n[^a-zA-Z0-9]*.*?[^a-zA-Z0-9]*\n\n"
        portfolio_pattern = r"\n\n➡️ Consultez notre newsletter complète:.*"
        cope_pattern = r"\n\n🔍 Découvrez notre démarche COPE d'automatisation des publications:.*"
        hashtags_pattern = r"\n\n#portfolio #contenu #automatisation #linkedin #newsletter.*"

        # Nettoyer le contenu existant - d'abord l'accroche et le titre
        main_content = re.sub(accroche_pattern, "", main_content, flags=re.DOTALL)
        # Puis les liens et hashtags
        main_content = re.sub(portfolio_pattern, "", main_content)
        main_content = re.sub(cope_pattern, "", main_content)
        main_content = re.sub(hashtags_pattern, "", main_content)
        
        # Construire le texte final avec tous les éléments requis
        new_text = f"{post_header}\n\n{description}\n\n{main_content.strip()}{portfolio_link}{cope_link}{hashtags}"
        
        # Calculer la taille maximale pour respecter la limite de LinkedIn
        max_length = 3000 - len(enhanced_title) - len(description) - len(portfolio_link) - len(cope_link) - len(hashtags) - 30  # marge de sécurité
        
        if len(main_content) > max_length:
            # On garde au maximum le contenu principal
            print(f"⚠️ Le contenu principal dépasse la limite LinkedIn. Tentative d'inclusion du maximum de contenu.")
            # On ne tronque pas ici, on laisse LinkedIn le faire si nécessaire
        
        
        print(f"\nNouveau texte préparé ({len(new_text)} caractères)")
        print(f"Titre avec émojis: {enhanced_title}")
        print(f"Ajout des liens vers la newsletter et l'article COPE")
        
 
        
        # 3. Récupérer les informations d'authentification
        access_token = access_token or os.getenv("LINKEDIN_ACCESS_TOKEN")
        person_id = person_id or os.getenv("LINKEDIN_PERSON_ID") or os.getenv("LINKEDIN_ORGANIZATION_ID")
        
        if not access_token:
            print("\nERREUR: Token d'accès LinkedIn manquant.")
            return False
        
        if not person_id:
            # Récupérer l'ID du profil via l'API
            person_id = get_linkedin_profile_id(access_token)
            if not person_id:
                print("Erreur: Impossible de déterminer l'ID utilisateur LinkedIn")
                return False
            else:
                print(f"ID utilisateur LinkedIn récupéré via API: {person_id}")
        
        # 4. Préparer la requête
        api_url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        # 5. Créer le contenu du post
        post_content = {
            "author": f"urn:li:person:{person_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": new_text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        # 6. Ajouter l'image si demandé
        if include_image and 'image_url' in post and post['image_url']:
            image_path = post['image_url']
            asset_id = upload_image_to_linkedin(image_path, access_token, person_id, img_folder)
            
            if asset_id:
                # Mettre à jour le contenu du post pour inclure l'image
                post_content["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
                post_content["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                    {
                        "status": "READY",
                        "description": {
                            "text": description
                        },
                        "media": asset_id,
                        "title": {
                            "text": title
                        }
                    }
                ]
                print(f"Image ajoutée au post: {asset_id}")
        
        # 7. Envoyer la requête
        print("\nTentative de publication sur LinkedIn...")
        response = requests.post(api_url, headers=headers, json=post_content)
        
        if response.status_code in (200, 201):
            post_id = None
            try:
                response_data = response.json()
                post_id = response_data.get("id")
            except:
                pass
            
            print(f"\n✅ REPUBLICATION RÉUSSIE!")
            print(f"Date: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
            if post_id:
                print(f"ID du post: {post_id}")
                direct_url = f"https://www.linkedin.com/feed/update/{post_id}"
                print(f"URL direct: {direct_url}")
            
            # Écrire dans le fichier de log des réussites
            try:
                with open("linkedin_publications_reussies.log", "a", encoding="utf-8") as log_file:
                    log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Post republié: {post['title']}")
                    if post_id:
                        log_file.write(f" - ID: {post_id}")
                    log_file.write("\n")
            except Exception as e:
                print(f"Erreur lors de l'écriture du log de succès: {str(e)}")
            
            # 8. Mettre à jour le CSV
            index = matching_posts.index[0]
            df.at[index, "status"] = "republished"
            df.at[index, "published_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if post_id:
                if 'post_id' not in df.columns:
                    df['post_id'] = None
                    df['post_id'] = df['post_id'].astype('object')
                df.at[index, "post_id"] = post_id
            df.to_csv(csv_path, index=False)
            
            print(f"\nInformations mises à jour dans le fichier CSV: {csv_path}")
            return True
        else:
            print(f"\n❌ ÉCHEC DE REPUBLICATION")
            print(f"Code d'erreur: {response.status_code}")
            try:
                error_details = response.json()
                print(f"Détails: {json.dumps(error_details, indent=2)}")
            except:
                print(f"Réponse: {response.text}")
            # Écrire dans le fichier de log des échecs
            try:
                with open("linkedin_publications_echecs.log", "a", encoding="utf-8") as log_file:
                    log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Échec republication: {post['title']} - Erreur: {response.status_code}\n")
            except Exception as e:
                    print(f"Erreur lors de l'écriture du log d'échec: {str(e)}")
            return False
            
    except Exception as e:
        print(f"Erreur lors de la republication: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
def get_todays_posts(csv_path):
    """Récupère les posts programmés pour aujourd'hui"""
    try:
        # Vérifier si le fichier CSV existe
        if not os.path.exists(csv_path):
            print(f"Erreur: Le fichier CSV {csv_path} n'existe pas.")
            return []
        
        # Charger les données
        df = pd.read_csv(csv_path, sep=';')
        
        # Filtrer les posts en attente
        pending_posts = df[df["status"] == "pending"]
        
        if len(pending_posts) == 0:
            print("Aucun post en attente de publication")
            return []
        
        # Obtenir la date d'aujourd'hui au format YYYY-MM-DD
        today = datetime.now().date()
        today_str = today.strftime("%Y-%m-%d")
        
        # Filtrer les posts programmés pour aujourd'hui
        todays_posts = []
        for _, post in pending_posts.iterrows():
            # Extraire la date (première partie de scheduled_time)
            scheduled_time = post["scheduled_time"]
            scheduled_date = scheduled_time.split(" ")[0]
            
            if scheduled_date == today_str:
                todays_posts.append(post)
        
        if not todays_posts:
            print(f"Aucun post programmé pour aujourd'hui ({today_str})")
        else:
            print(f"\n=== Posts programmés pour aujourd'hui ({today_str}) ===")
            for i, post in enumerate(todays_posts):
                print(f"{i+1}. {post['title']} (prévu à {post['scheduled_time'].split(' ')[1]})")
            print("="*50)
        
        return todays_posts
        
    except Exception as e:
        print(f"Erreur lors de la récupération des posts du jour: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

# Utilisation directe du script
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Republier un post LinkedIn avec image et contenu corrigé")
    parser.add_argument("--title", required=True, help="Titre exact du post à republier")
    parser.add_argument("--csv", default="linkedin_posts.csv", help="Chemin vers le fichier CSV")
    parser.add_argument("--url", default=PORTFOLIO_LINK, help="URL de la newsletter")
    parser.add_argument("--token", default=None, help="Token d'accès LinkedIn")
    parser.add_argument("--user", default=None, help="ID utilisateur LinkedIn")
    parser.add_argument("--img-folder", default="img", help="Dossier contenant les images")
    parser.add_argument("--no-image", action="store_true", help="Ne pas inclure l'image originale")
    parser.add_argument("--content-file", default=None, help="Fichier contenant le contenu personnalisé")
    
    args = parser.parse_args()
    
    # Charger le contenu personnalisé s'il est spécifié
    custom_content = None
    if args.content_file and os.path.exists(args.content_file):
        try:
            with open(args.content_file, 'r', encoding='utf-8') as f:
                custom_content = f.read()
            print(f"Contenu personnalisé chargé depuis {args.content_file} ({len(custom_content)} caractères)")
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier de contenu: {str(e)}")
    
    republish_linkedin_post(
        post_title=args.title, 
        csv_path=args.csv, 
        newsletter_url=args.url,
        access_token=args.token,
        person_id=args.user,
        img_folder=args.img_folder,
        custom_content=custom_content,
        include_image=not args.no_image
    )