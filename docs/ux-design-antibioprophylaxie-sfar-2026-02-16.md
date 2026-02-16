# UX Design : Antibioprophylaxie SFAR

**Date :** 2026-02-16
**Designer :** Thomas Boulier (assisté par Claude)
**Version :** 1.0
**Plateformes :** Web responsive (mobile 375px → desktop 1920px)
**Accessibilité :** Bonnes pratiques (Lighthouse > 80)
**Style :** Sobre, professionnel, inspiré de la charte SFAR

---

## Résumé

Design d'une webapp de consultation des recommandations d'antibioprophylaxie chirurgicale (RFE SFAR 2024). L'objectif UX principal est **zéro friction** : un anesthésiste au bloc opératoire doit trouver le bon antibiotique en moins de 5 secondes, sur téléphone ou PC, sans compte ni authentification.

**Périmètre :** 5 écrans, 3 flux principaux, 1 chatbot IA intégré.

---

## Principes de design

1. **La recherche d'abord** — La barre de recherche est le point d'entrée principal, en autofocus. Comme Google : on arrive, on tape, on trouve.
2. **Scannable en 2 secondes** — Au bloc, on porte des gants, on est pressé. L'information critique (molécule + dose) doit sauter aux yeux.
3. **Zéro friction** — Pas de login, pas de modal, pas de cookie banner. Accès immédiat au contenu.
4. **Mobile-first** — L'usage principal est sur téléphone au bloc. Le desktop est un bonus (station d'anesthésie).
5. **Source toujours visible** — Chaque protocole cite sa source exacte (page PDF, tableau). C'est un outil médical, la traçabilité est non-négociable.

---

## Flux utilisateurs

### Flux 1 : Recherche rapide (chemin principal)

**Contexte :** L'anesthésiste est au bloc, il a besoin de l'ATB pour une PTH.

```
[Accueil]
   ↓ tape "hanche" (autofocus sur la recherche)
[Résultats temps réel] (dès 2-3 caractères, < 200ms)
   ↓ clique sur "Prothèse totale de hanche"
[Protocole] → Céfazoline 2g IV, 30min avant incision
```

**Temps cible :** < 5 secondes de l'ouverture de l'app au protocole affiché.

**Cas d'erreur :**
- Aucun résultat → Message "Aucune intervention trouvée. Essayez un autre terme ou parcourez par spécialité."
- Terme ambigu → Tous les résultats correspondants affichés

---

### Flux 2 : Navigation par arborescence

**Contexte :** L'anesthésiste ne connaît pas le nom exact ou veut voir toutes les interventions d'une spécialité.

```
[Accueil]
   ↓ clique sur une carte spécialité (ou "Parcourir")
[Vue spécialité] → liste des interventions avec aperçu du protocole
   ↓ option A : clique sur une intervention → [Protocole]
   ↓ option B : "Tout déplier" → voit tous les protocoles d'un coup
```

**Point de design :** La vue spécialité affiche par défaut la liste des interventions avec un aperçu (molécule principale). Un bouton "Tout déplier" permet de voir tous les protocoles complets sans cliquer un par un.

---

### Flux 3 : Question au chatbot IA

**Contexte :** L'anesthésiste préfère poser une question en langage naturel.

```
[N'importe quel écran] → clique sur bouton chat (💬)
[Chatbot]
   ↓ tape "je mets quoi sur une PTH ?"
[Réponse IA] → protocole formaté + source cliquable
   ↓ clique sur la source → [Protocole]
```

**Cas limites :**
- Question hors périmètre → "Je n'ai pas trouvé cette information dans les RFE SFAR 2024."
- Question ambiguë → Le chatbot propose les interventions les plus proches
- Temps de réponse → Indicateur de chargement, réponse < 10s

---

## Wireframes

### Écran 1 : Accueil

L'écran le plus important. La barre de recherche est le héros.

#### Mobile (375px)

