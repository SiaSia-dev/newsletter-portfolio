# Publication LinkedIn

## Processus de publication

Le système de publication interagit avec l'API LinkedIn pour poster le contenu au moment programmé.

## Flux de publication

1. Le planificateur vérifie périodiquement s'il y a des publications à effectuer
2. Pour chaque publication dont l'heure est arrivée :
   - L'image est téléchargée sur LinkedIn si présente
   - Le post est créé avec le texte et l'image
   - Le résultat est enregistré dans le CSV et les logs

## Méthode de vérification des posts en attente

```python
def check_pending_posts(self):
    """Vérifie s'il y a des posts en attente à publier"""
    # Charger la source de données
    df = pd.read_csv(self.data_source_path)
    
    # Filtrer les posts en attente
    pending_posts = df[df["status"] == "pending"]
    
    current_time = datetime.now()
    
    for index, post in pending_posts.iterrows():
        scheduled_time = datetime.strptime(post["scheduled_time"], "%Y-%m-%d %H:%M:%S")
        
        # Si le temps programmé est passé, publier le post
        if scheduled_time <= current_time:
            # Publier le post
            success = self.publish_post(post)
            
            # Mettre à jour le statut du post
            if success:
                df.at[index, "status"] = "published"
                df.at[index, "published_time"] = current_time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                # Gestion des erreurs et tentatives
                df.at[index, "attempts"] = (df.at[index, "attempts"] if not pd.isna(df.at[index, "attempts"]) else 0) + 1
                
                # Si moins de 3 tentatives, remettre en "pending"
                if df.at[index, "attempts"] < 3:
                    df.at[index, "status"] = "pending"
                else:
                    df.at[index, "status"] = "failed"
```

## Méthode de publication

```python
def publish_post(self, post_data):
    """Publie un post sur LinkedIn"""
    # Vérifier et rafraîchir le token
    if not self.check_and_refresh_token():
        return False
    
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
    if post_data["image_url"]:
        asset_id = self.upload_image_to_linkedin(post_data["image_url"])
        if asset_id:
            # Configuration du post avec image
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
    
    # Envoyer la requête à l'API LinkedIn
    response = requests.post(
        f"{self.api_url}/ugcPosts",
        headers=headers,
        json=post_content
    )
    
    # Traiter la réponse
    if response.status_code in (200, 201):
        # Succès
        print(f"\n✅ PUBLICATION RÉUSSIE: \"{post_data['title']}\"")
        return True
    else:
        # Échec
        print(f"\n❌ ÉCHEC DE PUBLICATION: \"{post_data['title']}\"")
        return False
```

## Téléchargement d'images

Le processus de téléchargement d'images sur LinkedIn se fait en deux étapes :

1. **Enregistrement de l'upload** : Obtention d'une URL pour le téléchargement
2. **Téléchargement de l'image** : Envoi des données de l'image à l'URL obtenue

```python
def upload_image_to_linkedin(self, image_path):
    """Télécharge une image sur LinkedIn et retourne l'identifiant de l'actif"""
    # Construire le chemin complet vers l'image
    if not os.path.isabs(image_path):
        image_path = os.path.join(self.images_folder, image_path)
    
    # Vérifier si l'image existe
    if not os.path.exists(image_path):
        print(f"Image non trouvée: {image_path}")
        return None
    
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
    
    # Récupérer l'URL de téléchargement
    upload_data = response.json()
    asset_id = upload_data["value"]["asset"]
    upload_url = upload_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
    
    # Étape 2: Télécharger l'image
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    
    upload_response = requests.put(
        upload_url,
        data=image_data,
        headers=headers
    )
    
    if upload_response.status_code in (200, 201):
        print(f"Image téléchargée avec succès, asset_id: {asset_id}")
        return asset_id
    else:
        print(f"Erreur lors du téléchargement de l'image: {upload_response.text}")
        return None
```

## Gestion des erreurs

- Tentatives multiples en cas d'échec (jusqu'à 3 par défaut)
- Journalisation des échecs avec les détails de l'erreur
- Mécanisme de reprise plus tard pour les posts échoués