# Planificateur Windows

## Configuration comme tâche planifiée Windows

Pour que l'application s'exécute automatiquement au démarrage ou à des moments précis, vous pouvez utiliser le Planificateur de tâches Windows.

## Étape 1 : Créer un script batch

Créez un fichier batch (.bat) qui lancera votre script Python. Ouvrez un éditeur de texte et créez un fichier `run_linkedin_automation.bat` avec le contenu suivant :

```batch
@echo off
cd C:\Chemin\Vers\Votre\Dossier
call venv\Scripts\activate
python linkedin_automation.py --newsletter="C:\Chemin\Vers\Votre\Newsletter.html" --images="C:\Chemin\Vers\Vos\Images"
```

Sauvegardez ce fichier dans un emplacement facilement accessible.

## Étape 2 : Configurer le Planificateur de tâches

1. Appuyez sur la touche Windows + R, tapez `taskschd.msc` et appuyez sur Entrée
2. Dans le menu de droite, cliquez sur "Créer une tâche de base..."
3. Donnez un nom à votre tâche (par exemple, "LinkedIn Automation") et une description, puis cliquez sur "Suivant"

4. Choisissez quand vous voulez que la tâche démarre :
   - "Au démarrage de l'ordinateur" si vous voulez qu'elle s'exécute automatiquement à chaque démarrage
   - "Quotidiennement" si vous voulez qu'elle s'exécute à une heure précise chaque jour
   - Cliquez sur "Suivant"

5. Si vous avez choisi "Quotidiennement", spécifiez l'heure de démarrage (par exemple, 8h00 du matin)

6. Sélectionnez "Démarrer un programme" et cliquez sur "Suivant"

7. Parcourez et sélectionnez le fichier batch que vous avez créé (`run_linkedin_automation.bat`)

8. Cliquez sur "Terminer"

## Étape 3 : Modifier les paramètres avancés de la tâche

1. Trouvez votre tâche dans la bibliothèque du Planificateur de tâches
2. Faites un clic droit sur la tâche et sélectionnez "Propriétés"
3. Dans l'onglet "Général", cochez "Exécuter avec les privilèges les plus élevés"
4. Dans l'onglet "Conditions", décochez "Démarrer la tâche seulement si l'ordinateur est branché" si vous utilisez un portable
5. Dans l'onglet "Paramètres", cochez "Si la tâche est déjà en cours d'exécution, la règle suivante s'applique :" et sélectionnez "Ne pas démarrer une nouvelle instance"
6. Cliquez sur "OK" pour sauvegarder les modifications

## Scénarios d'utilisation

### 1. Exécution au démarrage de Windows

Idéal si vous souhaitez que le planificateur fonctionne en permanence sur votre machine. Configuration recommandée :
- Déclencheur : Au démarrage de l'ordinateur
- Action : Exécuter `run_linkedin_automation.bat`
- Utilisez le paramètre `--scheduler-only` si les posts sont déjà planifiés

### 2. Planification hebdomadaire automatique

Pour automatiser complètement le processus chaque semaine :
- Déclencheur : Hebdomadaire (par exemple, chaque dimanche à 18h00)
- Action : Exécuter `run_linkedin_automation.bat` 
- Le script extraira la nouvelle newsletter et planifiera les posts pour la semaine suivante

### 3. Reprise après arrêt imprévu

En cas d'arrêt inattendu de l'ordinateur, la tâche redémarrera automatiquement au prochain démarrage et reprendra la publication des posts planifiés.

## Vérification du fonctionnement

Pour vérifier que la tâche planifiée fonctionne correctement :
1. Exécutez manuellement la tâche en cliquant droit sur celle-ci et en sélectionnant "Exécuter"
2. Consultez l'historique d'exécution de la tâche pour voir si elle s'est bien déroulée
3. Vérifiez les journaux d'application pour confirmer l'activité du script