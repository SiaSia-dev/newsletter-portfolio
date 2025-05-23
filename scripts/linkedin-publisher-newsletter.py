"""
Publication LinkedIn d'un lien vers la newsletter.
Ce script publie un lien vers la newsletter HTML avec un message générique et unique.
"""

import os
import json
import requests
import hashlib
import pickle
import re
from datetime import datetime, timedelta
from pathlib import Path
import time
import random
import string
from bs4 import BeautifulSoup
import logging
from dotenv import load_dotenv

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
        # Charger les variables d'environnement
        load_dotenv()
        
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
        
        # Rétrocompatibilité avec les anciennes variables d'environnement
        if not self.person_id:
            self.person_id = os.environ.get('LINKEDIN_MEMBER_ID')
        if not self.org_id:
            self.org_id = os.environ.get('LINKEDIN_COMPANY_ID')
        
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

    def extract_newsletter_tags(self, newsletter_url):
        """
        Extrait les tags de la newsletter (méthode placeholder).
        
        Args:
            newsletter_url (str): URL de la newsletter
            
        Returns:
            list: Liste de tags par défaut
        """
        return ["innovation", "tech", "projets", "portfolio", "newsletter"]

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

    def _generate_unique_message(self, newsletter_url, variant=0):
        """
        Génère un message unique avec lien vers la newsletter.
        Chaque variante utilise du contenu unique et des identificateurs invisibles.
        
        Args:
            newsletter_url (str): URL publique de la newsletter
            variant (int): Numéro de variante (0-3)
            
        Returns:
            str: Texte de la publication formaté selon le modèle
        """
        # Date actuelle
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        # Générer un identifiant vraiment unique basé sur le timestamp actuel
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        unique_id = f"{timestamp}-{random_id}"
        
        # Créer une phrase invisible pour LinkedIn
        # Utiliser des caractères Unicode de largeur zéro
        invisible_unique = ''.join([f"​{c}​" for c in unique_id])
        
        # Essayer d'extraire les tags de la newsletter
        tags = self.extract_newsletter_tags(newsletter_url)
        
        # Si nous avons récupéré des tags, les utiliser pour créer des hashtags
        custom_hashtags = ""
        if tags:
            # Sélectionner quelques tags aléatoires pour plus de variété
            num_tags = min(8, len(tags))
            selected_tags = random.sample(tags, num_tags)
            custom_hashtags = " ".join([f"#{tag}" for tag in selected_tags])
        
        # Si aucun tag n'a été trouvé, utiliser des tags par défaut
        if not custom_hashtags:
            default_tags = [
                "innovation", "tech", "digital", "creation", "projets", 
                "developpement", "data", "design", "creative", "technologie",
                "showcase", "sharing", "portfolio"
            ]
            selected_default_tags = random.sample(default_tags, 5)
            custom_hashtags = " ".join([f"#{tag}" for tag in selected_default_tags])
        
        # Ajouter toujours les hashtags #projets et #newsletter
        hashtags = f"{custom_hashtags} #projets #newsletter"
        
        # Génération aléatoire d'emoji pour varier davantage
        emojis = ["🚀", "📰", "✨", "🔍", "💡", "📊", "🧠", "🌟", "📚", "🎯"]
        random_emojis = random.sample(emojis, 3)
        
        # Adjectives et synonymes pour varier les descriptions
        adjectives = [
            "nouvelle", "récente", "fraîche", "dernière", "passionnante",
            "inspirante", "créative", "innovante", "intéressante", "captivante"
        ]
        
        synonyms_newsletter = [
            "newsletter", "édition", "publication", "sélection", 
            "compilation", "collection", "curation"
        ]
        
        # Sélection aléatoire pour varier les messages
        adj = random.choice(adjectives)
        synonym = random.choice(synonyms_newsletter)
        
        # Plusieurs variantes de texte complètement différentes
        variants = [
            # Variante 0
            lambda: f"""{random_emojis[0]} {adj.capitalize()} {synonym} - {current_date} {random_emojis[1]}

Récits visuels, horizons numériques : Un voyage entre créativité et innovation.

Découvrez ma {adj} {synonym} avec une sélection de projets variés. {random_emojis[2]}

{newsletter_url}

{hashtags} {invisible_unique}""",
            
            # Variante 1
            lambda: f"""Bonjour à tous !

Je viens de publier ma {synonym} du {current_date}. {random_emojis[0]}

Au carrefour de la technologie et de la créativité, explorez avec moi de nouveaux horizons numériques. {random_emojis[1]}

Pour la consulter : {newsletter_url}

{hashtags} {invisible_unique} {random_emojis[2]}""",
            
            # Variante 2
            lambda: f"""{random_emojis[0]} {random_emojis[1]} {random_emojis[2]}

Aujourd'hui, {current_date} : ma {synonym} est en ligne !

Entre données, narrations visuelles et explorations numériques, découvrez mes derniers projets.

Lien ▶️ {newsletter_url}

{hashtags} {invisible_unique}""",
            
            # Variante 3
            lambda: f"""Edition du {current_date} {random_emojis[0]}

{invisible_unique} Une nouvelle sélection de projets est disponible dans ma {synonym} !

Explorez différentes facettes de mes travaux récents sur :
{newsletter_url}

N'hésitez pas à partager vos retours ! {random_emojis[1]} {random_emojis[2]}

{hashtags}""",
            
            # Variante 4
            lambda: f"""🔔 Nouvelle publication - {current_date}

À la croisée de la technologie et de la création, je partage avec vous ma dernière {synonym}.

{random_emojis[0]} {random_emojis[1]} {random_emojis[2]}

Rendez-vous sur : {newsletter_url}

{hashtags} {invisible_unique}"""
        ]
        
        # Utiliser la variante demandée ou une variante aléatoire si hors limites
        if variant < 0 or variant >= len(variants):
            variant = random.randint(0, len(variants) - 1)
            
        return variants[variant]()

    def publish_newsletter_link(self, newsletter_url, force_unique=False, skip_cache=False):
        """
        Publie un post texte sur LinkedIn avec un lien vers la newsletter.
        
        Args:
            newsletter_url (str): URL publique de la newsletter
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
        base_text = self._generate_unique_message(newsletter_url, variant=0)
        
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
                    # Générer une variante différente à chaque tentative avec contenu invisible unique
                    text = self._generate_unique_message(
                        newsletter_url, 
                        variant=current_variant
                    )
                    
                    # Titre pour la carte article, simple et unique
                    date_part = datetime.now().strftime("%d/%m/%Y")
                    unique_suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
                    article_title = f"Newsletter - {date_part} [{unique_suffix}]"
                    
                    # Description de la carte article avec quelques tags aléatoires pour la variété
                    tags = self.extract_newsletter_tags(newsletter_url)
                    tag_text = ""
                    if tags and len(tags) >= 3:
                        random_tags = random.sample(tags, min(3, len(tags)))
                        tag_text = f" #{' #'.join(random_tags)}"
                        
                    article_description = f"Récits visuels, horizons numériques : Un voyage entre créativité et innovation.{tag_text}"
                    
                    # Préparer le corps de la requête - Utilisation du format "article"
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
                                        "originalUrl": newsletter_url,
                                        "title": {
                                            "text": article_title
                                        },
                                        "description": {
                                            "text": article_description
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
                        current_variant = (current_variant + 1) % 5  # Nous avons maintenant 5 variantes
                        retry_count += 1
                        logger.warning(f"Contenu en double détecté pour {author_type}, nouvelle tentative avec la variante {current_variant}...")
                        # Attendre plus longtemps entre les tentatives
                        time.sleep(3)
                    
                    else:
                        logger.error(f"Échec de la publication LinkedIn pour {author_type}: {response.status_code} - {response.text}")
                        # Si on a d'autres variantes à essayer, on continue
                        if retry_count < max_retries - 1:
                            current_variant = (current_variant + 1) % 5
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
    Fonction principale pour publier le lien de la newsletter sur LinkedIn.
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

        # URL publique de la newsletter
        username = os.environ.get('GB_USERNAME', 'SiaSia-dev')
        repo_name = os.environ.get('GB_REPO', 'portfolio-newsletter')
        newsletter_url = f"https://{username}.github.io/{repo_name}/newsletter_20250523.html"
        
        # Vérification de l'URL via une requête HEAD pour s'assurer qu'elle est accessible
        try:
            response = requests.head(newsletter_url, timeout=10)
            if response.status_code >= 400:
                logger.warning(f"L'URL de la newsletter semble inaccessible: {response.status_code}")
                # On continue malgré tout car parfois les requêtes HEAD échouent alors que GET fonctionne
        except Exception as e:
            logger.warning(f"Erreur lors de la vérification de l'URL: {e}")
            # Continuer malgré l'erreur (peut-être un problème temporaire)
        
        logger.info(f"URL publique pour la publication : {newsletter_url}")
        
        # Créer l'instance LinkedIn Publisher et publier
        publisher = LinkedInPublisher()
        result = publisher.publish_newsletter_link(
            newsletter_url=newsletter_url, 
            force_unique=True,
            skip_cache=skip_cache
        )
        
        if result:
            logger.info("Lien vers la newsletter publié avec succès sur LinkedIn")
            # Créer le fichier de verrou hebdomadaire pour éviter les publications multiples
            with open(lock_file, 'w') as f:
                f.write(f"Publication effectuée le {datetime.now()}")
            return True
        else:
            logger.error("Échec de la publication du lien sur LinkedIn")
            return False
    
    except Exception as e:
        logger.error(f"Erreur générale: {e}")
        return False


if __name__ == "__main__":
    success = main()
    exit_code = 0 if success else 1
    logger.info(f"Script terminé. Code de sortie: {exit_code}")
    exit(exit_code)