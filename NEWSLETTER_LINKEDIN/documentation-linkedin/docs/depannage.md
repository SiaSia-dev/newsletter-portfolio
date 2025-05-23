# Dépannage

## Problèmes courants et solutions

Ce guide vous aidera à résoudre les problèmes les plus fréquents rencontrés lors de l'utilisation de l'outil d'automatisation LinkedIn.

## Problèmes d'authentification

### Erreur : "Aucun token d'accès disponible"

**Cause** : Le fichier `.env` n'existe pas ou ne contient pas les informations d'identification correctes.

**Solution** :
1. Vérifiez que le fichier `.env` existe à la racine du projet
2. Assurez-vous qu'il contient les variables suivantes :
   ```
   LINKEDIN_CLIENT_ID=votre_client_id
   LINKEDIN_CLIENT_SECRET=votre_client_secret
   LINKEDIN_REDIRECT_URI=votre_uri_de_redirection
   ```
3. Exécutez à nouveau le script avec l'option `--test`

### Erreur : "Le token a expiré"

**Cause** : Le token d'accès OAuth a expiré et n'a pas pu être rafraîchi automatiquement.

**Solution** :
1. Supprimez les variables `LINKEDIN_ACCESS_TOKEN` et `LINKEDIN_REFRESH_TOKEN` du fichier `.env`
2. Relancez le script pour obtenir un nouveau token :
   ```bash
   python linkedin_automation.py --test
   ```
3. Suivez les instructions pour autoriser à nouveau l'application

## Problèmes d'extraction de contenu

### Erreur : "Erreur lors de l'extraction du contenu"

**Cause** : La newsletter HTML n'a pas pu être lue ou ne contient pas la structure attendue.

**Solution** :
1. Vérifiez que le chemin vers la newsletter est correct
2. Assurez-vous que le fichier HTML est valide et encodé en UTF-8
3. Confirmez que la structure HTML contient les classes attendues :
   - `.project-card`
   - `.project-title`
   - `.project-description`
   - `.project-image`

### Erreur : "Aucun projet trouvé pour la planification"

**Cause** : L'extraction n'a trouvé aucun élément correspondant aux sélecteurs CSS.

**Solution** :
1. Ouvrez la newsletter HTML et vérifiez que les éléments ont les bonnes classes CSS
2. Si la structure est différente, modifiez les sélecteurs dans `extract_content_from_newsletter()` pour correspondre à votre HTML

## Problèmes de publication

### Erreur : "Image non trouvée"

**Cause** : Le chemin vers l'image est incorrect ou l'image n'existe pas.

**Solution** :
1. Vérifiez que le dossier d'images est correctement spécifié avec `--images`
2. Assurez-vous que les noms de fichiers dans la newsletter correspondent aux fichiers dans le dossier d'images
3. Vérifiez que les images sont dans un format supporté (JPG, PNG)

### Erreur : "ÉCHEC DE PUBLICATION" avec code d'erreur 401

**Cause** : Problème d'authentification avec l'API LinkedIn.

**Solution** :
1. Rafraîchissez votre token comme indiqué ci-dessus
2. Vérifiez que votre application LinkedIn dispose des bonnes permissions (w_member_social, w_organization_social)

### Erreur : "ÉCHEC DE PUBLICATION" avec code d'erreur 429

**Cause** : Vous avez atteint la limite de requêtes de l'API LinkedIn.

**Solution** :
1. Attendez quelques heures avant de réessayer
2. Réduisez la fréquence des publications

## Problèmes de planificateur

### Le planificateur s'arrête après la fermeture du terminal

**Cause** : Le processus est lié au terminal.

**Solution** :
1. Utilisez les méthodes d'exécution en arrière-plan décrites dans [Déploiement en local](local.md)
2. Configurez une tâche planifiée Windows comme décrit dans [Planificateur Windows](windows.md)

### Les publications ne se font pas aux heures prévues

**Cause** : Le planificateur n'est pas en cours d'exécution au moment prévu.

**Solution** :
1. Assurez-vous que l'ordinateur est allumé aux heures de publication prévues
2. Vérifiez que le script est en cours d'exécution (utilisez le Gestionnaire des tâches)
3. Consultez les fichiers journaux pour identifier d'éventuelles erreurs

## Problèmes de fichiers CSV

### Erreur : "Impossible d'ouvrir le fichier CSV"

**Cause** : Problème de permission ou fichier ouvert dans un autre programme.

**Solution** :
1. Fermez tout programme qui pourrait utiliser le fichier (Excel, etc.)
2. Vérifiez que vous avez les droits d'écriture dans le dossier
3. Si le problème persiste, spécifiez un autre chemin avec `--data`

## Comment obtenir plus d'informations de débogage

Pour obtenir plus d'informations sur les erreurs :

1. Consultez les fichiers journaux :
   - `linkedin_publications_reussies.log`
   - `linkedin_publications_echecs.log`

2. Exécutez le script en mode verbose (si implémenté) :
   ```bash
   python linkedin_automation.py --verbose
   ```

3. Vérifiez manuellement le fichier CSV pour voir l'état des publications :
   ```bash
   cat linkedin_posts.csv
   ```

Si vous rencontrez un problème qui n'est pas répertorié ici, n'hésitez pas à ouvrir une issue sur le dépôt GitHub du projet.