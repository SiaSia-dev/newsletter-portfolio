# 📰 Newsletter Portfolio - 23/05/2025

## Récits visuels, horizons numériques : Un voyage entre créativité et innovation 🚀

---

### 📌 Blog scientifique : archnum

![Blog scientifique : archnum](img/IA_Fleur_au_fusil.png)

#### Blog scientifique : archnum

[Blog scientifique : archnum](#)

[Retour en haut](#)


---

### 📌 MCP = Méta-API ?

![MCP = Méta-API ?](img/MCP.png)

#### MCP = Méta-API ?

[MCP = Méta-API ?](#)


#### 1.Model Context Protocol (MCP)

Rappel de ce qu'est MCP : un protocole de communication unificateur qui standardise le <em>chaos des API</em> !! 😉

<code>ascii
┌─────────────────┐
│   Assistant IA  │
└─────────┬───────┘
          │ MCP Protocol (méta-API)
┌─────────▼───────┐
│   MCP Server    │
└─┬─────┬─────┬───┘
  │     │     │ APIs sous-jacentes
┌─▼─┐ ┌─▼─┐ ┌─▼─┐
│API│ │API│ │API│
│ 1 │ │ 2 │ │ 3 │
└───┘ └───┘ └───┘</code>

Alors oui, on peut dire que MCP est une méta-API dans le sens où ce protocole standardise les échanges de données entre API.


#### 2.MCP, une méta-API spécialisée pour l'IA

Voilà tout le changement d'échelle, puisque ce sont les modèles IA qui orchestrent dans cet ecosystème.

Requête classique

<code>ascii
Humain → Une demande → Une réponse</code>

Orchestration MCP

<code>ascii
 Humain → Intention complexe → IA → Multiple tools → Synthèse</code>

...Mais je vous vois déjà vous demander ce qu'est une intention complexe? Prenons un exemple concret sur cette notion qui nous semble centrale.

Une intention complexe se formulerait sous la forme d'une question de ce type : <em>"Comment on peut améliorer notre productivité ?"</em> (...oui je cherche 😜)

L'IA va alors décomposer <em>"le problème"</em> :

- Analyser les métriques actuelles
- Identifier les goulots d'étranglement
- Comparer avec les standards du secteur
- Proposer des solutions adaptées au contexte
Donc "l'intention complexe" est bien plus qu'une demande humaine naturelle, en réalité, elle cache <strong>un besoin d'orchestration multi-services</strong> pour donner une réponse complète et contextualisée que doit pouvoir apporter l'IA.

...pas mal.

[Retour en haut](#)


---

### 📌 L'information obligée d'être créative

![L'information obligée d'être créative](img/IA_Fleur_au_fusil.png)

#### L'information obligée d'être créative

[L'information obligée d'être créative](#)


#### 1. La créativité en information : une réponse à la crise du journalisme

L'expression sonne un peu étrange mais cette recherche de réinvention, face aussi à des problèmes d'enjeux démocratiques, nous conduit tous à être entre l'admiration et l'ironie mordante comme le titrait récemment le Wall Street Journal, de cette manière, en parlant de cet entrepreneur Jeremy Gulban : ["He Wanted to Fix Local News. It's Harder Than He Thought." (article du 30/03/25)](https://www.wsj.com/business/media/he-wanted-to-fix-local-news-its-harder-than-he-thought-e56b4f12)

["He Wanted to Fix Local News. It's Harder Than He Thought." (article du 30/03/25)](https://www.wsj.com/business/media/he-wanted-to-fix-local-news-its-harder-than-he-thought-e56b4f12)

<em>... sans blague ?</em>

Mais il faut admettre que Monsieur GULBAN est audacieux.

Au début, j'ai cru que c'était un revival hippy mais pas du tout, cet entretien avec le journaliste Mark CARO permet justement de présenter sa démarche et ses enjeux : <strong>rendre l'information accessible en promouvant une alternative citoyenne.</strong>

[Entretien du 12/05/2025 avec Mark CARO sur "Local News Initiative" : Paving the CherryRoad - Jeremy Gulban dreams of creating a national network of community papers–but first must make 2/3 of his own outlets profitable](https://localnewsinitiative.northwestern.edu/posts/2025/05/12/jeremy-gulban-cherryroad-q-and-a/index.html)

[Entretien du 12/05/2025 avec Mark CARO sur "Local News Initiative" : Paving the CherryRoad - Jeremy Gulban dreams of creating a national network of community papers–but first must make 2/3 of his own outlets profitable](https://localnewsinitiative.northwestern.edu/posts/2025/05/12/jeremy-gulban-cherryroad-q-and-a/index.html)

Et à la lecture de son projet, je reconnais qu'il mène admirablement son défi : <strong>créer un réseau national de journaux communataires aux Etats-Unis</strong>.

Cette entreprise est vraiment intéressante car elle l'a obligé à repenser le modèle classique du format presse papier selon les contraintes actuelles (essor du numérique, baisse de la lecture etc.), en tentant maintenant d'en proposer un modèle économique.

Il fallait oser, à l'heure où se plaindre des médias est tellement évident mais sans rien amener ; son idée a le mérite d'ouvrir sur des actions concrètes pour sortir de cette crise.


#### 2. De nouvelles formes de régulation de l'information

Cette segmentation du Web devient finalement de plus en plus visible, avec des formes de régulation du trafic selon des échelles territoriales marquées.

On voit bien des réseaux sociaux décentralisés prendre place dans le paysage numérique. Je pense au réseau social [Mastodon](https://joinmastodon.org/fr) car le plus connu.

[Mastodon](https://joinmastodon.org/fr)

Beaucoup préfèrent parler de <strong>fragmentation du web</strong> pour aborder finalement les politiques qui luttent entre national et global.

Toutes ces luttes sont légitimes et démontrent une certaine volonté à exister.

[Retour en haut](#)


---

### 📌 LLM function calls don't scale; code orchestration is simpler, more effective de Jiquan Ngiam

![LLM function calls don't scale; code orchestration is simpler, more effective de Jiquan Ngiam](img/IA_Fleur_au_fusil.png)

#### LLM function calls don't scale; code orchestration is simpler, more effective de Jiquan Ngiam

[LLM function calls don't scale; code orchestration is simpler, more effective de Jiquan Ngiam](#)

Un article très intéressant sur l'orchestration avec MCP et des propositions pour accélérer les performances : <strong>séparer l'orchestration des appels de fonctions.</strong>

On pourrai résumer cela par :

Problème actuel :

<code>ascii
Tool Call → Large JSON → LLM → Processing → Output</code>

Sa solution : séparer les responsabilités

<code>ascii
LLM → Code Orchestration → Data Processing → Results</code>

Donc là encore on sépare le fond de la forme : la structure se distingue de la logique.

Son expérience métier rend cet article pertinent et direct ce qui le rend accessible aux néophytes que nous sommes.

[LLM function calls don't scale; code orchestration is simpler, more effective de Jiquan NGIAM" publié le 20 mai 2025](https://jngiam.bearblog.dev/mcp-large-data/) présent aussi sur LinkedIn.

[LLM function calls don't scale; code orchestration is simpler, more effective de Jiquan NGIAM" publié le 20 mai 2025](https://jngiam.bearblog.dev/mcp-large-data/)

[Retour en haut](#)


---

### 📌 archaedyn

![archaedyn](img/1ere-couv_1.jpg)

#### archaedyn

[archaedyn](#)


#### Blog Scientifique : ARCHAEDYN


#### Image Représentative

<img alt="Couverture ARCHAEDYN" src="/img/1ere-couv_1.jpg"/>


#### Contexte du Projet

Un projet de recherche archéologique innovant explorant les dynamiques territoriales sur 7 millénaires.


#### Objectifs de Recherche

- Analyser l'occupation humaine
- Étudier les transformations territoriales
- Comprendre l'évolution historique des espaces

#### Méthodologie de Recherche


#### Approche Interdisciplinaire

- Archéologie
- Cartographie historique
- Analyse spatiale
- Systèmes d'Information Géographique (SIG)

#### Techniques d'Analyse

1. Analyse cartographique détaillée
1. Reconstruction des territoires historiques
1. Étude des mutations spatiales
1. Cartographie comparative
1. Études archéologiques comparatives
1. Analyse des vestiges
1. Comparaison inter-sites
1. Reconstruction des dynamiques d'occupation
1. Modélisation des Données Spatiales
1. Utilisation d'outils SIG avancés
1. Création de modèles spatiaux
1. Analyse des transformations territoriales
Cartographie comparative

<strong>Études archéologiques comparatives</strong>

Reconstruction des dynamiques d'occupation

<strong>Modélisation des Données Spatiales</strong>


#### Compétences Mises en Œuvre

- Recherche archéologique
- Analyse géospatiale
- Traitement de données historiques
- Modélisation cartographique
- Systèmes d'Information Géographique

#### Périodes Étudiées

- Néolithique
- Périodes intermédiaires
- Moyen Âge

#### Impact Scientifique

- Compréhension approfondie des dynamiques territoriales
- Nouvelle perspective sur l'occupation humaine
- Méthodologie innovante d'analyse historique

#### Lien vers la Publication

[Article complet sur ArchNum](https://archnum.hypotheses.org/175)

[Article complet sur ArchNum](https://archnum.hypotheses.org/175)


#### Philosophie de Recherche

"Chaque trace, chaque vestige est un fragment d'un récit territorial plus large."


#### Conclusion

Un projet qui transcende la simple étude archéologique pour proposer une vision dynamique et vivante de l'histoire territoriale.

[Retour en haut](#)


---

### 📈 Méréologie comme cadre d'analyse

![Méréologie comme cadre d'analyse](img/IA_Fleur_au_fusil.png)

#### Méréologie comme cadre d'analyse

[Méréologie comme cadre d'analyse](#)

Demande de prompt : définition et applications de la méréologie


#### Origines et définition

La méréologie, théorie formelle des relations entre les parties et le tout, trouve ses racines dans les travaux du philosophe et logicien polonais Stanisław Leśniewski, qui développa cette approche dans les années 1910-1920. Cependant, l'étude des relations partie-tout était déjà présente dans la pensée d'Aristote et a été explorée plus tard par des philosophes comme Edmund Husserl dans ses "Recherches logiques" (1900-1901) et Alfred North Whitehead.

D'autres contributions significatives incluent les travaux de Peter Simons ("Parts: A Study in Ontology", 1987) et Nelson Goodman ("The Structure of Appearance", 1951), qui ont étendu et formalisé davantage cette théorie logique.


#### Applications dans l'analyse culturelle

Dans le domaine de l'analyse culturelle, l'approche méréologique offre un cadre conceptuel permettant d'examiner comment les éléments culturels fonctionnent simultanément comme entités autonomes et comme composantes de systèmes plus larges. Cette perspective s'avère particulièrement utile pour comprendre:

- Les relations entre pratiques culturelles individuelles et systèmes globaux
- L'intégration des sous-cultures dans des cultures plus étendues
- La manière dont les artefacts culturels acquièrent des significations différentes selon les contextes
Ce cadre théorique permet d'analyser efficacement les processus d'hybridation culturelle en montrant comment des éléments issus de différents ensembles peuvent être recombinés pour former de nouvelles totalités culturelles.


#### La méréologie en linguistique cognitive

La linguistique cognitive utilise la méréologie pour étudier comment nous conceptualisons et exprimons les relations partie-tout dans le langage. On peut distinguer plusieurs types de relations méréologiques dans les expressions linguistiques:

1. Relations partie-objet physique: "le toit de la maison", "la poignée de la porte"
1. Relations membre-collection: "un joueur de l'équipe", "une carte du jeu"
1. Relations portion-masse: "une tranche de pain", "une goutte d'eau"
Ces expressions reflètent notre conceptualisation cognitive des ensembles et peuvent varier considérablement d'une langue à l'autre, certaines utilisant des classificateurs spécifiques ou des constructions grammaticales distinctes.


#### Applications en ontologie informatique

Dans le domaine de l'informatique, la méréologie est fondamentale pour la construction d'ontologies comme SNOMED CT (Systematized Nomenclature of Medicine -- Clinical Terms), l'une des plus importantes ontologies médicales. Les relations méréologiques y sont utilisées pour:

- Structurer hiérarchiquement les concepts médicaux
- Faciliter le raisonnement automatique
- Permettre des requêtes complexes dans les dossiers médicaux électroniques
Par exemple, l'ontologie établit des relations comme "le ventricule gauche est une partie du cœur" ou "la fièvre est une partie du syndrome grippal", fournissant ainsi une base pour l'inférence automatisée.


#### Analyse méréologique des archives visuelles

L'application de la méréologie à l'analyse des archives visuelles constitue un domaine particulièrement innovant. Cette approche permet d'étudier:

1. La relation entre l'image individuelle et la collection: Une image isolée possède sa propre signification, mais acquiert des dimensions supplémentaires lorsqu'elle est mise en relation avec d'autres images.
1. Les sous-ensembles significatifs: Comment certains groupements d'images constituent des "parties" cohérentes qui transmettent un message spécifique au sein de l'ensemble plus large.
1. Les éléments visuels récurrents: La façon dont certains motifs deviennent des unités méréologiques structurant la collection.
<strong>La relation entre l'image individuelle et la collection</strong>: Une image isolée possède sa propre signification, mais acquiert des dimensions supplémentaires lorsqu'elle est mise en relation avec d'autres images.

<strong>Les sous-ensembles significatifs</strong>: Comment certains groupements d'images constituent des "parties" cohérentes qui transmettent un message spécifique au sein de l'ensemble plus large.

<strong>Les éléments visuels récurrents</strong>: La façon dont certains motifs deviennent des unités méréologiques structurant la collection.


#### Le raisonnement métavisuel

Le raisonnement métavisuel, qui consiste à analyser les relations entre les images au-delà de leur contenu individuel, s'appuie sur plusieurs opérations:

- Catégorisation: Identifier les principes d'organisation des images
- Contextualisation: Replacer chaque image dans son rapport aux autres
- Abstraction: Dégager des motifs invisibles au niveau de l'image individuelle

#### Opérations rhétoriques dans l'analyse scientifique des archives visuelles

Pour produire des informations scientifiques à partir d'une collection d'images, plusieurs opérations rhétoriques sont employées:

1. Juxtaposition: Révéler des similarités ou différences par la mise en parallèle
1. Série et séquence: Organiser les images pour dégager des tendances ou ruptures
1. Synecdoque visuelle: Utiliser certaines images comme représentatives d'ensembles plus larges
1. Métaphore structurelle: Employer des structures conceptuelles pour représenter les relations entre images
1. Échantillonnage représentatif: Sélectionner des sous-ensembles reflétant les propriétés de la collection entière
Ces opérations transforment une accumulation d'images en un corpus structuré produisant des connaissances scientifiques sur les phénomènes visuels, les pratiques culturelles ou les évolutions historiques qu'elles documentent.


#### Conclusion

La méréologie, née dans le domaine de la logique formelle, s'est révélée être un cadre conceptuel exceptionnellement fertile pour diverses disciplines. Son application à l'analyse culturelle, à la linguistique cognitive, à l'ontologie informatique et particulièrement à l'étude des archives visuelles démontre sa puissance pour comprendre les relations complexes entre les parties et les ensembles dans de multiples domaines de la connaissance.

En offrant une méthodologie pour analyser comment les significations émergent non seulement des éléments individuels mais aussi de leurs interactions, la méréologie constitue un outil précieux pour la recherche contemporaine dans les sciences humaines et sociales, ainsi que dans le domaine des technologies de l'information.

<em>contenu généré par une IA générative</em>

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