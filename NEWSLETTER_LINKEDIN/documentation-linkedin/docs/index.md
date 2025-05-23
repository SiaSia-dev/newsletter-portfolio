# Documentation LinkedIn Newsletter Automation

## Vue d'ensemble

LinkedInNewsletterAutomation est un outil qui automatise la publication de contenu sur LinkedIn à partir d'une newsletter HTML. Il permet d'extraire les projets de votre newsletter hebdomadaire et de planifier leur publication quotidienne sur LinkedIn, suivant le principe COPE (Create Once, Publish Everywhere).

## Fonctionnalités principales

- **Extraction automatique** du contenu à partir de newsletters HTML
- **Planification intelligente** des publications (un post par jour)
- **Support des images** pour des publications plus attrayantes
- **Publication automatique** sur LinkedIn aux dates programmées
- **Authentification OAuth** pour sécuriser l'accès à l'API LinkedIn

## Guides rapides

- [Installation](guide/installation.md)
- [Utilisation de base](guide/utilisation.md)
- [Architecture technique](technique/architecture.md)

## Commandes essentielles

```bash
# Planifier des publications à partir du prochain lundi
python linkedin_automation.py --newsletter="path/to/newsletter.html" --images="path/to/images"

# Planifier des publications à partir d'une date spécifique
python linkedin_automation.py --start-date="20/05/2025" --newsletter="path/to/newsletter.html"

# Planifier sans lancer le planificateur (mode test)
python linkedin_automation.py --test --newsletter="path/to/newsletter.html"

# Lancer uniquement le planificateur sans replanifier
python linkedin_automation.py --scheduler-only