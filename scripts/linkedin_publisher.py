import requests
import json
import logging
import os
import hashlib
import pickle
import re
from datetime import datetime, timedelta
from pathlib import Path
import time
import random
import string
from bs4 import BeautifulSoup
import base64

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
        
        # Récupérer les ID de publication (avec rétrocompatibilité)
        self.member_id = os.environ.get('LINKEDIN_MEMBER_ID') or os.environ.get('LINKEDIN_PERSON_ID')
        self.company_id = os.environ.get('LINKEDIN_COMPANY_ID') or os.environ.get('LINKEDIN_ORG_ID')
        
        # Validation des ID (assurer qu'ils ne sont pas None)
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
            list: Liste des hachages de publications précédentes avec leurs timestamps
        """
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                logger.warning(f"Erreur lors du chargement du cache: {e}")
                return []
        return []

    def _save_published_hash(self, content_hash, author_type):
        """
        Sauvegarde le hachage d'une publication dans le fichier de cache.
        
        Args:
            content_hash (str): Hachage du contenu
            author_type (str): Type d'auteur (person ou organization)
        """
        # Nettoyer les hachages anciens de plus d'une semaine
        current_time = datetime.now()
        self.published_hashes = [
            (hash_val, timestamp, author) 
            for hash_val, timestamp, author in self.published_hashes 
            if current_time - timestamp < timedelta(days=7)
        ]
        
        # Ajouter le nouveau hachage avec le type d'auteur
        self.published_hashes.append((content_hash, current_time, author_type))
        
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

    def is_duplicate(self, text, author_type=None):
        """
        Vérifie si une publication est un doublon avec une tolérance temporelle et par type d'auteur.
        
        Args:
            text (str): Contenu textuel de la publication
            author_type (str, optional): Type d'auteur (person ou organization)
        
        Returns:
            bool: True si un doublon existe, False sinon
        """
        content_hash = self._generate_content_hash(text)
        current_time = datetime.now()
        
        # Filtrer les hachages par type d'auteur si spécifié
        filtered_hashes = [
            (hash_val, timestamp, author) 
            for hash_val, timestamp, author in self.published_hashes 
            if current_time - timestamp < timedelta(days=7) 
            and (author_type is None or author == author_type)
        ]
        
        # Vérifier si un hachage identique existe pour ce type d'auteur
        for existing_hash, _, _ in filtered_hashes:
            if existing_hash == content_hash:
                return True
        
        return False
    
    def _generate_variant_message(self, title, date, project_titles, variant=0, include_random=True):
        """
        Génère une variante du message selon un modèle spécifique.
        Ajoute un contenu unique à chaque génération.
        
        Args:
            title (str): Titre de la newsletter
            date (str): Date de la newsletter
            project_titles (list): Liste des titres de projets
            variant (int): Numéro de variante (0-3)
            include_random (bool): Inclure un identifiant aléatoire
            
        Returns:
            str: Texte de la publication formaté selon le modèle
        """
        # Générer un identifiant vraiment unique basé sur le timestamp actuel
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        unique_id = f"{timestamp}-{random_id}"
        
        # Créer une phrase invisible (presque) pour LinkedIn
        # Utiliser des caractères Unicode de largeur zéro et des espaces sans chasse
        invisible_unique = ''.join([f"​{c}​" for c in unique_id])  # Utilise le caractère Unicode "joindre sans largeur" (U+200B)
        
        # Plusieurs variantes de texte pour la même information
        variants = [
            # Variante 0 - Standard
            lambda: f"""🚀 {title} - {date} 🚀

Découvrez mes derniers projets et réalisations dans cette nouvelle édition de ma newsletter portfolio !

📌 Au sommaire:
{chr(10).join([f"- {t}" for t in project_titles])}

👉 Consultez la version complète pour plus de détails sur chaque projet.

