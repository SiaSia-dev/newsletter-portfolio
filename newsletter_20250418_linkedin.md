# 📰 Newsletter Portfolio - 18/04/2025

## Récits visuels, horizons numériques : Un voyage entre créativité et innovation 🚀

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

### 📊 Quiz Interactif NumPy : Apprentissage interactif en Data Science

![Quiz Interactif NumPy : Apprentissage interactif en Data Science](img/NumPy_logo_2020.svg.png)

#### Quiz Interactif NumPy : Apprentissage interactif en Data Science


#### Présentation du Projet "Quiz Numpy"

<img height="100" src="/img/NumPy_logo_2020.svg.png" width="100"/>
Un quiz interactif conçu pour tester et approfondir les connaissances en manipulation de données avec NumPy, illustrant une approche innovante d'apprentissage technologique.

La librairie NumPy est un incontournable des sciences de données, impossible de ne pas connaître : <strong>projet open-source</strong>, <u>cela implique que vous être libres d'utiliser cet outil comme bon vous semble</u> (<em>petit rappel sur les fondements de l'informatique, partage &amp; liberté</em>)

Notre propos se veut donc très modeste : développer une application qui génère les questions et réponses basées sur la documentation de Numpy.


#### Objectifs

- Tester les compétences en manipulation de données
- Fournir un apprentissage ludique et interactif
- Renforcer la compréhension des concepts NumPy

#### Technologies Utilisées

- Python
- NumPy
- Modèle d'apprentissage
- E-learning
- Interfaces interactives

#### Lien du Projet

