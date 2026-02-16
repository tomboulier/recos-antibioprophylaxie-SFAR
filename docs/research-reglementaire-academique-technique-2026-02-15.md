# Rapport de recherche : Réglementaire, État de l'art académique, MCP vs RAG

**Date :** 2026-02-15
**Type de recherche :** Mixte (réglementaire + académique + technique)
**Auteur :** Thomas Boulier
**Projet :** Antibioprophylaxie SFAR

---

## Résumé exécutif

Cette recherche couvre trois axes essentiels pour le projet :

1. **Réglementaire** : un logiciel qui affiche des recommandations existantes (sans les transformer) n'est probablement **pas un dispositif médical** au sens du règlement EU 2017/745, mais le module IA/chatbot pourrait changer la donne — à clarifier avec un expert.
2. **État de l'art** : les LLMs montrent des taux d'hallucination de **15-40% en natif** sur des tâches cliniques, réduits à **0-8% avec RAG**, et une étude spécifique sur l'antibioprophylaxie rachidienne montre **62-81% de réponses correctes** selon le modèle. Le domaine est en plein essor avec de nombreuses publications en 2024-2025.
3. **MCP vs RAG** : les deux approches sont **complémentaires, pas concurrentes**. RAG excelle sur les données non structurées (texte, documents), MCP sur les données structurées (API, BDD). Notre projet bénéficierait d'une approche hybride.

**Conclusion principale** : le projet est bien positionné dans un champ de recherche actif et pertinent. La comparaison MCP vs RAG sur des recommandations médicales structurées serait une contribution originale.

---

## Questions de recherche

1. Une app qui affiche des recommandations d'ATB est-elle un dispositif médical (DM) / SADC au sens du règlement EU 2017/745 ?
2. Quelles obligations si c'est classé DM ? Et si ce n'est pas le cas ?
3. Quelles publications existent sur l'utilisation de LLMs avec des recommandations médicales ?
4. Quels taux d'hallucination ont été mesurés ?
5. Quelles méthodologies d'évaluation sont utilisées ?
6. Quelles différences fondamentales entre MCP et RAG pour des données médicales structurées ?
7. Quels avantages/inconvénients de chaque approche pour notre cas d'usage ?

---

## Méthodologie

**Approche :** Recherche web structurée (WebSearch + WebFetch) sur sources institutionnelles (ANSM, Commission Européenne), publications scientifiques (PubMed/PMC, Nature, arXiv) et documentation technique.

**Sources consultées :** ~25 sources (articles scientifiques, guides réglementaires, articles techniques)

---

## Axe 1 : Réglementaire — Dispositif médical et SADC

### Q1 : Notre application est-elle un dispositif médical ?

**Réponse : C'est nuancé — probablement non pour la V1, à investiguer pour le module IA.**

**Confiance :** Moyenne (nécessite confirmation par un expert réglementaire)

#### Le cadre réglementaire

Le **Règlement EU 2017/745** (MDR) et le guide **MDCG 2019-11** (révisé en juin 2025 — Rev.1) définissent les critères de qualification d'un logiciel comme dispositif médical.

Le processus de qualification suit plusieurs étapes :
1. **Le logiciel est-il un produit qui traite des données ?** → Oui
2. **Le logiciel est-il utilisé au bénéfice de patients individuels ?** → C'est la question clé
3. **Le logiciel fait-il plus que du stockage, de l'archivage, de la communication ou de la recherche simple (simple search) ?** → C'est la question discriminante

#### Application à notre projet

**Module recherche/affichage (webapp V1)** : un logiciel qui se contente d'afficher des recommandations existantes sans les transformer, qui fait de la "recherche simple" dans une base de données de recommandations publiques, **ne serait probablement pas qualifié de DM**. Il s'apparente à un moteur de recherche dans des guidelines existantes.

**Module IA/chatbot** : ici c'est différent. Un chatbot qui *interprète* une question clinique et *génère* une réponse basée sur les recommandations fait plus que de la "simple recherche". Il pourrait être considéré comme un logiciel qui fournit des informations utilisées pour prendre des décisions thérapeutiques, ce qui le classerait potentiellement en **Classe IIa** (règle 11 du MDR).

**Point important (Rev.1 2025)** : le terme **MDAI (Medical Device Artificial Intelligence)** apparaît pour la première fois dans la révision, reflétant un focus réglementaire croissant sur les logiciels IA.

### Q2 : Obligations si classé DM

