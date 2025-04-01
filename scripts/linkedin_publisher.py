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

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('linkedin_publisher')

class LinkedInPublisher:
    # [Reste du code identique jusqu'à la fonction main]
    
    def __init__(self, access_token=None):
        # Même code qu'avant
        # ...
        # [Le reste de la classe reste identique]
        
    # Toutes les autres méthodes restent identiques
    # ...


    def main():
        """
        Fonction principale pour générer et publier la newsletter sur LinkedIn.
        Publication hebdomadaire au lieu de quotidienne.
        
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
            
            # [Le reste du code reste identique]
            # ...
            
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