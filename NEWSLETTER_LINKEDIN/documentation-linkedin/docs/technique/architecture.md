# Architecture

## Architecture générale

L'application est construite autour de la classe principale `LinkedInNewsletterAutomation` qui orchestre l'ensemble du processus.

```
+---------------+     +------------------+     +-------------------+     +----------------+
| Newsletter    |---->| Extraction       |---->| Planification     |---->| Publication    |
| HTML          |     | du contenu       |     | (1 post par jour) |     | sur LinkedIn   |
+---------------+     +------------------+     +-------------------+     +----------------+
```

## Composants principaux

1. **Authentification LinkedIn**
   - Gestion des tokens OAuth 2.0
   - Rafraîchissement automatique des tokens
   - Stockage sécurisé dans le fichier .env

2. **Extracteur de contenu**
   - Analyse de la newsletter HTML avec BeautifulSoup
   - Identification des projets et de leurs composants
   - Extraction des textes et chemins d'images

3. **Planificateur**
   - Organisation des publications selon un calendrier défini
   - Distribution du lundi au samedi
   - Randomisation des heures de publication

4. **Moteur de publication**
   - Interface avec l'API LinkedIn
   - Téléchargement des images
   - Formatage des posts
   - Gestion des erreurs et tentatives

5. **Système de persistence**
   - Stockage des données dans un fichier CSV
   - Reprise sur erreur
   - Journalisation des succès et échecs

## Flux de données

1. La newsletter HTML est parsée pour extraire les projets
2. Chaque projet est transformé en publication potentielle
3. Les publications sont programmées avec des dates et heures
4. Les informations sont stockées dans le fichier CSV
5. Le planificateur vérifie périodiquement les publications à effectuer
6. Les publications sont envoyées à l'API LinkedIn au moment voulu
7. Les résultats sont journalisés et le CSV est mis à jour

## Gestion des erreurs

- Tentatives multiples en cas d'échec (jusqu'à 3 par défaut)
- Journalisation détaillée des erreurs
- Mécanisme de reprise après interruption