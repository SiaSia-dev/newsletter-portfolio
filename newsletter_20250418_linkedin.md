# 📰 Newsletter Portfolio - 18/04/2025

## Récits visuels, horizons numériques : Un voyage entre créativité et innovation 🚀

---

### 🤖 Comment lire Reliquiae Aquitanicae ? Avatar Edouard Lartet : Agent Conversationnel Historique

![Comment lire Reliquiae Aquitanicae ? Avatar Edouard Lartet : Agent Conversationnel Historique](img/Photo-dAvatar-2.jpg)

#### Comment lire Reliquiae Aquitanicae ? Avatar Edouard Lartet : Agent Conversationnel Historique


#### Présentation du Projet "Avatar Lartet"

<img height="60" src="/img/Photo-dAvatar-2.jpg" width="50"/> <em>Un agent conversationnel basé sur un personnage historique, démontrant l'application des techniques de traitement du langage naturel (NLP) pour </em><em>créer une expérience interactive et éducative sur une oeuvre litteraire ancienne.</em>**

<em>Reliquiae Aquitanicae</em> est une oeuvre majeure en archéolgie préhistorique (et en paléontologie), d'une part, elle démontre la préhistoire comme une discipline scientifique rigoureuse et, d'autre part, elle participe à interroger les origines de l'homme, à une époque où celles-ci se fondent d'abord sur un texte religieux comme la Bible.

Cette publication, dirigée par Édouard Lartet et Henry Christy, dans les années 1865-1875, représente donc l'une des premières études scientifiques systématiques des vestiges préhistoriques du Périgord et des régions avoisinantes du sud de la France.


#### Objectifs

Le but est bien d'interroger <strong>notre manière de lire face à des oeuvres anciennes</strong> : notre rapport à la lecture a été particulièrement modifié par le numérique, et bien qu'il ne soit jamais simple de les aborder, perdre cette <em>"confrontation"</em> entre cet objet médiatisé que représente ici l'ouvrage scientifique et ceux qui le lisent serait préjudiciable, à mon sens, à <strong>notre capacité à transmettre.</strong>

Autrement dit, la lecture et son pendant l'esprit critique sont <strong>des formes de <em>mise en présence</em></strong> : il s'agit soit d'une proposition, soit d'une nécessité, d'exercer sa pensée. (<em>Vaste débat que la mise en présence du texte...</em>)

Il nous a semblé alors intéressant de créer cette sorte d'affontement (intellectuel et pacifiste!) à travers ces objectifs :

- Créer une expérience de médiation culturelle basée sur une partie du texte de Reliquiae Aquitanicae,
- Utiliser l'IA pour rendre cette histoire accessible à travers un apprentissage personnalisé,
- Permettre des interactions immersives avec un personnage historique, représenté par cet avatar, dans une notion de transmission de connaissances historiques.

#### Cadre de l'analyse

Au même titre que n'importe quelle analyse, celle-ci se base sur une méthodologie pour répondre à une problématique.

Nous avons fait appel à différents outils conceptuels comme <strong>l'ontologie et l'analyse méréologique pour organiser les informations du texte original.</strong>

<strong>L'objectif principal était une intégration explicite de l'ontologie et de la méréologie dans le processus de génération des réponses proposées par le modèle d'apprentissage.</strong>

Pourquoi ? <strong>Notre hypothèse de travail était de tester à une petite échelle si ces structures de contrôle pouvaient limiter les hallucinations (incohérences et anachronismes) en encadrant la "créativité" du modèle.</strong>

Si cette démarche vous intéresse, je vous renvoie vers mon carnet HYPOTHESES sur la plateforme OpenEdition à l'article suivant : [Architecture conceptuelle d’un avatar historique : analyse textuelle intégrant une ontologie et analyse méréologique](https://archnum.hypotheses.org/1432)