[Tester Vos Compétences avec le Quiz NumPy](https://quiz-numpy.streamlit.app/)

[Tester Vos Compétences avec le Quiz NumPy](https://quiz-numpy.streamlit.app/)


#### Concept Pédagogique

Combinaison de l'apprentissage ludique avec des concepts techniques avancés de manipulation de données.


#### Fonctionnalités Principales

- Questions interactives sur NumPy
- Feedback immédiat
- Progression adaptative
- Couverture complète des concepts clés

#### Approche Pédagogique

- Apprentissage par l'interaction
- Mise en pratique immédiate des concepts
- Adaptation du niveau de difficulté
- Engagement actif de l'apprenant

#### Compétences Mises en Œuvre

- Développement d'outils éducatifs interactifs
- Conception d'interfaces pédagogiques
- Maîtrise technique de NumPy
- Conception de systèmes d'apprentissage adaptatifs

#### Référence

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

### 📌 Architecture Modulaire à Base de Contenu

![Architecture Modulaire à Base de Contenu](img/Slowsia.jpg)

#### Architecture Modulaire à Base de Contenu

L'<strong>Architecture Modulaire à Base de Contenu</strong> (ou "Content-Driven Modular Architecture") représente une approche moderne et flexible pour concevoir des sites web et des applications. Cette méthodologie place le contenu au centre du processus de développement, en le séparant strictement de la présentation.

<strong>Mots-clés:</strong> développement, architecture, contentdriven, méthodologie, applications


#### Principes fondamentaux

Cette architecture repose sur plusieurs principes clés qui la rendent particulièrement efficace pour les sites riches en contenu comme les portfolios et les blogs :

<strong>Mots-clés:</strong> architecture, portfolios, principes, plusieurs

Le contenu est stocké dans des fichiers indépendants (souvent au format Markdown) avec des métadonnées standardisées (frontmatter), complètement séparés du code HTML, CSS et JavaScript qui définit leur présentation. Cette séparation permet à chaque aspect d'évoluer indépendamment.

<strong>Mots-clés:</strong> standardisées, indépendance, présentation

Les sections et composants peuvent être facilement réutilisés, réorganisés ou recombinés pour créer de nouvelles pages ou expériences. Cette flexibilité permet d'assembler rapidement différentes vues à partir des mêmes éléments de base.

<strong>Mots-clés:</strong> expériences, réorganisation, flexibilité

Modifier un contenu n'exige pas de toucher au code HTML principal. Les rédacteurs de contenu peuvent se concentrer uniquement sur les fichiers Markdown pertinents, sans risquer d'altérer la structure ou le fonctionnement du site.

<strong>Mots-clés:</strong> fonctionnement, pertinents, concentrer, uniquement, rédacteurs

Ajouter une nouvelle section est aussi simple que de créer un nouveau fichier Markdown. Cette approche réduit considérablement la friction pour enrichir le site avec de nouveaux contenus.

<strong>Mots-clés:</strong>  contenus


#### Implémentation pratique

Pour les composants simples, le Markdown pur suffit généralement. Cependant, pour les composants plus complexes comme les grilles de compétences, les cartes de services, ou les processus multi-étapes, l'HTML embarqué dans Markdown offre le meilleur compromis :

Cette approche hybride permet de préserver le rendu visuel des composants complexes tout en profitant pleinement de la modularité du système.

<strong>Mots-clés:</strong> multiétapes, compétences, composants, markdown, modularité, composants, complexes


#### Avantages à long terme

Au-delà des bénéfices immédiats, cette architecture offre des avantages substantiels sur le long terme :

- Transitions technologiques facilitées - Le contenu peut être conservé même si le framework ou la technologie de présentation change
- Versionning efficace - Les modifications de contenu sont clairement visibles dans les commits Git
- Possibilités de migration accrues - Le contenu peut être facilement exporté vers d'autres systèmes
- Optimisation du workflow - Les designers et développeurs peuvent travailler sur l'interface pendant que les rédacteurs créent le contenu
Cette architecture représente une évolution naturelle des systèmes de gestion de contenu traditionnels, offrant davantage de flexibilité tout en conservant une structure claire et organisée.

<strong>Mots-clés:</strong> architecture, flexibilité


#### 1. Séparation du contenu et de la présentation

Le contenu est stocké dans des fichiers indépendants (souvent au format Markdown) avec des métadonnées standardisées (frontmatter), complètement séparés du code HTML, CSS et JavaScript qui définit leur présentation. Cette séparation permet à chaque aspect d'évoluer indépendamment.

<strong>Mots-clés:</strong> indépendance, standardisés, présentation


#### 2. Composabilité

Les sections et composants peuvent être facilement réutilisés, réorganisés ou recombinés pour créer de nouvelles pages ou expériences. Cette flexibilité permet d'assembler rapidement différentes vues à partir des mêmes éléments de base.

<strong>Mots-clés:</strong> flexibilité


#### 3. Maintenabilité

Modifier un contenu n'exige pas de toucher au code HTML principal. Les rédacteurs de contenu peuvent se concentrer uniquement sur les fichiers Markdown pertinents, sans risquer d'altérer la structure ou le fonctionnement du site.

<strong>Mots-clés:</strong> pertinents, rédacteurs


#### 4. Évolutivité

Ajouter une nouvelle section est aussi simple que de créer un nouveau fichier Markdown. Cette approche réduit considérablement la friction pour enrichir le site avec de nouveaux contenus.

<strong>Mots-clés:</strong> enrichir, contenus

[Retour en haut](#)


---

### 📌 OPENEDITION : carnet HYPOTHESES - Blog scientifique Archnum

![OPENEDITION : carnet HYPOTHESES - Blog scientifique Archnum](img/hypotheses.jpg)

#### OPENEDITION : carnet HYPOTHESES - Blog scientifique Archnum


#### OpenEdition, le portail de la communication scientifique en SHS

<em><strong>OpenEdition</strong> est un portail de ressources électroniques en sciences humaines et sociales.</em>
[Pour en savoir plus](https://www.openedition.org/)

[Pour en savoir plus](https://www.openedition.org/)

Il s'agit d'une <em>vaste librairie en ligne</em>, regroupant <strong>en accès libre des ressources numériques de communication scientifique.</strong>
<em>A une époque où la défiance systématique (et souvent justifiée) envers les médias pose de vrais problèmes d'accès à l'information et de démocratie, </em><em>ce dispositif est <u>une bouffée d'oxygène</u></em><em>.</em>

<strong>Hypothèses</strong> constitue l'une de ses plateformes avec pour finalité la publication en ligne : il s'agit de mettre à disposition au plus grand nombre les recherches, les avancées, les questionnements scientifiques actuels, et gratuitement!


#### Présentation de la plateforme de publication Hypothèses

Par sa vocation de publication en ligne, [Hypothèses](https://hypotheses.org) utilise le [BLOG](https://fr.wikipedia.org/wiki/Blog) pour rendre compte d'<strong>un très grand nombre d'actualités scientifiques</strong> :

[Hypothèses](https://hypotheses.org)

[BLOG](https://fr.wikipedia.org/wiki/Blog)

Elle est ouverte prioritairement à la recherche académique mais la recherche indépendante y a aussi sa place, ce qui en fait <strong>un espace de reflexions riches et diversifiés</strong>.

Nous espérons participer à <strong>ce mouvement de partage des savoirs et des connaissances</strong> par notre petit blog <strong>ARCHNUM</strong> dont le but au départ était de rendre compte des pratiques numériques en archéologie ; et qui a évolué aujourd'hui vers la thématique Data et ses applications.

[VISITER LE BLOG ARCHNUM](https://archnum.hypotheses.org/)

[VISITER LE BLOG ARCHNUM](https://archnum.hypotheses.org/)

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

## 💡 Philosophie de l'Innovation

> "L'innovation naît à l'intersection des disciplines, là où la créativité rencontre la technologie."

## 📱 Restons connectés !

**Envie d'explorer de nouveaux horizons numériques ?**

— [Portfolio Complet](https://portfolio-af-v2.netlify.app/)  
— [Me Contacter sur LinkedIn](https://www.linkedin.com/in/alexiafontaine)

#Innovation #TechCreative #DataScience #DigitalTransformation #CreativeTech

© 2025 Alexia Fontaine - Tous droits réservés