```
┌─────────────────────────┐
│  ATB SFAR    [💬]       │ ← Header compact
├─────────────────────────┤
│                         │
│  Antibioprophylaxie     │ ← H1
│  chirurgicale           │
│  RFE SFAR 2024          │ ← Sous-titre discret
│                         │
│  ┌─────────────────┐    │
│  │ 🔍 Rechercher...│    │ ← Barre de recherche
│  └─────────────────┘    │   autofocus
│                         │
│  ou parcourir par       │
│  spécialité ↓           │
│                         │
│  ┌─────────────────┐    │
│  │ Orthopédie      › │  │
│  │ Digestif        › │  │ ← Liste spécialités
│  │ Urologie        › │  │   (accordéon)
│  │ Cardiaque       › │  │
│  │ Gynécologie     › │  │
│  │ Neurochirurgie  › │  │
│  │ ORL / Stomato   › │  │
│  │ Thoracique      › │  │
│  │ ...             › │  │
│  └─────────────────┘    │
│                         │
├─────────────────────────┤
│ Outil de consultation · │ ← Footer disclaimer
│ Ne remplace pas le      │   permanent, discret
│ jugement clinique.      │
│ Source : RFE SFAR 2024  │
└─────────────────────────┘
```

#### Desktop (1200px)

```
┌──────────────────────────────────────────────────────────┐
│  ATB SFAR          Rechercher    Parcourir    [💬 Chat]  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│              Antibioprophylaxie chirurgicale              │
│                    RFE SFAR 2024                         │
│                                                          │
│           ┌──────────────────────────────┐               │
│           │ 🔍 Rechercher une interven...│               │
│           └──────────────────────────────┘               │
│                                                          │
│    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│    │Orthopédie│ │ Digestif │ │ Urologie │ │Cardiaque │  │
│    │  12 int. │ │  15 int. │ │   8 int. │ │  10 int. │  │
│    └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│    │Gynéco    │ │ Neuro    │ │ORL/Stoma │ │ Thorax   │  │
│    └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Outil de consultation · Ne remplace pas le jugement      │
│ clinique · Source : RFE SFAR 2024                        │
└──────────────────────────────────────────────────────────┘
```

**Interactions :**
- Autofocus sur la barre de recherche au chargement
- Les résultats apparaissent en overlay sous la barre dès 2-3 caractères (voir Écran 2)
- Clic sur une spécialité → Écran 3 (Vue spécialité)
- Clic sur 💬 → Écran 5 (Chatbot)

---

### Écran 2 : Résultats de recherche (type-ahead)

Les résultats s'affichent **sous la barre de recherche** en temps réel, comme un autocomplete enrichi. Pas une page séparée — c'est un overlay/dropdown.

#### Mobile

```
┌─────────────────────────┐
│  ← ATB SFAR      [💬]  │
├─────────────────────────┤
│  ┌─────────────────┐    │
│  │ 🔍 hanch█       │    │ ← Saisie en cours
│  └─────────────────┘    │
│                         │
│  3 résultats            │
│                         │
│  ┌─────────────────┐    │
│  │ Prothèse totale │    │
│  │ de hanche (PTH) │    │ ← Nom intervention (gras)
│  │ Orthopédie      │    │ ← Spécialité (gris)
│  │ Céfazoline 2g   │    │ ← Aperçu protocole
│  └─────────────────┘    │
│  ┌─────────────────┐    │
│  │ Reprise de PTH  │    │
│  │ Orthopédie      │    │
│  │ Céfazoline 2g   │    │
│  └─────────────────┘    │
│  ┌─────────────────┐    │
│  │ Fracture col    │    │
│  │ du fémur/hanche │    │
│  │ Orthopédie      │    │
│  │ Céfazoline 2g   │    │
│  └─────────────────┘    │
│                         │
├─────────────────────────┤
│ Disclaimer footer       │
└─────────────────────────┘
```

**Interactions :**
- Résultats mis à jour à chaque frappe (debounce 100ms)
- Clic sur un résultat → Écran 4 (Protocole)
- Touche Escape ou clic hors résultats → ferme l'overlay
- Aucun résultat → "Aucune intervention trouvée" + lien "Parcourir par spécialité"
- Navigation clavier : flèches haut/bas + Enter

---

### Écran 3 : Vue spécialité

Affiche toutes les interventions d'une spécialité avec aperçu.

