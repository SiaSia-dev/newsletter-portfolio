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

def get_newsletter_content():
    """Récupère le même contenu que dans l'issue"""
    import requests
    from bs4 import BeautifulSoup
    
    url = "https://siasia-dev.github.io/portfolio-newsletter/latest.html"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Même extraction que dans le YML
        sections = [
            "LLM function calls don't scale; code orchestration is simpler, more effective de Jiquan Ngiam",
            "MCP = Méta-API ?", 
            "L'information obligée d'être créative",
            "Implémentation de la stratégie COPE (Create Once, Publish Everywhere)",
            "Architecture Modulaire à Base de Contenu",
            "Méréologie comme cadre d'analyse"
        ]
        
        content = ""
        for i, section in enumerate(sections, 1):
            if "LLM function" in section:
                desc = "Retour d'expérience et proposition pour l'orchestration MCP"
            elif "MCP" in section:
                desc = "MCP est un orchestrateur d'API"
            elif "information" in section:
                desc = "La segmentation du web conduit à de nouvelles formes de régulation de l'information"
            elif "COPE" in section:
                desc = "Mise en place d'un système \"Create Once, Publish Everywhere\""
            elif "Architecture" in section:
                desc = "L'Architecture Modulaire à Base de Contenu"
            else:
                desc = "La méréologie comme cadre d'analyse"
            
            content += f"**{i}. {section}**\n{desc}\n\n"
        
        return content
        
    except:
        return "Articles sur l'innovation technologique."


def publish_simple_post():
    """Publie un post simple sur LinkedIn avec message engageant"""
    
    # Configuration
    access_token = os.environ.get('LINKEDIN_ACCESS_TOKEN')
    company_id = os.environ.get('LINKEDIN_COMPANY_ID')
    #person_id = os.environ.get('LINKEDIN_PERSON_ID')

    if not access_token or not company_id:
        logger.error("Token LinkedIn ou Company ID manquant")
        return False
    
    # Message simple et engageant avec identifiant unique
    date_str = datetime.now().strftime("%d/%m/%Y")
    unique_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    newsletter_content = get_newsletter_content()

    message = f"""📰 Newsletter Portfolio - {date_str}

    La newsletter de cette semaine est arrivée !

    🔗 Liens principaux
    - Version complète: https://siasia-dev.github.io/portfolio-newsletter/latest.html
    - Archives: https://siasia-d ev.github.io/portfolio-newsletter/archives.html

    📋 Contenu de la newsletter

    {newsletter_content}"""
   
    
    # Données du post simple (pas d'image pour éviter les complications)
    post_data = {
        "author": f"urn:li:company:{company_id}",
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