[Architecture conceptuelle d’un avatar historique : analyse textuelle intégrant une ontologie et analyse méréologique](https://archnum.hypotheses.org/1432)


#### Technologies Utilisées

- Traitement du Langage Naturel
- Python
- Streamlit

#### Lien du Projet

Il s'agit d'un prototype pour tester la création d'une base de connaissances à partir de fichiers d'ontologie et de méréologie, celui-ci sera amené à encore évoluer.

[Interagir avec l'Avatar Edouard Lartet](https://avatar-lartet.streamlit.app/)

[Interagir avec l'Avatar Edouard Lartet](https://avatar-lartet.streamlit.app/)

<em>Note: il faut un compte STREAMLIT et le temps de chargement peut être assez long.</em>


#### Fonctionnalités Principales

- Conversation contextuelle basée sur l'ouvrage d'Edouard Lartet et Henry Christy
- Réponses adaptatives et personnalisées (personnalisation contextuelle)
- Capacité à partager des informations historiques détaillées

#### Compétences mises en oeuvre

Il y a aussi de notre part l'idée d'une exploration des possibilités de l'IA générative dans ces outils :

- Développement d'agents conversationnels
- Modélisation de personnalités historiques
- Techniques avancées de NLP
- Conception d'expériences interactives éducatives

#### Référence

Lartet &amp; Christy 1865-1875, Lartet É., Christy H., Reliquiae Aquitanicae: being contributions to the archaeology and palaeontology of Perigord and the adjoining provinces of southern France; edited by Thomas Rupert Jones, London/Paris/Leipzig, Williams &amp; Norgate/J.B. Baillière/A. Brockhaus, 1865-1875, 204 p., 79 pl. h.-t.

[Retour en haut](#)


---

### 🤖 Optimisation d'un avatar conversationnel pour l'archéologie préhistorique

![Optimisation d'un avatar conversationnel pour l'archéologie préhistorique](img/Slowsia.jpg)

#### Optimisation d'un avatar conversationnel pour l'archéologie préhistorique


#### Introduction

Cet article résume un processus d'amélioration d'un système d'IA conversationnel nommé "Lartet", conçu pour simuler les interactions avec Édouard Lartet, un paléontologue et préhistorien français du 19ème siècle. Le système utilise une architecture d'apprentissage automatique pour générer des réponses informées à partir de passages de l'ouvrage "Reliquiae Aquitanicae".


#### Défis identifiés

L'analyse des logs et des réponses générées a permis d'identifier plusieurs défis:

1. Répétition de contenus: Le système intégrait le même passage dans différentes sections
1. Problèmes de traduction: La traduction automatique anglais-français produisait des textes incohérents
1. Hallucinations et substitutions inappropriées: Les noms propres étaient systématiquement remplacés par "mon collègue"
1. Absence d'utilisation de l'ontologie et de la méréologie: Malgré des structures de données riches, ces éléments n'étaient pas intégrés
1. Réponses non adaptées à certaines questions sensibles: Le système ne traitait pas correctement les questions sur Henry Christy

#### Solutions développées


#### 1. Amélioration de l'extraction d'informations

La fonction <code>extract_structured_info</code> a été optimisée pour éviter les doublons entre catégories:

```python


#### Éviter les doublons entre catégories

all_items = set()
for category in list(info.keys()):
    unique_items = []
    for item in info[category]:
        item_hash = hash(item)
        if item_hash not in all_items:
            all_items.add(item_hash)
            unique_items.append(item)
    info[category] = unique_items
```


#### 2. Gestion des questions sensibles

Une fonction spécifique a été implémentée pour traiter les questions sur Henry Christy:

<code>python
def get_christy_collaboration_response(self):
    """Fournit une réponse prédéfinie sur la collaboration avec Christy"""
    if self.language == "fr":
        return """
Je préfère ne pas m'étendre sur mes relations personnelles ou professionnelles...
"""</code>


#### 3. Restructuration du générateur de questions suggérées

La fonction <code>get_default_question</code> a été entièrement réécrite pour offrir des suggestions pertinentes sans mentionner Henry Christy:

```python
def get_default_question(self, user_input: str) -&gt; str:
    """Retourne une question par défaut basée sur la requête utilisateur."""
    query_lower = user_input.lower()

```


#### 4. Amélioration de la cohérence linguistique

Le système a été modifié pour présenter clairement les extraits en anglais tout en maintenant une structure en français:

```python


#### Note explicative sur la langue

response_parts.append("## Note sur la langue")
response_parts.append("Bien que mes publications scientifiques fussent rédigées en anglais, je vous présente ici une synthèse en français de mes travaux.")
```


#### 5. Intégration de l'ontologie et de la méréologie

Des fonctions ont été ajoutées pour exploiter les structures ontologiques et méréologiques:

<code>python
def initialize_knowledge_base(self):
    """Charge et structure l'ontologie et la méréologie"""
    self.structured_ontology = {}
    self.structured_mereology = {}
    # Traitement des données...</code>


#### Résultats

Les modifications ont permis d'obtenir:

1. Des réponses plus cohérentes et sans répétitions
1. Une meilleure présentation des extraits originaux
1. Une gestion appropriée des questions sensibles
1. Une exploitation plus riche des connaissances structurées

#### Conclusion

Ce processus d'optimisation illustre les défis spécifiques de la création d'avatars historiques utilisant le RAG. Il souligne l'importance d'une adaptation fine des mécanismes de génération et de vérification pour produire des interactions authentiques et informatives.

L'amélioration de ce système démontre comment les techniques d'IA contemporaines peuvent être adaptées pour préserver et transmettre le patrimoine scientifique historique de manière interactive et engageante.

[Retour en haut](#)


---

### 🎭 Comment les analystes de données contribuent à décoder la culture organisationnelle ?

![Comment les analystes de données contribuent à décoder la culture organisationnelle ?](img/data-analyst-subcultures-map.png)

#### Comment les analystes de données contribuent à décoder la culture organisationnelle ?


#### Une analyse culturelle depuis les posts LinkedIn

Tous ces métiers de la Data porte à confusion, le paysage semble flou tant leur place dans les organisations est tout aussi récente et en cours de structuration (peut-être pas pour les grands groupes) : il est clair que cet écosystème se met en place.

De ce constat, nous avons ciblé notre réflexion sur le métier d'Analyste de Données (se rapportant à notre profil) et plus particulièrement, nous avons voulu connaître <strong>l'application d'une analyse culturelle sur ce métier.</strong>


#### Etude de cas sur le métier d'Analyste de Données

<img alt="Cartographie" src="/img/data-analyst-subcultures-map.png"/>

En extrayant les posts (français) sur LinkedIn, en référence au terme d'analyste de données, nous avons pu illustrer comment différentes sous-cultures de ce métier contribuent actuellement à façonner la culture organisationnelle des entreprises.

<em>[Approche bottom-up assistée par IA générative]</em>


#### Des approches variées selon les sous-cultures du métier

On notera par cette infographie la diversité des méthodes employées selon les différentes sous-cultures professionnelles du métier d'analyste de données.

Cette cartographie de ces sous-cultures révèle cinq profils distincts, chacun apportant une perspective à l'analyse culturelle en entreprise.


#### Business Intelligence : mesurer pour comprendre

<em>Cas concret : Au sein de grands groupes, les analystes BI créent des tableaux de bord mesurant l'adoption des valeurs RSE par département.</em>

Cette approche quantitative permet de révéler les silos culturels entre équipes traditionnelles et initiatives innovantes, offrant ainsi une base factuelle pour adapter la communication interne et mesurer l'impact des formations sur l'évolution culturelle.


#### Data Science : prédire les transformations culturelles

<em>Cas concret : Dans le contexte d'une fusion d'entreprise, les data scientists utilisent le traitement du langage naturel (NLP) pour analyser les communications internes.</em>

Cette méthode sophistiquée permet d'identifier la persistance des cultures d'origine, de prédire l'adhésion aux nouvelles valeurs par analyse de sentiment, et de proposer des interventions ciblées basées sur des clusters de profils d'employés.


#### Marketing Digital : aligner valeurs internes et externes

<em>Cas concret : Les analystes marketing corrèlent l'engagement des employés sur l'intranet aux valeurs de marque par exemple.</em>

En comparant le langage utilisé en interne avec celui des campagnes publiques, ils détectent les désalignements culturels et peuvent identifier des ambassadeurs internes selon leur adhésion démontrée aux valeurs de l'entreprise.


#### Big Data : cartographier l'évolution culturelle

<em>Cas concret : Les ingénieurs Big Data créent des data lakes intégrant emails, documents et données collaboratives sur plusieurs années.</em>

Cette approche permet de cartographier l'évolution des valeurs entre différents sites, pays et départements, fournissant des insights précieux sur la perméabilité culturelle entre équipes et l'impact des réorganisations.


#### Éthique & Gouvernance : évaluer la maturité éthique

<em>Cas concret : Les Data Protection Officers développent des indices de maturité éthique par équipe et région.</em>

Ils analysent les écarts entre la culture déclarée et les pratiques réelles de gestion des données clients, identifient les résistances culturelles aux normes RGPD et évaluent les besoins en formation sur l'éthique des données.


#### Défis méthodologiques et éthiques

L'extraction et l'analyse des données culturelles posent ici néanmoins certains défis.

L'accès aux données sur des plateformes comme LinkedIn est restreint et coûteux, nécessitant souvent des approches alternatives comme l'échantillonnage qualitatif ou les entretiens directs. Par ailleurs, les questions de confidentialité et de respect des conditions d'utilisation des plateformes doivent être prises en compte dans toute démarche d'analyse culturelle : raison pour laquelle nous avons défini l'extraction sur un terme très large comme "analyste de données".

<strong>Là encore, il s'agissait d'explorer un vaste ensemble de données comme l'est une plateforme LinkedIn qui est assez <u>révélateur de nos pratiques de travail</u>.</strong>

Et notre principale conclusion sur ce rapide tour d'horizon est qu'<strong>il semble assez opportun d'identifier les leviers de transformation culturelle les plus pertinents et d'accompagner efficacement les évolutions stratégiques des entreprises dans un contexte économique et social en perpétuelle mutation.</strong>


#### L'analyse culturelle en entreprise par les méthodes informatiques

L'analyse culturelle assistée par des méthodes informatiques représente donc aujourd'hui un levier stratégique pour les organisations souhaitant mieux comprendre leurs valeurs et convictions partagées.

En exploitant des techniques d'analyse de données avancées, les entreprises peuvent désormais interpréter et corréler divers artefacts culturels (procédures, décisions, compétences et comportements) pour obtenir une vision plus précise de leur culture organisationnelle.

[Retour en haut](#)


---

### 📌 Méthodologie Narrative de Traitement de Données

![Méthodologie Narrative de Traitement de Données](img/Slowsia.jpg)

#### Méthodologie Narrative de Traitement de Données

Chaque ensemble de données raconte une histoire. Mon approche consiste à écouter ces récits, à comprendre leurs nuances et leurs implications culturelles sous-jacentes.

Au-delà des chiffres, je recherche les fils conducteurs qui relient les données aux expériences humaines, aux dynamiques organisationnelles et aux évolutions sociétales.

Chaque donnée est située dans son écosystème : professionnel, culturel, historique. Cette approche permet de révéler des insights qui dépassent l'analyse statistique traditionnelle.

[Retour en haut](#)


---

### 🎨 architecture Modulaire pour Portfolio Digital - Une Approche Basée sur le Markdown

![architecture Modulaire pour Portfolio Digital - Une Approche Basée sur le Markdown](img/abeille.jpg)

#### architecture Modulaire pour Portfolio Digital - Une Approche Basée sur le Markdown


#### Introduction

La gestion d'un portfolio digital peut rapidement devenir complexe lorsque le contenu s'enrichit et se diversifie. L'architecture traditionnelle où le contenu est directement intégré dans le HTML pose des problèmes de maintenance et d'évolutivité. Cet article présente une approche modulaire basée sur le contenu (Content-Driven Modular Architecture) qui sépare clairement la présentation du contenu, offrant ainsi une solution élégante pour les portfolios riches en contenu.


#### Le problème du contenu monolithique

Imaginez un portfolio comme celui-ci :

```html

Présentation


#### À Propos


#### Mon Univers Créatif et Analytique

Bienvenue dans mon portfolio multidisciplinaire où convergent la créativité, la technologie et l'analyse de données. Mon approche combine des compétences en data science, storytelling, design et documentation créative pour créer des expériences narratives riches et significatives.


#### Solution : Architecture Modulaire à Base de Contenu

L'architecture modulaire à base de contenu propose de séparer le contenu (texte, images, liens) de sa présentation (HTML, CSS), en utilisant Markdown comme format de contenu.


#### Principe fondamental

La séparation contenu/présentation s'articule autour de trois composants :

1. Fichiers Markdown (.md) : Contiennent uniquement le contenu avec métadonnées (frontmatter)
1. Template HTML unique : Définit la structure et la mise en page
1. Script de chargement : Intègre dynamiquement le contenu Markdown dans le HTML

#### Structure de fichiers

<code>portfolio/
├── index.html            # Template principal avec la structure
├── css/
│   └── styles.css        # Styles CSS 
├── js/
│   └── main.js           # Scripts JavaScript (optionnel)
├── content/              # Dossier des contenus en Markdown
│   ├── about.md          # Section "À propos"
│   ├── skills.md         # Section "Compétences"
│   ├── projects/         # Sous-dossier pour les projets
│   │   ├── project1.md
│   │   └── project2.md
│   └── ...
└── img/                  # Images</code>


#### Les fichiers Markdown avec frontmatter

Voici un exemple de fichier Markdown pour la section "À propos" :


#### ```markdown

title: "À Propos"
subtitle: "Présentation"
image: "/img/abeille.jpg"


#### Une Approche Intégrée

Ma démarche s'articule autour d'une vision transversale où chaque discipline enrichit les autres...
```


#### HTML modularisé

Le fichier HTML devient un simple template qui charge dynamiquement le contenu :

```html




#### 


#### Script de chargement JavaScript

Un script JavaScript charge dynamiquement le contenu Markdown, le convertit en HTML et l'insère dans la page :

<code>``javascript
async function loadMarkdownContent(filePath, targetElementId, imageId, titleId, subtitleId) {
    // Chargement du fichier Markdown
    const response = await fetch(</code>content/${filePath}.md`);
    const mdContent = await response.text();

}

// Chargement des sections
document.addEventListener('DOMContentLoaded', function() {
    loadMarkdownContent('about', 'about-content', 'about-image', 'about-title', 'about-subtitle');
    // Chargement des autres sections...
});
```


#### Automatisation du processus

Pour simplifier encore davantage la gestion du contenu, un script Python a été développé pour :

1. Extraire la structure d'un fichier Markdown (titres, images, liens)
1. Générer un frontmatter YAML complet avec métadonnées
1. Créer des versions résumées des contenus
1. Transformer des paragraphes en listes de mots-clés
Cet outil permet de traiter les fichiers Markdown de manière cohérente et d'extraire automatiquement les métadonnées pertinentes.


#### Avantages de cette architecture

Cette approche présente de nombreux avantages :

1. Séparation du contenu et de la présentation - Le contenu est stocké indépendamment du code de l'interface
1. Composabilité - Les sections peuvent être réutilisées ou réorganisées facilement
1. Maintenabilité - Modifier un contenu n'exige pas de toucher au code HTML principal
1. Évolutivité - Ajouter une nouvelle section est aussi simple que de créer un nouveau fichier
1. Versionning efficace - Les modifications de contenu sont clairement visibles dans les commits Git
1. Workflow optimisé - Les designers peuvent travailler sur l'interface pendant que les rédacteurs créent le contenu

#### Mise en pratique

Pour mettre en place cette architecture dans votre propre portfolio :

1. Convertissez vos contenus en fichiers Markdown avec frontmatter
1. Créez un template HTML avec des conteneurs identifiés pour chaque section
1. Implémentez le script de chargement JavaScript
1. Utilisez des outils d'automatisation pour faciliter la gestion du contenu

#### Conclusion

L'architecture modulaire à base de contenu représente une évolution naturelle pour les portfolios digitaux riches en contenu. En séparant clairement le contenu de la présentation, cette approche simplifie considérablement la maintenance et l'évolution de votre portfolio, tout en offrant une grande flexibilité pour personnaliser chaque aspect de votre présence en ligne.

Cette méthode s'inscrit parfaitement dans la philosophie "Create Once, Publish Everywhere" (COPE), permettant de réutiliser le contenu sur différentes plateformes et dans différents formats sans duplication d'effort.

[Retour en haut](#)


---

### 🎭 Résumé // Lev MANOVTICH, *The Science of Culture ?* in *Cultural Analysis*

![Résumé // Lev MANOVTICH, *The Science of Culture ?* in *Cultural Analysis*](img/Slowsia.jpg)

#### Résumé // Lev MANOVTICH, *The Science of Culture ?* in *Cultural Analysis*


#### Résumé // Lev MANOVTICH, The Science of Culture ? in Cultural Analysis

L'analyse culturelle s'intéresse aux modèles qui peuvent être dérivés de l'analyse de vastes ensembles de données culturelles.
[Lien vers l'ouvrage en ligne : Cultural Analysis](https://direct.mit.edu/books/monograph/4966/Cultural-Analytics)

[Lien vers l'ouvrage en ligne : Cultural Analysis](https://direct.mit.edu/books/monograph/4966/Cultural-Analytics)

<strong>#analyse_quantitative #big_data #medias</strong>

<em>"L'idée qu'un groupe ou une personne a des comportements et des goûts culturels cohérents avait du sens dans les sociétés anciennes et modernes. Mais avec les nombreux choix culturels disponibles aujourd'hui, nous pourrions découvrir que l'idée d'un goût stable ou d'une « personnalité culturelle » stable est une illusion."</em>

➡️l'illusion du goût
➡️la classification n'est toujours pas l'explication
➡️Nouveau paradigme? D'où l'importance "<em>And here the concepts and methods of sampling, feature extraction, and exploratory data analysis are more important than data size"</em>


#### Structures cognitives & structures sociales

Nos structures cognitives sont celles de nos structures sociales (La distinction, 1979)

Pour reprendre R.MOURIEUX, <em>"Entre réalisme populaire et l'idéalisme bourgeois se situe le goût moyen des couches moyennes, fait de refus des extrêmes et de mimétisme de l'immédiat supérieur"</em> 1.https://www.persee.fr/doc/sotra_0038-0296_1980_num_22_4_1655_t1_0475_0000_2


#### Les séries de Claude Monet (1840-1926)

<em>Du 22 septembre 2010 au 24 janvier 2011 - Paris, Galeries nationales du Grand Palais</em>

➡️ Notons aussi le rapport entre <em>expérience sensible &amp; image</em> (<strong>une image est une densité de probabilités dans un espace de plus grande dimension</strong>) Remarquez que dès le potron-minet, la lumière sur la pierre d'une façade de cathédrale reste une expérience sensible comparable à l'image - les séries de MONET ça ne fait pas de mal non plus ! 🙂

<em>Posté sur Linkedin du 28 mars 2025</em>

[Retour en haut](#)


---

## 💡 Philosophie de l'Innovation

> "L'innovation naît à l'intersection des disciplines, là où la créativité rencontre la technologie."

## 📱 Restons connectés !

**Envie d'explorer de nouveaux horizons numériques ?**

— [Portfolio Complet](https://portfolio-af-v2.netlify.app/)  
— [Me Contacter sur LinkedIn](https://www.linkedin.com/in/alexiafontaine)

#Innovation #TechCreative #DataScience #DigitalTransformation #CreativeTech

© 2025 Alexia Fontaine - Tous droits réservés