#### Mobile — Vue par défaut (liste)

```
┌─────────────────────────┐
│  ← Orthopédie    [💬]  │
├─────────────────────────┤
│  🔍 Filtrer...          │ ← Filtre local
│                         │
│  12 interventions       │
│  [Tout déplier]         │ ← Bouton toggle
│                         │
│  ┌─────────────────┐    │
│  │ PTH             › │  │
│  │ Céfazoline 2g     │  │ ← Aperçu
│  ├─────────────────┤    │
│  │ PTG             › │  │
│  │ Céfazoline 2g     │  │
│  ├─────────────────┤    │
│  │ Fracture col    › │  │
│  │ fémur              │  │
│  │ Céfazoline 2g     │  │
│  ├─────────────────┤    │
│  │ Arthroscopie    › │  │
│  │ Pas d'ABP         │  │
│  └─────────────────┘    │
│  ...                    │
├─────────────────────────┤
│ Disclaimer footer       │
└─────────────────────────┘
```

#### Mobile — Vue dépliée (tous les protocoles)

```
┌─────────────────────────┐
│  ← Orthopédie    [💬]  │
├─────────────────────────┤
│  🔍 Filtrer...          │
│                         │
│  12 interventions       │
│  [Tout replier]         │
│                         │
│  ▾ PTH                  │
│  ┌─────────────────┐    │
│  │ CÉFAZOLINE       │   │
│  │ 2g IV · 30min    │   │ ← Protocole complet
│  │ avant incision   │   │   visible directement
│  │ Réinj: 1g /4h    │   │
│  │ Allergie: Clinda │   │
│  │ 900mg IV         │   │
│  │ 📄 p.73          │   │
│  └─────────────────┘    │
│                         │
│  ▾ PTG                  │
│  ┌─────────────────┐    │
│  │ CÉFAZOLINE       │   │
│  │ 2g IV · 30min    │   │
│  │ ...               │  │
│  └─────────────────┘    │
│  ...                    │
└─────────────────────────┘
```

**Interactions :**
- "Tout déplier" / "Tout replier" → toggle global
- Clic sur une intervention (vue liste) → Écran 4 (Protocole)
- Clic sur une intervention (vue dépliée) → replie/déplie individuellement
- Filtre local → filtre les interventions de cette spécialité uniquement
- Bouton ← → retour à l'accueil

---

### Écran 4 : Protocole (détail intervention)

L'écran qu'on regarde au bloc. **Lisibilité maximale.**

#### Mobile

```
┌─────────────────────────┐
│  ← Orthopédie    [💬]  │
├─────────────────────────┤
│                         │
│  Prothèse totale        │ ← H1
│  de hanche (PTH)        │
│                         │
│  ┌─────────────────┐    │
│  │ CÉFAZOLINE       │   │ ← Bloc principal
│  │                  │   │   fond légèrement
│  │ Posologie  2g IV │   │   teinté (bleu clair)
│  │ Timing     30min │   │
│  │            avant │   │
│  │            incis.│   │
│  │ Réinjection 1g   │   │
│  │            /4h   │   │
│  │ Durée      Dose  │   │
│  │            unique│   │
│  └─────────────────┘    │
│                         │
│  ┌─────────────────┐    │
│  │ ⚠ ALLERGIE      │   │ ← Bloc alternatif
│  │                  │   │   fond orangé/warning
│  │ Clindamycine     │   │
│  │ 900mg IV         │   │
│  │ Réinj: 600mg/6h  │  │
│  └─────────────────┘    │
│                         │
│  📄 Source : RFE 2024   │ ← Lien cliquable
│     Tableau 12, p.73    │   vers le PDF
│                         │
├─────────────────────────┤
│ Disclaimer footer       │
└─────────────────────────┘
```

#### Desktop