Si le module IA est classé DM (Classe IIa) :
- Marquage CE obligatoire
- Évaluation de conformité par un organisme notifié
- Système de management de la qualité (ISO 13485)
- Documentation technique complète
- Surveillance post-commercialisation

**Si non classé DM** (module recherche seule) :
- Pas d'obligations réglementaires spécifiques
- Recommandé : ajouter un disclaimer clair ("outil d'aide, ne remplace pas le jugement clinique")

### Recommandation pour le projet

- **V1 (recherche + affichage)** : se positionner comme un outil de consultation de données publiques, pas comme un DM. Ajouter un disclaimer.
- **Module IA** : se positionner comme un **outil de recherche académique**, pas comme un outil en production clinique. Le cadre de la publication scientifique protège cette position.
- **À terme** : si le projet évolue vers une mise en production hospitalière, consulter un expert réglementaire.

**Sources :**
- [ANSM — Logiciels et applications mobiles en santé](https://ansm.sante.fr/documents/reference/reglementation-relative-aux-dispositifs-medicaux-dm-et-aux-dispositifs-medicaux-de-diagnostic-in-vitro-dmdiv/logiciels-et-applications-mobiles-en-sante)
- [MDCG 2019-11 Rev.1 (juin 2025)](https://health.ec.europa.eu/latest-updates/update-mdcg-2019-11-rev1-qualification-and-classification-software-regulation-eu-2017745-and-2025-06-17_en)
- [Qualitiso — Guide MDCG 2019-11](https://www.qualitiso.com/guide-mdcg-qualification-classification-logiciels-reglement-ue-2017-745/)
- [DeviceMed — Enjeux réglementaires SADC](https://www.devicemed.fr/dossiers/reglementation/quel-enjeu-reglementaire-pour-les-logiciels-daide-a-la-decision-clinique/21068)
- [Emergo by UL — MDCG 2019-11 Rev.1](https://www.emergobyul.com/news/european-revision-primary-software-guidance-mdcg-2019-11-revision-1-small-changes-meaningful)

---

## Axe 2 : État de l'art académique — LLMs et recommandations médicales

### Q3 : Publications sur LLMs + recommandations médicales

Le domaine est **très actif en 2024-2025** avec de nombreuses publications. Voici les études les plus pertinentes :

#### Étude directement pertinente : LLM et antibioprophylaxie

**"Performance of a Large Language Model in the Generation of Clinical Guidelines for Antibiotic Prophylaxis in Spine Surgery"** (PMC, 2024)

- **Méthodologie** : 16 questions extraites des directives NASS (2013) posées à GPT-3.5 et GPT-4.0
- **Résultats** :
  - GPT-3.5 : **62,5% de réponses correctes**, 25% de réponses excessivement confiantes, fabrication de citations
  - GPT-4.0 : **81% de réponses correctes**, avec citations directes dans 62,5% des cas
- **Conclusion** : les auteurs recommandent la prudence pour l'usage clinique

#### LLM comme système d'aide à la décision pour la sécurité médicamenteuse

**"Large language model as clinical decision support system augments medication safety in 16 clinical specialties"** (PMC, 2025)

- **Méthodologie** : étude prospective, 91 scénarios d'erreurs, 40 vignettes cliniques, 16 spécialités, 6 pharmaciens évaluateurs
- **LLMs testés** : Gemini Flash, Gemini 1.5 Pro, GPT-4 Turbo, GPT-4 Omni, Claude 3.5 Sonnet
- **Résultats clés** :
  - Claude 3.5 Sonnet natif : **51% d'exactitude** (meilleur en natif)
  - Claude + RAG : **49%** (le RAG n'a pas amélioré les résultats !)
  - Mode co-pilot (pharmacien + LLM) : **61%** vs 46% pharmacien seul
  - Détection des erreurs graves : x1,5 en mode co-pilot
- **Conclusion importante** : le RAG n'améliore pas toujours les performances — "les LLMs peuvent montrer de la réticence à accepter pleinement les nouvelles connaissances"

#### Framework d'évaluation des hallucinations

**"A framework to assess clinical safety and hallucination rates of LLMs for medical text summarisation"** (Nature npj Digital Medicine, 2025)

- **Méthodologie** : 18 expériences, 450 paires consultation-note, 12 999 phrases annotées manuellement par des cliniciens
- **Framework CREOLA** à 4 composantes :
  1. Taxonomie d'erreurs cliniquement informée (fabrications, négations, causalité, contextuelles)
  2. Structure expérimentale itérative
  3. Cadre de sécurité clinique (inspiré des certifications DM)
  4. Interface graphique CREOLA pour annotation clinicienne
- **Taux mesurés** :
  - Hallucinations : **1,47%** (191/12 999 phrases), dont **44% d'erreurs majeures**
  - Omissions : **3,45%** (1 712/49 590 phrases), dont **16,7% majeures**
- **Conclusion** : l'affinage itératif des prompts peut réduire les erreurs sous les taux d'erreurs humaines documentés

### Q4 : Taux d'hallucination mesurés

| Contexte | LLM natif | Avec RAG | Source |
|----------|-----------|----------|--------|
| Tâches cliniques générales | 15-40% | — | [arXiv 2503.05777](https://arxiv.org/html/2503.05777v2) |
| Résumés de consultations | 1,47% | — | [Nature npj Digital Medicine](https://pmc.ncbi.nlm.nih.gov/articles/PMC12075489/) |
| ATB prophylaxie rachis (GPT-3.5) | 37,5% erreurs | — | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10992653/) |
| ATB prophylaxie rachis (GPT-4) | 19% erreurs | — | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10992653/) |
| Sécurité médicamenteuse (Claude) | 49% erreurs | 51% erreurs (!) | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12629785/) |
| Modèles médicaux spécialisés | 28,6-39,6% | 0-8% | [MDPI Electronics](https://www.mdpi.com/2079-9292/14/21/4227) |
| Santé publique (MEGA-RAG) | 8% | 0% | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12540348/) |

**Observation clé** : les taux varient énormément selon la tâche, le modèle, et la méthode d'évaluation. Le RAG réduit généralement les hallucinations mais pas toujours (cf. étude Claude + RAG sur la sécurité médicamenteuse).

### Q5 : Méthodologies d'évaluation

Les principales approches identifiées :

1. **Annotation clinicienne manuelle** (gold standard) : des cliniciens annotent chaque sortie du LLM comme correcte/incorrecte/hallucinée. Coûteux mais fiable.
2. **Comparaison aux guidelines existantes** : les réponses du LLM sont comparées aux recommandations officielles (comme les directives NASS). Adapté à notre cas d'usage.
3. **Framework CREOLA** : taxonomie d'erreurs + annotation via interface dédiée + évaluation de la sécurité clinique.
4. **Benchmark MIRAGE** : 7 663 questions issues de 5 datasets cliniques, avec évaluation zero-shot, format QCM.
5. **Mode co-pilot** : le clinicien utilise le LLM comme aide et on mesure l'amélioration de performance (vs clinicien seul et LLM seul).

**Pour notre projet** : l'approche "comparaison aux guidelines" est la plus pertinente. On pourrait créer un jeu de questions-réponses à partir des RFE et mesurer le taux de réponses correctes / hallucinations / "je ne sais pas".

**Sources :**
- [LLM et antibioprophylaxie rachidienne](https://pmc.ncbi.nlm.nih.gov/articles/PMC10992653/)
- [LLM comme CDSS pour la sécurité médicamenteuse](https://pmc.ncbi.nlm.nih.gov/articles/PMC12629785/)
- [Framework CREOLA — hallucinations LLM](https://pmc.ncbi.nlm.nih.gov/articles/PMC12075489/)
- [Medical Hallucination in Foundation Models](https://arxiv.org/html/2503.05777v2)
- [Clinicians' Guide to LLM Hallucinations](https://www.i-jmr.org/2025/1/e59823)
- [RAG for LLMs in Healthcare — revue systématique](https://pmc.ncbi.nlm.nih.gov/articles/PMC12157099/)
- [MEGA-RAG — mitigation hallucinations santé publique](https://pmc.ncbi.nlm.nih.gov/articles/PMC12540348/)
- [AI for bacterial infection management](https://academic.oup.com/jac/advance-article/doi/10.1093/jac/dkaf470/8388020)
- [LLM medication safety — NHS Primary Care](https://arxiv.org/html/2512.21127v1)
- [LLMs in Healthcare — Review](https://pmc.ncbi.nlm.nih.gov/articles/PMC12189880/)

---

## Axe 3 : Technique — MCP vs RAG

### Q6 : Différences fondamentales

| Aspect | RAG | MCP |
|--------|-----|-----|
| **Type de données** | Non structurées (PDF, texte, docs) | Structurées (API, BDD, JSON) |
| **Méthode d'accès** | Recherche par similarité vectorielle (embeddings) | Invocation d'outils/API à la demande |
| **Pré-traitement** | Chunking + embedding + indexation en BDD vectorielle | Définition de schémas d'outils/ressources |
| **Temps réel** | Non (données pré-indexées) | Oui (requêtes live) |
| **Précision** | Approximative (similarité sémantique) | Exacte (requêtes structurées) |
| **Hallucinations** | Réduites (contexte fourni) mais pas éliminées | Réduites (données exactes) mais le LLM peut mal interpréter |
| **Mise à jour** | Re-embedding nécessaire | Modification de la source directement |
| **Sécurité/contrôle** | Données stockées en BDD vectorielle | Contrôle d'accès fin (OAuth2, permissions) |
| **Complexité** | Pipeline d'embedding + BDD vectorielle | Serveur MCP + définition d'outils |

### Q7 : Application à notre cas d'usage

#### Pourquoi MCP est pertinent pour nous

Nos données (RFE antibioprophylaxie) sont **structurées par nature** : c'est un tableau avec des colonnes (spécialité, intervention, antibiotique, posologie, timing, réinjection, alternative allergie). MCP est idéal pour ça :
- Requêtes exactes ("quel ATB pour la PTH ?") → réponse précise, pas approximative
- Pas de risque de "mauvais chunk" récupéré
- Mise à jour facile si les RFE changent
- L'API REST et le serveur MCP servent aussi de produit standalone

#### Pourquoi RAG est aussi pertinent

Les RFE contiennent aussi du **texte narratif** (recommandations générales, argumentaires, cas particuliers) qui ne se réduit pas à un tableau. RAG permettrait de :
- Répondre à des questions complexes ("quand faut-il prolonger l'antibioprophylaxie ?")
- Intégrer le texte des recommandations générales (timing, patients obèses, insuffisance rénale, etc.)
- Comparer les réponses RAG vs MCP (volet recherche/publication)

#### Approche recommandée pour l'étude : Comparaison RAG brut vs MCP structuré

La question de recherche centrale est celle du **coût-bénéfice de la structuration** :

- **RAG brut** : on donne le PDF tel quel au LLM (via chunking + embedding), sans pré-formattage. Coût de mise en place faible, mais précision incertaine.
- **MCP structuré** : on structure manuellement les tableaux du PDF en base de données, puis on expose via MCP. Coût de structuration élevé, mais précision attendue supérieure.

**Protocole d'étude proposé :**
1. **Phase 1** : Comparer RAG brut (PDF → LLM) vs MCP (données structurées → LLM) sur un même jeu de questions standardisé
2. **Phase 2** : Si les résultats le justifient, tester une approche hybride (MCP pour les tableaux + RAG pour le texte narratif)

**Question fondamentale** : la structuration manuelle des données (coûteuse en temps) améliore-t-elle suffisamment la fiabilité des réponses pour en justifier l'effort ? C'est une question très concrète et pertinente pour toutes les sociétés savantes envisageant la numérisation de leurs recommandations.

**Contribution originale** : aucune publication identifiée ne compare spécifiquement ces deux approches (RAG sur PDF brut vs MCP sur données structurées) dans le contexte de recommandations médicales. C'est un angle de publication fort.

**Sources :**
- [TrueFoundry — MCP vs RAG](https://www.truefoundry.com/blog/mcp-vs-rag)
- [Merge — MCP vs RAG overlap and differ](https://www.merge.dev/blog/rag-vs-mcp)
- [GitButler — MCP vs RAG context](https://blog.gitbutler.com/mcp-vs-rag)
- [Contentful — MCP vs RAG](https://www.contentful.com/blog/mcp-vs-rag/)
- [HyScaler — RAG vs MCP Full Guide 2025](https://hyscaler.com/insights/rag-vs-mcp-full-guide-2/)
- [DevContentOps — MCP vs RAG for AI Applications](https://devcontentops.io/post/2025/06/mcp-vs-rag-for-ai-applications)

---

## Insights clés

### Insight 1 : Le positionnement "recherche" protège réglementairement

**Constat :** Le cadre réglementaire des DM (EU 2017/745) est complexe, mais un projet de recherche académique avec disclaimer approprié n'a pas les mêmes contraintes qu'un produit commercial en production clinique.

**Implication :** On peut développer le module IA/chatbot sans blocage réglementaire, tant qu'on se positionne clairement comme outil de recherche.

**Recommandation :** Ajouter un disclaimer explicite. Investiguer plus en profondeur si le projet évolue vers la production.

**Priorité :** Haute

### Insight 2 : Le RAG n'améliore pas toujours les performances — résultat surprenant

**Constat :** L'étude sur la sécurité médicamenteuse montre que Claude + RAG (49%) fait *moins bien* que Claude natif (51%). Les auteurs suggèrent que les LLMs peuvent "résister" aux nouvelles connaissances injectées.

**Implication :** Le RAG n'est pas une solution magique. La qualité du chunking, de l'embedding et du prompt engineering est cruciale.

**Recommandation :** Tester rigoureusement les deux approches (MCP et RAG) plutôt que de supposer que l'une est meilleure.

**Priorité :** Haute (pour le design de l'étude)

### Insight 3 : GPT-4 fait significativement mieux que GPT-3.5 sur l'antibioprophylaxie

**Constat :** 81% vs 62,5% de réponses correctes sur les guidelines NASS. GPT-4 cite ses sources dans 62,5% des cas.

**Implication :** Le choix du modèle a un impact majeur. Les modèles récents (Claude 3.5+, GPT-4+) sont nettement meilleurs.

**Recommandation :** Tester plusieurs modèles dans l'étude comparative.

**Priorité :** Moyenne

### Insight 4 : Le framework CREOLA est une référence méthodologique

**Constat :** Le framework publié dans Nature npj Digital Medicine propose une approche structurée (taxonomie d'erreurs, annotation clinicienne, évaluation de sécurité) avec des métriques précises.

**Implication :** On peut s'inspirer de cette méthodologie pour notre propre évaluation.

**Recommandation :** Adapter le framework CREOLA à notre contexte (recommandations d'ATB plutôt que résumés de consultation).

**Priorité :** Haute (pour le design de l'étude)

### Insight 5 : La comparaison RAG brut vs MCP structuré serait une contribution originale et pragmatique

**Constat :** Aucune publication identifiée ne compare le RAG sur PDF brut (sans pré-formattage) vs le MCP sur données structurées (après extraction manuelle) sur des recommandations médicales. C'est pourtant LA question que se posent les sociétés savantes : faut-il investir dans la structuration de nos recommandations, ou peut-on simplement donner le PDF à un LLM ?

**Implication :** C'est un angle de publication original, pragmatique et généralisable.

**Recommandation :** Structurer l'étude en 2 phases : (1) RAG brut vs MCP structuré, (2) si pertinent, tester une approche hybride. Jeu de questions standardisé + évaluation par des cliniciens.

**Priorité :** Haute (c'est le cœur de la contribution scientifique)

### Insight 6 : Le mode "co-pilot" est plus efficace que l'autonomie

**Constat :** Pharmacien + LLM (61%) > LLM seul (51%) > pharmacien seul (46%). La détection des erreurs graves est x1,5 en co-pilot.

**Implication :** L'outil doit être conçu comme une aide, pas un remplacement. Le clinicien reste dans la boucle.

**Recommandation :** Designer l'UX du chatbot en mode "co-pilot" : proposer, sourcer, mais laisser le clinicien décider.

**Priorité :** Moyenne

---

## Recommandations

### Actions immédiates (prochaines 2 semaines)

1. **Ajouter un disclaimer** dans les specs du projet : "Outil de recherche et de consultation, ne se substitue pas au jugement clinique"
2. **Définir le jeu de questions de test** : extraire 30-50 questions-réponses à partir des RFE pour évaluer les LLMs
3. **Approche comparative définie** : RAG brut (PDF tel quel) vs MCP (données pré-structurées), puis hybride si pertinent

### Court terme (1-3 mois)

1. **Structurer les données** du PDF en base de données (prérequis pour MCP et RAG)
2. **Implémenter les 3 approches** sur un sous-ensemble de données
3. **S'inspirer du framework CREOLA** pour la taxonomie d'erreurs

### Long terme (3+ mois)

1. **Évaluation complète** avec annotation par des cliniciens (au moins 2 anesthésistes indépendants)
2. **Rédaction de l'article** : comparaison MCP vs RAG vs hybride sur les RFE antibioprophylaxie
3. **Investigation réglementaire approfondie** si mise en production envisagée

---

## Lacunes identifiées

**Ce qu'on ne sait pas encore :**
- Le statut réglementaire exact du module IA (nécessite un avis d'expert juridique/réglementaire)
- La performance comparative réelle de MCP vs RAG sur NOS données spécifiques (à mesurer)
- Les conditions d'utilisation exactes des RFE SFAR (propriété intellectuelle) — à vérifier avec la SFAR
- L'existence d'autres projets similaires en cours dans d'autres sociétés savantes

**Recherches complémentaires recommandées :**
- Interview d'un expert réglementaire (DM/SADC)
- Revue de littérature systématique complète (pour la publication)
- Contact avec d'autres groupes numériques de sociétés savantes

---

## Sources complètes

### Réglementaire
1. [ANSM — Logiciels et applications mobiles en santé](https://ansm.sante.fr/documents/reference/reglementation-relative-aux-dispositifs-medicaux-dm-et-aux-dispositifs-medicaux-de-diagnostic-in-vitro-dmdiv/logiciels-et-applications-mobiles-en-sante)
2. [MDCG 2019-11 — Document original (PDF)](https://health.ec.europa.eu/system/files/2020-09/md_mdcg_2019_11_guidance_en_0.pdf)
3. [MDCG 2019-11 Rev.1 (juin 2025)](https://health.ec.europa.eu/latest-updates/update-mdcg-2019-11-rev1-qualification-and-classification-software-regulation-eu-2017745-and-2025-06-17_en)
4. [Qualitiso — Guide MDCG 2019-11](https://www.qualitiso.com/guide-mdcg-qualification-classification-logiciels-reglement-ue-2017-745/)
5. [DeviceMed — Enjeux réglementaires SADC](https://www.devicemed.fr/dossiers/reglementation/quel-enjeu-reglementaire-pour-les-logiciels-daide-a-la-decision-clinique/21068)
6. [Qualitiso — Applis et logiciels sous règlement DM](https://www.qualitiso.com/applis-logiciel-reglement-dispositifs-medicaux/)
7. [NAMSA — Classification MDSW](https://namsa.com/fr/resources/blog/eu-mdr-and-ivdr-classifying-medical-device-software-mdsw/)
8. [Emergo by UL — MDCG 2019-11 Rev.1 Clarifications](https://www.emergobyul.com/news/european-revision-primary-software-guidance-mdcg-2019-11-revision-1-small-changes-meaningful)

### Académique — LLMs et recommandations médicales
9. [LLM et antibioprophylaxie rachidienne (PMC 2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10992653/)
10. [LLM comme CDSS — sécurité médicamenteuse 16 spécialités (PMC 2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12629785/)
11. [Framework CREOLA — hallucinations LLM (Nature npj Digital Medicine 2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12075489/)
12. [Medical Hallucination in Foundation Models (arXiv 2025)](https://arxiv.org/html/2503.05777v2)
13. [Clinicians' Guide to LLM Hallucinations (i-JMR 2025)](https://www.i-jmr.org/2025/1/e59823)
14. [AI for bacterial infection management (JAC 2025)](https://academic.oup.com/jac/advance-article/doi/10.1093/jac/dkaf470/8388020)
15. [LLMs in Healthcare — Review (PMC 2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12189880/)
16. [LLM medication safety — NHS Primary Care (arXiv 2025)](https://arxiv.org/html/2512.21127v1)
17. [Antibiotics and AI — Clinical Considerations (PMC 2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11933589/)
18. [LLMs for antibiotic prescribing — from parlour trick to practical tool (CMI 2025)](https://www.clinicalmicrobiologyandinfection.org/article/S1198-743X(25)00245-9/abstract)

### Académique — RAG en santé
19. [RAG for LLMs in Healthcare — revue systématique (PMC 2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12157099/)
20. [MEGA-RAG — mitigation hallucinations santé publique (PMC 2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12540348/)
21. [RAG variants for clinical decision support (MDPI 2024)](https://www.mdpi.com/2079-9292/14/21/4227)
22. [RAG in Healthcare — Comprehensive Review (MDPI 2025)](https://www.mdpi.com/2673-2688/6/9/226)

### Technique — MCP vs RAG
23. [TrueFoundry — MCP vs RAG Key Differences](https://www.truefoundry.com/blog/mcp-vs-rag)
24. [Merge — MCP vs RAG overlap and differ](https://www.merge.dev/blog/rag-vs-mcp)
25. [GitButler — MCP vs RAG context](https://blog.gitbutler.com/mcp-vs-rag)
26. [HyScaler — RAG vs MCP Full Guide 2025](https://hyscaler.com/insights/rag-vs-mcp-full-guide-2/)

---

*Généré par BMAD Method v6 — Creative Intelligence*
*Durée de recherche : ~45 minutes*
*Sources consultées : 26*
