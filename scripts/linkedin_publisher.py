import requests
import json
import logging
import os
import hashlib
import pickle
import re
from datetime import datetime
from pathlib import Path
import time
import random
import string
from bs4 import BeautifulSoup

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('linkedin_publisher')

class LinkedInPublisher:
    def __init__(self, access_token=None):
        """
        Initialise la classe de publication LinkedIn.
        
        Args:
            access_token (str, optional): Token d'accès LinkedIn. 
                                          Si non fourni, tentera de le récupérer des variables d'environnement.
        """
        # Récupérer le token d'accès
        self.access_token = access_token or os.environ.get('LINKEDIN_ACCESS_TOKEN') or os.environ.get('DEPLOY_TOKEN')
        
        # Nettoyer et valider le token
        if self.access_token:
            self.access_token = self.access_token.strip()
            
        if not self.access_token:
            logger.error("Token d'accès LinkedIn non trouvé")
            raise ValueError("Token d'accès LinkedIn requis")
            
        # Vérifier que le token n'est pas expiré ou invalide
        if not self._validate_token():
            logger.error("Token d'accès LinkedIn invalide ou expiré")
            raise ValueError("Token d'accès LinkedIn invalide ou expiré")
        
        # Récupérer les ID de publication
        self.person_id = os.environ.get('LINKEDIN_PERSON_ID')
        self.org_id = os.environ.get('LINKEDIN_ORG_ID')
        
        # Valider les ID
        if not self.person_id and not self.org_id:
            logger.error("Aucun ID de publication LinkedIn trouvé")
            raise ValueError("ID de personne ou d'organisation LinkedIn requis")
        
        # Gestion du cache des publications
        self.cache_dir = Path('./.linkedin_cache')
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / 'published_posts.pkl'
        
        # Charger les hachages des publications précédentes
        self.published_hashes = self._load_published_hashes()

    def _validate_token(self):
        """
        Vérifie si le token d'accès est valide.
        
        Returns:
            bool: True si le token est valide, False sinon
        """
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        try:
            # Utiliser une API simple pour vérifier le token
            response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
            
            if response.status_code == 200:
                logger.info("Token LinkedIn valide")
                return True
            elif response.status_code == 401:
                logger.error(f"Token LinkedIn non autorisé: {response.text}")
                return False
            else:
                logger.warning(f"Vérification du token LinkedIn: statut {response.status_code} - {response.text}")
                # En cas de doute, on continue (peut-être un problème temporaire)
                return True
                
        except Exception as e:
            logger.error(f"Erreur lors de la vérification du token LinkedIn: {e}")
            return False

    def _load_published_hashes(self):
        """
        Charge les hachages des publications précédentes depuis le fichier de cache.
        
        Returns:
            set: Ensemble des hachages de publications précédentes
        """
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                logger.warning(f"Erreur lors du chargement du cache: {e}")
                return set()
        return set()

    def _save_published_hash(self, content_hash):
        """
        Sauvegarde le hachage d'une publication dans le fichier de cache.
        
        Args:
            content_hash (str): Hachage du contenu de la publication
        """
        self.published_hashes.add(content_hash)
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.published_hashes, f)
        except Exception as e:
            logger.warning(f"Erreur lors de la sauvegarde du cache: {e}")

    def _generate_content_hash(self, text):
        """
        Génère un hachage unique pour le contenu de la publication.
        
        Args:
            text (str): Contenu textuel de la publication
        
        Returns:
            str: Hachage MD5 du contenu
        """
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def is_duplicate(self, text):
        """
        Vérifie si une publication est un doublon.
        
        Args:
            text (str): Contenu textuel de la publication
        
        Returns:
            bool: True si le contenu est un doublon, False sinon
        """
        content_hash = self._generate_content_hash(text)
        return content_hash in self.published_hashes

    def make_unique(self, text):
        """
        Rend le contenu unique en ajoutant un horodatage et un identifiant aléatoire.
        
        Args:
            text (str): Contenu original de la publication
        
        Returns:
            str: Contenu modifié avec un horodatage et un identifiant unique
        """
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Générer un identifiant aléatoire de 8 caractères
        random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"{text}\n\nPublié le {timestamp} [ID:{random_id}]"

    def publish_text_post(self, text, public_url, force_unique=False):
        """
        Publie un post texte sur LinkedIn sur plusieurs cibles.
        
        Args:
            text (str): Le texte à publier
            public_url (str): URL publique de la newsletter
            force_unique (bool): Force l'ajout d'un horodatage pour rendre le contenu unique
        
        Returns:
            dict: Réponse de l'API LinkedIn ou None en cas d'échec
        """
        # Préparer les auteurs
        authors = {}
        if self.person_id:
            authors['person'] = self.person_id
        if self.org_id:
            authors['organization'] = self.org_id

        # Gestion du contenu dupliqué
        original_text = text
        
        if force_unique:
            text = self.make_unique(text)
        elif self.is_duplicate(text):
            logger.warning("Contenu en double détecté, ajout d'un horodatage")
            text = self.make_unique(text)
        
        # Configuration de l'API
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        # Stocker les résultats des publications
        publication_results = {}
        
        # Publier pour chaque auteur
        for author_type, author_id in authors.items():
            # Préparer le corps de la requête
            post_data = {
                "author": f"urn:li:{author_type}:{author_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "ARTICLE",
                        "media": [
                            {
                                "status": "READY",
                                "originalUrl": public_url,
                                "title": {
                                    "text": "Newsletter Portfolio"
                                },
                                "description": {
                                    "text": "Découvrez mes derniers projets et réalisations"
                                }
                            }
                        ]
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            # Tentatives de publication avec gestion des erreurs
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    post_url = "https://api.linkedin.com/v2/ugcPosts"
                    
                    # Journalisation de la requête
                    logger.info(f"Envoi de la requête POST à {post_url} pour {author_type} {author_id}")
                    
                    # Envoi de la requête
                    response = requests.post(post_url, headers=headers, json=post_data)
                    
                    # Gestion des différents codes de réponse
                    if response.status_code == 201:
                        logger.info(f"Publication réussie sur LinkedIn pour {author_type} {author_id}")
                        
                        # Sauvegarder le hachage du contenu
                        content_hash = self._generate_content_hash(original_text)
                        self._save_published_hash(content_hash)
                        
                        publication_results[author_type] = response.json()
                        break
                    
                    elif response.status_code == 429:  # Rate limit
                        retry_count += 1
                        wait_time = min(2 ** retry_count, 60)  # Exponential backoff
                        logger.warning(f"Rate limit atteint pour {author_type}, nouvelle tentative dans {wait_time} secondes...")
                        time.sleep(wait_time)
                    
                    elif response.status_code == 422:  # Duplicate content
                        # Rendre le contenu unique avec un ID aléatoire et réessayer
                        random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                        text = f"{original_text}\n\nPublié le {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} [ID:{random_id}]"
                        post_data['specificContent']['com.linkedin.ugc.ShareContent']['shareCommentary']['text'] = text
                        retry_count += 1
                        logger.warning(f"Contenu en double détecté pour {author_type}, nouvelle tentative avec un texte modifié...")
                    
                    else:
                        logger.error(f"Échec de la publication LinkedIn pour {author_type}: {response.status_code} - {response.text}")
                        publication_results[author_type] = None
                        break
                        
                except Exception as e:
                    logger.error(f"Erreur lors de la publication sur LinkedIn pour {author_type}: {e}")
                    retry_count += 1
                    if retry_count < max_retries:
                        logger.info(f"Nouvelle tentative {retry_count}/{max_retries} pour {author_type}...")
                        time.sleep(5)
                    else:
                        publication_results[author_type] = None
                        break
        
        # Vérifier si au moins une publication a réussi
        if any(publication_results.values()):
            return publication_results
        else:
            logger.error("Échec de toutes les publications LinkedIn")
            return None

def main():
    """
    Fonction principale pour générer et publier la newsletter sur LinkedIn.
    
    Returns:
        bool: True si la publication est réussie, False sinon
    """
    try:
        # Vérifier si c'est déjà publié aujour(d'hui
        lock_file = Path('./.linkedin_cache/daily_lock')
        lock_file.parent.mkdir(exist_ok=True)
        
        # Si le fichier existe et a été créé aujourd'hui, on arrête
        if lock_file.exists():
            file_date = datetime.fromtimestamp(lock_file.stat().st_mtime)
            today = datetime.now()
            if file_date.date() == today.date():
                logger.info("Une publication a déjà été effectuée aujourd'hui. Publication ignorée.")
                return True
        
        # Récupérer le répertoire des newsletters
        newsletters_dir = os.environ.get('NEWSLETTERS_DIR', '.')
        
        logger.info(f"Recherche des fichiers de newsletter dans {newsletters_dir}")
        
        # Vérifier l'existence du répertoire
        if not os.path.exists(newsletters_dir):
            logger.error(f"Le répertoire {newsletters_dir} n'existe pas")
            return False
            
        # Lister le contenu du répertoire
        all_files = os.listdir(newsletters_dir)
        logger.info(f"Fichiers trouvés: {all_files}")
        
        # Recherche du fichier HTML le plus récent (priorité à latest.html)
        if 'latest.html' in all_files:
            latest_html = 'latest.html'
            logger.info("Utilisation de latest.html pour la publication")
        else:
            # Chercher les fichiers newsletter_*.html
            newsletter_files = [f for f in all_files if f.startswith('newsletter_') and f.endswith('.html')]
            
            if not newsletter_files:
                logger.error("Aucun fichier HTML de newsletter trouvé")
                return False
            
            # Trier par date de modification (le plus récent en premier)
            latest_html = sorted(
                newsletter_files, 
                key=lambda f: os.path.getmtime(os.path.join(newsletters_dir, f)), 
                reverse=True
            )[0]
        
        logger.info(f"Dernier fichier de newsletter trouvé: {latest_html}")
        
        # URL publique de la newsletter
        username = os.environ.get('GITHUB_USERNAME', 'SiaSia-dev')
        repo_name = os.environ.get('GITHUB_REPO', 'newsletter-portfolio')
        public_url = f"https://{username}.github.io/{repo_name}/{latest_html}"
        logger.info(f"URL publique : {public_url}")
        
        # Lire le contenu du fichier HTML
        html_path = os.path.join(newsletters_dir, latest_html)
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extraire le titre et la date
        title = soup.find('h1').text.strip() if soup.find('h1') else "Newsletter Portfolio"
        
        # Recherche de la date dans le titre ou dans un paragraphe contenant une date
        date_in_title = re.search(r'\d{1,2}/\d{1,2}/\d{4}', title)
        if date_in_title:
            date_text = date_in_title.group(0)
        else:
            date = soup.find('p', string=lambda s: s and ('/' in s))
            date_text = date.text.strip() if date else datetime.now().strftime("%d/%m/%Y")
        
        # Extraire les titres des projets
        project_titles = (
            [h2.text.strip() for h2 in soup.find_all('h2', class_='project-title')] or
            [h2.text.strip() for h2 in soup.select('.project-card h2')] or
            [h2.text.strip() for h2 in soup.find_all('h2')][:5]  # Limiter aux 5 premiers
        )
        
        # Créer le contenu de la publication LinkedIn
        post_text = f"""🚀 {title} - {date_text} 🚀

Découvrez mes derniers projets et réalisations dans cette nouvelle édition de ma newsletter portfolio !

📌 Au sommaire:
"""
        # Ajouter les titres des projets
        for proj_title in project_titles:
            post_text += f"- {proj_title}\n"

        post_text += f"""
👉 Consultez la version complète pour plus de détails sur chaque projet.

#portfolio #developpeur #tech #projets #newsletter"""
        
        # Ajouter un ID unique à chaque publication
        random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        post_text += f" {random_id}"
        
        # Créer l'instance LinkedIn Publisher et publier
        publisher = LinkedInPublisher()
        result = publisher.publish_text_post(post_text, public_url, force_unique=True)
        
        if result:
            logger.info("Newsletter publiée avec succès sur LinkedIn")
            # Créer le fichier de verrou quotidien pour éviter les publications multiples
            with open(lock_file, 'w') as f:
                f.write(f"Publication effectuée le {datetime.now()}")
            return True
        else:
            logger.error("Échec de la publication sur LinkedIn")
            return False
    
    except Exception as e:
        logger.error(f"Erreur générale: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit_code = 0 if success else 1
    logger.info(f"Script terminé. Code de sortie: {exit_code}")
    exit(exit_code)