```
┌──────────────────────────────────────────────────────────┐
│  ATB SFAR    Orthopédie > PTH            [💬 Chat]       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Prothèse totale de hanche (PTH)                        │
│                                                          │
│  ┌────────────────────────┐  ┌────────────────────────┐  │
│  │ CÉFAZOLINE              │  │ ⚠ ALLERGIE            │  │
│  │                         │  │                        │  │
│  │ Posologie    2g IV      │  │ Clindamycine           │  │
│  │ Timing       30min      │  │ 900mg IV               │  │
│  │              avant      │  │ Réinj: 600mg / 6h     │  │
│  │              incision   │  │                        │  │
│  │ Réinjection  1g / 4h    │  │                        │  │
│  │ Durée        Dose       │  │                        │  │
│  │              unique     │  │                        │  │
│  └────────────────────────┘  └────────────────────────┘  │
│                                                          │
│  📄 Source : RFE SFAR 2024 — Tableau 12, page 73         │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Disclaimer footer                                        │
└──────────────────────────────────────────────────────────┘
```

**Design du bloc protocole :**
- Molécule en **gras, grande taille** (c'est l'info n°1)
- Labels à gauche, valeurs à droite (tableau implicite, lisible)
- Bloc allergie visuellement distinct : bordure orange, fond orangé léger
- Sur desktop : les deux blocs côte à côte
- Sur mobile : empilés verticalement

---

### Écran 5 : Chatbot IA

Interface de chat accessible depuis n'importe quel écran via le bouton 💬.

#### Mobile

```
┌─────────────────────────┐
│  ← Chat IA       ATB   │
├─────────────────────────┤
│                         │
│  ┌─────────────────┐    │
│  │ Posez une ques-  │   │ ← Message d'accueil
│  │ tion sur l'anti- │   │
│  │ bioprophylaxie.  │   │
│  │                  │   │
│  │ Ex: "je mets     │   │
│  │ quoi sur une     │   │
│  │ PTH ?"           │   │
│  └─────────────────┘    │
│                         │
│         ┌──────────────┐│
│         │je mets quoi  ││ ← Bulle user (droite)
│         │sur une PTH ? ││
│         └──────────────┘│
│                         │
│  ┌─────────────────┐    │
│  │ Pour une PTH,    │   │ ← Bulle IA (gauche)
│  │ la RFE 2024      │   │
│  │ recommande :      │   │
│  │                   │   │
│  │ ┌───────────────┐ │  │
│  │ │ CÉFAZOLINE    │ │  │ ← Carte protocole
│  │ │ 2g IV         │ │  │   intégrée dans
│  │ │ 30min avant   │ │  │   la réponse
│  │ │ incision      │ │  │
│  │ │ Réinj: 1g/4h  │ │  │
│  │ │               │ │  │
│  │ │ Allergie:     │ │  │
│  │ │ Clinda 900mg  │ │  │
│  │ └───────────────┘ │  │
│  │                   │  │
│  │ 📄 Source: p.73   │  │ ← Lien cliquable
│  │    Voir protocole │  │
│  └─────────────────┘    │
│                         │
├─────────────────────────┤
│ ┌───────────────┐ [➤]  │ ← Input toujours
│ │ Votre question│       │   visible en bas
│ └───────────────┘       │
└─────────────────────────┘
```

