# Utilisation de base

## Préparation de votre newsletter

L'outil attend une newsletter au format HTML avec une structure spécifique :

- Chaque projet doit être dans un élément avec la classe `.project-card`
- Le titre doit être dans un élément avec la classe `.project-title`
- La description doit être dans un élément avec la classe `.project-description`
- L'image doit être dans un élément avec la classe `.project-image`

## Commandes principales

### 1. Planification standard (du lundi au samedi)

```bash
python linkedin_automation.py --newsletter="chemin/vers/newsletter.html" --images="chemin/vers/images"
```

Cette commande va :
- Extraire jusqu'à 6 projets de votre newsletter
- Les planifier pour publication du lundi au samedi suivant
- Lancer le planificateur pour publier automatiquement

### 2. Planification à partir d'une date spécifique

```bash
python linkedin_automation.py --start-date="20/05/2025" --newsletter="chemin/vers/newsletter.html" --images="chemin/vers/images"
```

Utilisez cette option pour démarrer la publication à une date précise.

### 3. Mode test (sans publication)

```bash
python linkedin_automation.py --test --newsletter="chemin/vers/newsletter.html" --images="chemin/vers/images"
```

Ce mode planifie les publications mais ne lance pas le planificateur, utile pour vérifier que tout est correctement configuré.

### 4. Lancer uniquement le planificateur

```bash
python linkedin_automation.py --scheduler-only
```

Utilisez cette option pour démarrer le planificateur sans replanifier de publications, idéal pour reprendre après un arrêt de l'ordinateur.

## Résumé des publications planifiées

Après planification, l'outil affiche un tableau récapitulatif :

```
# Résumé des publications planifiées

| Titre | Jour | Date | Heure |
|-------|------|------|-------|
| Projet A | Lundi | 26/05/2025 | 11:21 | 
| Projet B | Mardi | 27/05/2025 | 10:45 |
| Projet C | Mercredi | 28/05/2025 | 09:30 |
...

Total: 6 posts planifiés
```