#portfolio #developpeur #tech #projets #newsletter {invisible_unique}""",
            
            # Variante 1 - Réorganisée
            lambda: f"""📰 Newsletter Portfolio ({date}) : {title} 📰
{invisible_unique}
{chr(10).join([f"✅ {t}" for t in project_titles])}

Nouvelle édition disponible ! Cliquez sur le lien pour découvrir en détail tous ces projets passionnants.

#developpeur #portfolio #coding #tech""",
            
            # Variante 2 - Plus personnelle
            lambda: f"""Bonjour à tous ! Je viens de publier ma dernière newsletter ({date}) :

"{title}" {invisible_unique}

Elle présente mes projets récents :
{chr(10).join([f"• {t}" for t in project_titles])}

N'hésitez pas à consulter la version complète ! #tech #dev #portfolio""",
            
            # Variante 3 - Direct et concis
            lambda: f"""NOUVELLE NEWSLETTER 📱💻 - {date}

{title}

Projets inclus :
{chr(10).join([f">> {t}" for t in project_titles])}

Lien vers la version complète ci-dessous 👇
#developpement #portfolio {invisible_unique}"""
        ]
        
        # Utiliser la variante demandée ou une variante aléatoire si hors limites
        variant_index = variant if 0 <= variant < len(variants) else random.randint(0, len(variants) - 1)
        return variants[variant_index]()

    def publish_text_post(self, title, date, project_titles, public_url, force_unique=False, skip_cache=False):
        """
        Publie un post texte sur LinkedIn sur plusieurs cibles.
        
        Args:
            title (str): Titre de la newsletter
            date (str): Date de la newsletter
            project_titles (list): Liste des titres de projets
            public_url (str): URL publique de la newsletter
            force_unique (bool): Force l'utilisation d'un texte unique
            skip_cache (bool): Ignore la vérification du cache
            
        Returns:
            dict: Réponse de l'API LinkedIn ou None en cas d'échec
        """
        # Préparer les auteurs
        authors = {}
        if self.person_id:
            authors['person'] = self.person_id
        if self.org_id:
            authors['organization'] = self.org_id
            
        # Vérifier qu'il y a au moins un auteur valide
        if not authors:
            logger.error("Aucun ID d'auteur LinkedIn valide trouvé (person_id ou org_id)")
            return None

        # Génération du texte initial
        base_text = self._generate_variant_message(title, date, project_titles, variant=0)
        
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
            current_variant = 0
            # Tentatives de publication avec gestion des erreurs
            max_retries = 5  # Augmentation du nombre de tentatives
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    # Générer un titre et une description uniques pour l'article
                    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                    article_title = f"Newsletter Portfolio - {date} [{random_suffix}]"
                    article_desc = f"Découvrez mes derniers projets et réalisations - {datetime.now().strftime('%H:%M:%S')}"
                    
                    # Générer une variante différente à chaque tentative avec contenu invisible unique
                    text = self._generate_variant_message(
                        title, 
                        date, 
                        project_titles, 
                        variant=current_variant,
                        include_random=True
                    )
                    
                    # Générer une URL unique en ajoutant un paramètre aléatoire
                    unique_url = f"{public_url}?t={int(time.time())}&r={random.randint(1000, 9999)}"
                    
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
                                        "originalUrl": unique_url,
                                        "title": {
                                            "text": article_title
                                        },
                                        "description": {
                                            "text": article_desc
                                        }
                                    }
                                ]
                            }
                        },
                        "visibility": {
                            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                        }
                    }
                    
                    post_url = "https://api.linkedin.com/v2/ugcPosts"
                    
                    # Journalisation de la requête
                    logger.info(f"Envoi de la requête POST à {post_url} pour {author_type} {author_id} (variante {current_variant})")
                    
                    # Envoi de la requête
                    response = requests.post(post_url, headers=headers, json=post_data)
                    
                    # Gestion des différents codes de réponse
                    if response.status_code == 201:
                        logger.info(f"Publication réussie sur LinkedIn pour {author_type} {author_id}")
                        
                        # Sauvegarder le hachage du contenu
                        if not skip_cache:
                            content_hash = self._generate_content_hash(base_text)
                            self._save_published_hash(content_hash, author_type)
                        
                        publication_results[author_type] = response.json()
                        break
                    
                    elif response.status_code == 429:  # Rate limit
                        retry_count += 1
                        wait_time = min(2 ** retry_count, 60)  # Exponential backoff
                        logger.warning(f"Rate limit atteint pour {author_type}, nouvelle tentative dans {wait_time} secondes...")
                        time.sleep(wait_time)
                    
                    elif response.status_code == 422:  # Duplicate content
                        # Attendre un peu plus longtemps et essayer avec une nouvelle variante
                        current_variant = (current_variant + 1) % 4
                        retry_count += 1
                        logger.warning(f"Contenu en double détecté pour {author_type}, nouvelle tentative avec la variante {current_variant}...")
                        # Attendre plus longtemps entre les tentatives
                        time.sleep(3)
                    
                    else:
                        logger.error(f"Échec de la publication LinkedIn pour {author_type}: {response.status_code} - {response.text}")
                        # Si on a d'autres variantes à essayer, on continue
                        if retry_count < max_retries - 1:
                            current_variant = (current_variant + 1) % 4
                            retry_count += 1
                            logger.info(f"Nouvelle tentative avec la variante {current_variant}...")
                            time.sleep(3)
                        else:
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
    Publication hebdomadaire.
    
    Returns:
        bool: True si la publication est réussie, False sinon
    """
    try:
        # Vérifier si c'est déjà publié cette semaine
        lock_file = Path('./.linkedin_cache/weekly_lock')
        lock_file.parent.mkdir(exist_ok=True)
        
        # Vérifier si l'option de forçage est activée
        force_publish = os.environ.get('FORCE_LINKEDIN_PUBLISH', '').lower() in ('true', '1', 'yes')
        skip_cache = os.environ.get('SKIP_LINKEDIN_CACHE', '').lower() in ('true', '1', 'yes')
        
        # Si le fichier existe et a été créé cette semaine, on arrête (sauf si force_publish)
        if lock_file.exists() and not force_publish:
            file_date = datetime.fromtimestamp(lock_file.stat().st_mtime)
            today = datetime.now()
            
            # Calculer le début de la semaine actuelle (lundi)
            start_of_week = today - timedelta(days=today.weekday())
            start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Vérifier si la publication a été faite après le début de cette semaine
            if file_date >= start_of_week:
                logger.info("Une publication a déjà été effectuée cette semaine. Publication ignorée. Utilisez FORCE_LINKEDIN_PUBLISH=true pour forcer.")
                return True
            else:
                logger.info("La dernière publication date d'une semaine précédente. Poursuite de la publication...")

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
        
        # Chercher les fichiers newsletter_*.html
        newsletter_files = [f for f in all_files if f.startswith('newsletter_') and f.endswith('.html')]
        
        if not newsletter_files:
            # Si aucun fichier newsletter_*.html, alors seulement chercher latest.html
            if 'latest.html' in all_files:
                latest_html = 'latest.html'
                logger.info("Utilisation de latest.html car aucun fichier newsletter_*.html trouvé")
            else:
                logger.error("Aucun fichier HTML de newsletter trouvé")
                return False
        else:
            # Trier par date de modification (le plus récent en premier)
            latest_html = sorted(
                newsletter_files, 
                key=lambda f: f.replace('newsletter_', '').replace('.html', ''), 
                reverse=True
            )[0]
            logger.info(f"Dernier fichier de newsletter trouvé: {latest_html}")
        
        # URL publique de la newsletter
        username = os.environ.get('GB_USERNAME')
        repo_name = os.environ.get('GB_REPO')

        if not username or not repo_name:
            logger.error("Variables d'environnement GB_USERNAME et/ou GB_REPO non définies")
            logger.error("Veuillez définir ces variables dans votre environnement ou dans GitHub Actions")
            return False

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
        
        # Créer l'instance LinkedIn Publisher et publier
        publisher = LinkedInPublisher()
        result = publisher.publish_text_post(
            title=title, 
            date=date_text, 
            project_titles=project_titles, 
            public_url=public_url, 
            force_unique=True,
            skip_cache=skip_cache
        )
        
        if result:
            logger.info("Newsletter publiée avec succès sur LinkedIn")
            # Créer le fichier de verrou hebdomadaire pour éviter les publications multiples
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