**Interactions :**
- Le chat s'ouvre en plein écran sur mobile, en panneau latéral sur desktop
- Indicateur de chargement ("..." animé) pendant la génération (< 10s)
- Les réponses contiennent des **cartes protocole** cliquables (même composant que l'écran Protocole)
- "📄 Voir protocole" → navigation vers l'écran Protocole complet
- Historique de la conversation conservé pendant la session
- Bouton "Nouvelle conversation" pour repartir de zéro

**Réponse hors périmètre :**
```
  ┌─────────────────┐
  │ Je n'ai pas      │
  │ trouvé cette     │
  │ information dans │
  │ les RFE SFAR     │
  │ 2024.            │
  │                  │
  │ Essayez de       │
  │ reformuler ou    │
  │ utilisez la      │
  │ recherche.       │
  └─────────────────┘
```

---

## Design Tokens

Inspirés de la charte visuelle SFAR (sfar.org) et adaptés au contexte médical.

### Couleurs

```
Primaire (hérité SFAR) :
  --color-primary:        #273466   (bleu foncé SFAR — textes, header)
  --color-primary-light:  #3a4d8c   (hover, liens)

Accents :
  --color-accent:         #0cc9bf   (turquoise SFAR — boutons, liens actifs)
  --color-accent-dark:    #0aab a2  (hover sur accent)

Alerte / Allergie :
  --color-warning:        #f15c40   (orange SFAR — blocs allergie, alertes)
  --color-warning-bg:     #fef3f1   (fond bloc allergie)

Neutres :
  --color-bg:             #ffffff   (fond principal)
  --color-bg-subtle:      #f5f7fa   (fond cartes protocole)
  --color-border:         #e2e6ea   (bordures)
  --color-text:           #273466   (texte principal — même que primary)
  --color-text-secondary: #6c757d   (texte secondaire, spécialités)
  --color-text-muted:     #9ca3af   (disclaimers, hints)

Chatbot :
  --color-chat-user:      #273466   (bulle user)
  --color-chat-user-text: #ffffff
  --color-chat-ai:        #f5f7fa   (bulle IA)
  --color-chat-ai-text:   #273466

Succès / Info :
  --color-success:        #16a34a   (messages positifs)
  --color-info:           #0cc9bf   (info, tips)
```

### Typographie

```
Font family:
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
  --font-mono: "SF Mono", Monaco, "Cascadia Code", monospace

Échelle (mobile → desktop) :
  --text-xs:    12px / 14px     (disclaimers, source)
  --text-sm:    14px / 14px     (labels, texte secondaire)
  --text-base:  16px / 16px     (corps de texte — min 16px pour éviter le zoom iOS)
  --text-lg:    18px / 20px     (sous-titres)
  --text-xl:    24px / 28px     (titres de section)
  --text-2xl:   28px / 36px     (titre principal)
  --text-3xl:   20px / 24px     (nom de molécule dans les cartes)

Poids :
  --font-normal:   400
  --font-medium:   500
  --font-semibold: 600
  --font-bold:     700
```

### Espacement

```
Base : 8px

  --space-1:   4px
  --space-2:   8px
  --space-3:   12px
  --space-4:   16px
  --space-5:   20px
  --space-6:   24px
  --space-8:   32px
  --space-10:  40px
  --space-12:  48px
  --space-16:  64px
```

### Breakpoints

```
  --bp-mobile:  375px   (min supporté)
  --bp-tablet:  768px
  --bp-desktop: 1024px
  --bp-wide:    1200px  (max-width du contenu)
```

### Ombres et rayons

```
  --shadow-sm:   0 1px 2px rgba(0,0,0,0.05)
  --shadow-md:   0 4px 6px rgba(0,0,0,0.07)
  --shadow-lg:   0 10px 15px rgba(0,0,0,0.10)

  --radius-sm:   4px    (boutons, inputs)
  --radius-md:   8px    (cartes)
  --radius-lg:   12px   (modals, chat)
  --radius-full: 9999px (badges, pills)
```

---

## Bibliothèque de composants

### Composant : Barre de recherche (SearchBar)

**Usage :** Écran d'accueil, haut de page

**Structure :**
- Icône loupe (gauche, 20px)
- Input texte (placeholder : "Rechercher une intervention...")
- Bouton clear (×) quand texte saisi

**Tailles :**
- Accueil : grande (48px hauteur, texte 18px)
- Header/navigation : compacte (40px hauteur, texte 16px)

**États :**
- Default : bordure `--color-border`, fond blanc
- Focus : bordure `--color-accent`, ombre `--shadow-sm`
- Avec texte : bouton clear visible
- Avec résultats : dropdown ouvert en dessous

---

### Composant : Carte de résultat (SearchResult)

**Usage :** Dropdown de recherche type-ahead

**Structure :**
- Nom de l'intervention (gras, `--text-base`)
- Spécialité (secondaire, `--color-text-secondary`, `--text-sm`)
- Aperçu protocole (molécule principale, `--text-sm`)

**États :**
- Default : fond blanc
- Hover / focus clavier : fond `--color-bg-subtle`
- Active : fond `--color-accent` à 10% opacité

---

### Composant : Carte protocole (ProtocolCard)

**Usage :** Écran protocole, vue spécialité dépliée, réponse chatbot

C'est le composant central de l'application.

**Structure :**
```
┌──────────────────────┐
│ NOM DE LA MOLÉCULE   │ ← Gras, --text-3xl, --color-primary
│                      │
│ Posologie    2g IV   │ ← Tableau label/valeur
│ Timing       30min   │   Labels en --color-text-secondary
│              avant   │   Valeurs en --font-semibold
│              incis.  │
│ Réinjection  1g /4h  │
│ Durée        ...     │
└──────────────────────┘
```

**Variantes :**
- **Standard** : fond `--color-bg-subtle`, bordure gauche `--color-accent` (4px)
- **Allergie** : fond `--color-warning-bg`, bordure gauche `--color-warning` (4px), badge "⚠ ALLERGIE" en haut

**Tailles :**
- Complet (écran protocole) : largeur 100%, espacement généreux
- Compact (résultat de recherche, chatbot) : réduit, moins d'espacement
- Inline (vue spécialité dépliée) : dans le flux de la liste

---

### Composant : Carte spécialité (SpecialtyCard)

**Usage :** Grille sur l'accueil (desktop), liste sur mobile

**Structure :**
- Nom de la spécialité (gras)
- Nombre d'interventions (secondaire)

**États :**
- Default : fond blanc, bordure `--color-border`
- Hover : ombre `--shadow-md`, bordure `--color-accent`

---

### Composant : Bouton chat (ChatFAB)

**Usage :** Bouton flottant sur tous les écrans (sauf chatbot)

**Structure :**
- Bouton rond, 56px × 56px
- Icône 💬 (24px)
- Position : fixed, bottom-right (16px de marge)

**États :**
- Default : fond `--color-accent`, icône blanche
- Hover : fond `--color-accent-dark`
- Desktop : peut être intégré dans la nav au lieu d'un FAB

---

### Composant : Bulle de chat (ChatBubble)

**Usage :** Écran chatbot

**Variantes :**
- **User** : alignée à droite, fond `--color-chat-user`, texte blanc, radius arrondi sauf coin bas-droit
- **IA** : alignée à gauche, fond `--color-chat-ai`, texte `--color-chat-ai-text`, peut contenir une ProtocolCard

---

### Composant : Footer disclaimer

**Usage :** Présent sur tous les écrans, en bas

**Structure :**
- Texte en `--text-xs`, couleur `--color-text-muted`
- Contenu : "Outil de consultation · Ne remplace pas le jugement clinique · Source : RFE SFAR 2024"
- Centré, padding vertical `--space-4`

---

## Accessibilité

### Bonnes pratiques appliquées (cible Lighthouse > 80)

**HTML sémantique :**
- `<header>` pour le header/nav
- `<main>` pour le contenu principal
- `<footer>` pour le disclaimer
- `<nav>` pour la navigation
- `<section>` pour les groupes de contenu
- `<h1>` unique par page, hiérarchie H1 → H2 → H3 respectée

**Contraste vérifié :**
- Texte principal (`#273466` sur `#ffffff`) : ratio 11.5:1 ✓ (AAA)
- Texte secondaire (`#6c757d` sur `#ffffff`) : ratio 4.6:1 ✓ (AA)
- Texte muted (`#9ca3af` sur `#ffffff`) : ratio 2.9:1 — uniquement pour le disclaimer (décoratif)
- Accent (`#0cc9bf` sur `#ffffff`) : ratio 2.8:1 — utilisé uniquement pour les bordures/icônes, pas pour du texte seul
- Warning (`#f15c40` sur `#ffffff`) : ratio 3.3:1 — utilisé avec du texte foncé à côté

**Navigation clavier :**
- Tab pour naviguer entre éléments interactifs
- Enter pour activer boutons/liens
- Escape pour fermer le chatbot ou l'overlay de recherche
- Flèches haut/bas dans les résultats de recherche
- Focus visible : outline 2px `--color-accent`, offset 2px

**Formulaires :**
- La barre de recherche a un `aria-label="Rechercher une intervention chirurgicale"`
- Le champ de chat a un `aria-label="Posez une question sur l'antibioprophylaxie"`
- Les résultats de recherche utilisent `role="listbox"` et `role="option"`

**Images / Icônes :**
- Icônes décoratives : `aria-hidden="true"`
- Icônes fonctionnelles (loupe, chat, fermer) : `aria-label` descriptif

**Responsive :**
- Taille de texte minimale 16px (évite le zoom automatique iOS)
- Cibles tactiles minimum 44px × 44px
- Pas de scroll horizontal
- Contenu lisible à 200% de zoom

**Skip link :**
- Lien "Aller au contenu principal" visible au focus, caché sinon

---

## Handoff développeur

### Priorités d'implémentation

Les wireframes et composants ci-dessus deviennent des user stories dans le sprint planning :

**Fondations (sprint 1) :**
1. Design tokens (variables CSS) et reset/base styles
2. Composant ProtocolCard (c'est le composant central, réutilisé partout)
3. Composant SearchBar + logique type-ahead
4. Layout de base (header, main, footer disclaimer)

**Écrans principaux (sprint 2) :**
5. Écran d'accueil (recherche + grille spécialités)
6. Résultats de recherche (overlay type-ahead)
7. Écran protocole (détail intervention)
8. Vue spécialité (liste + toggle déplier)

**Chatbot (sprint 3) :**
9. Écran chatbot (bulles + input)
10. Intégration IA (appel API LLM, formatage réponse)
11. Carte protocole dans les réponses chatbot

### Approche technique suggérée

- **Mobile-first** : coder pour 375px d'abord, puis ajouter les media queries
- **CSS custom properties** : utiliser les design tokens comme variables CSS
- **Composants réutilisables** : ProtocolCard est utilisé dans 3 contextes (protocole, spécialité dépliée, chatbot)
- **Pas de framework CSS** : les composants sont peu nombreux, un framework serait overkill

### Points d'attention

- **Performance recherche** : debounce 100ms sur l'input, résultats < 200ms
- **Autofocus** : la recherche prend le focus au chargement (sauf si l'utilisateur arrive sur un protocole en URL directe)
- **Chatbot sur mobile** : plein écran (pas un petit widget), car l'écran est petit
- **Chatbot sur desktop** : panneau latéral (1/3 de l'écran) ou plein écran, à tester
- **"Pas d'ABP"** : certaines interventions n'ont pas d'antibioprophylaxie recommandée. Afficher clairement "Pas d'antibioprophylaxie recommandée" (pas un protocole vide)

---

## Couverture des exigences

| Exigence | Écran(s) concerné(s) | Couvert |
|----------|----------------------|---------|
| FR-003 Recherche instantanée | Accueil, Résultats | ✓ |
| FR-004 Navigation arborescence | Accueil, Vue spécialité | ✓ |
| FR-005 Affichage protocole | Protocole, Vue spécialité (dépliée) | ✓ |
| FR-006 Disclaimer médical | Footer (tous les écrans) | ✓ |
| FR-007 Chatbot langage naturel | Chatbot | ✓ |
| FR-008 Sourçage réponses IA | Chatbot (lien source dans réponses) | ✓ |
| NFR-001 Temps réponse < 200ms | Recherche type-ahead | ✓ |
| NFR-002 Temps chatbot < 10s | Chatbot (indicateur chargement) | ✓ |
| NFR-004 Pas d'authentification | Aucun écran de login | ✓ |
| NFR-006 Design responsive | Wireframes mobile + desktop | ✓ |
| NFR-007 Accessibilité de base | Section accessibilité | ✓ |

---

## Questions ouvertes (à valider en développement)

1. **Vue spécialité : liste vs tout déplié** — prévoir les deux et tester avec des utilisateurs
2. **Chatbot desktop : panneau latéral vs plein écran** — à tester
3. **Nombre de résultats dans le type-ahead** — 5 ? 10 ? tous ?
4. **Suggestions dans le chatbot** — afficher des questions suggérées au premier lancement ?

---

*Généré par BMAD Method v6 — UX Designer*
*Date : 2026-02-16*

*Pour continuer : lancer `/bmad:architecture` pour concevoir l'architecture technique, puis `/bmad:sprint-planning` pour planifier le développement.*
