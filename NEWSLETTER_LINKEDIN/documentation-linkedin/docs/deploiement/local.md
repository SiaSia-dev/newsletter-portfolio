# Déploiement en local

## Configuration pour une exécution locale

Pour exécuter l'outil sur votre machine locale, plusieurs approches sont possibles selon votre usage.

## 1. Exécution manuelle

C'est la méthode la plus simple pour une utilisation occasionnelle.

```bash
python linkedin_automation.py --newsletter="path/to/newsletter.html" --images="path/to/images"
```

Dans ce mode, le script s'exécutera et le planificateur restera actif jusqu'à ce que vous fermiez le terminal ou appuyiez sur Ctrl+C.

## 2. Exécution en arrière-plan

Pour que le script continue à s'exécuter même après la fermeture du terminal :

### Sous Windows

```bash
start /B python linkedin_automation.py --newsletter="path/to/newsletter.html" --images="path/to/images"
```

### Sous Linux/macOS

```bash
nohup python linkedin_automation.py --newsletter="path/to/newsletter.html" --images="path/to/images" &
```

## 3. Utilisation des versions spécialisées

### Version ponctuelle (oneshot)

Pour programmer des publications à une date spécifique :

```bash
python linkedin_automation_oneshot.py --start-date="20/05/2025" --newsletter="path/to/newsletter.html" --images="path/to/images"
```

### Lancer uniquement le planificateur

Si vous avez déjà programmé des publications et souhaitez simplement démarrer le planificateur :

```bash
python linkedin_automation.py --scheduler-only
```

## Bonnes pratiques

1. **Toujours exécuter une première fois en mode test** :
   ```bash
   python linkedin_automation.py --test --newsletter="path/to/newsletter.html" --images="path/to/images"
   ```

2. **Vérifier les logs régulièrement** :
   - `linkedin_publications_reussies.log` pour les succès
   - `linkedin_publications_echecs.log` pour les échecs

3. **Sauvegarder le fichier CSV** :
   Créez régulièrement des sauvegardes de `linkedin_posts.csv` pour éviter toute perte de données.

4. **Maintenir à jour le token d'accès** :
   Si vous utilisez l'application pendant une longue période, vérifiez que le token d'accès est toujours valide.