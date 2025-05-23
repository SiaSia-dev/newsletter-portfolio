"""
Script pour publier sur LinkedIn newsletter hebdomadaire
"""

import os
import requests
import logging
from datetime import datetime
import random
import string

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('simple_linkedin')

def publish_simple_post():
    """Publie un post simple sur LinkedIn avec message engageant"""
    
    # Configuration
    access_token = os.environ.get('LINKEDIN_ACCESS_TOKEN')
    #company_id = os.environ.get('LINKEDIN_COMPANY_ID')
    person_id = os.environ.get('LINKEDIN_PERSON_ID')

    if not access_token or not person_id:
        logger.error("Token LinkedIn ou Person ID manquant")
        return False
    
    # Message simple et engageant avec identifiant unique
    date_str = datetime.now().strftime("%d/%m/%Y")
    unique_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    # Messages variants pour éviter les doublons
    messages = [
        f"""📰 Newsletter SlowSia - {date_str}

🔍 Explorez mes derniers projets et réflexions numériques dans cette nouvelle édition.

Entre innovation, créativité et horizons technologiques.

👀 Découvrez la newsletter complète :
https://siasia-dev.github.io/portfolio-newsletter/latest.html

#newsletter #projets #innovation #tech #portfolio #{unique_suffix}""",

        f"""🌟 Nouvelle édition SlowSia - {date_str}

📚 Récits visuels, horizons numériques : un voyage entre créativité et innovation.

💡 Articles variés sur l'innovation technologique et les projets créatifs.

🔗 Lien : https://siasia-dev.github.io/portfolio-newsletter/latest.html

#innovation #tech #creative #digital #portfolio #{unique_suffix}""",

        f"""📊 SlowSia Newsletter - {date_str}

🎯 Au carrefour de la technologie et de la créativité, explorez de nouveaux horizons numériques.

✨ Une sélection de projets et analyses pour cette semaine.

👉 https://siasia-dev.github.io/portfolio-newsletter/latest.html

#tech #innovation #projets #newsletter #creation #{unique_suffix}"""
    ]
    
    # Sélectionner un message aléatoire
    message = random.choice(messages)
    
    # Données du post simple (pas d'image pour éviter les complications)
    post_data = {
        "author": f"urn:li:person:{person_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    # Headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    # Publication
    try:
        response = requests.post(
            'https://api.linkedin.com/v2/ugcPosts',
            headers=headers,
            json=post_data
        )
        
        if response.status_code == 201:
            logger.info("✅ Post publié avec succès sur LinkedIn")
            return True
        else:
            logger.error(f"❌ Erreur LinkedIn: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur: {e}")
        return False
    
    

if __name__ == "__main__":
    success = publish_simple_post()
    exit(0 if success else 1)