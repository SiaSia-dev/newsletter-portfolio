# Installation

## Prérequis

- Python 3.6 ou supérieur
- Pip (gestionnaire de paquets Python)
- Accès à l'API LinkedIn

## Étapes d'installation

1. **Clonez le dépôt**
   ```bash
   git clone https://github.com/votre-utilisateur/linkedin-newsletter-automation.git
   cd linkedin-newsletter-automation
   ```

2. **Installez les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration de l'API LinkedIn**
   
   Pour utiliser l'API LinkedIn, vous devez créer une application sur la [Plateforme de développeurs LinkedIn](https://www.linkedin.com/developers/):
   
   - Créez une application LinkedIn Developer
   - Obtenez un Client ID et un Client Secret
   - Configurez l'URI de redirection

4. **Création du fichier .env**
   
   Créez un fichier `.env` à la racine du projet avec les informations suivantes:
   
   ```
   LINKEDIN_CLIENT_ID=votre_client_id
   LINKEDIN_CLIENT_SECRET=votre_client_secret
   LINKEDIN_REDIRECT_URI=votre_uri_de_redirection
   ```

5. **Première exécution et authentification**
   
   Lors de la première exécution, le script vous guidera pour l'authentification OAuth:
   
   ```bash
   python linkedin_automation.py --test
   ```
   
   Suivez les instructions pour autoriser l'application à accéder à votre compte LinkedIn.

## Vérification de l'installation

Pour vérifier que tout fonctionne correctement, exécutez:

```bash
python linkedin_automation.py --test
```

Si aucune erreur n'apparaît et que vous voyez le message "Mode test activé", l'installation est réussie.