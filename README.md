# 🪐 AstroDistance (chlefastro)

Calculateur haute précision des distances astronomiques et **Logique Complète du Mois Lunaire : Terre (30 Jours) vs Lune (29.530588... Jours)**.

Ce projet calcule la distance en temps réel entre la **Terre** et :
- 🌕 **La Lune (Moon)**
- ☀️ **Le Soleil (Sun)**
- ☿️ **Mercure (Mercury)**
- ♀️ **Vénus (Venus)**
- ♂️ **Mars**
- ♃ **Jupiter**
- ♄ **Saturne (Saturn)**
- ♅ **Uranus**
- ♆ **Neptune**
- ♇ **Pluton (Pluto)**

Et intègre désormais **toute la logique mathématique et physique du mois lunaire** :
- 📐 **Pourquoi la Lune fait 29.530588... jours alors que la Terre compte 30 jours ?**
- 🔬 Démonstration par la formule des périodes synodiques.
- 📊 Calculs exacts du décalage cumulé depuis l'an 2000 jusqu'à aujourd'hui.
- 🪐 Les **5 types de mois lunaires** (Synodique, Sidéral, Anomalistique, Draconitique, Tropique).
- 🔄 Convertisseur interactif Mois Terrestres (30j) $\leftrightarrow$ Mois Lunaires (29.530588j).
- 🏛️ Le Cycle de Méton (19 ans terrestres = 235 mois lunaires).

---

## 🔬 La Logique Mathématique : Terre (30 Jours) vs Lune (29.530588... Jours)

### 1. Pourquoi le mois lunaire dure-t-il exactement 29.530588 jours ?
1. **La révolution sidérale (360°)** : La Lune met **$27.321661\text{ jours}$** pour faire un tour complet autour de la Terre par rapport aux étoiles fixes.
2. **Le déplacement de la Terre** : Pendant ces $27.32$ jours, la Terre avance elle-même sur son orbite autour du Soleil d'environ **$27°$ d'arc angulaire**.
3. **Le rattrapage (+2.21 jours)** : Pour retrouver la même phase (ex: Nouvelle Lune à Nouvelle Lune), la Lune doit parcourir ces $27°$ supplémentaires, ce qui lui prend **$2.208927\text{ jours}$**.
4. **Formule mathématique fondamentale** :
   $$\frac{1}{T_{\text{synodique}}} = \frac{1}{T_{\text{sidéral}}} - \frac{1}{T_{\text{Terre}}}$$
   $$\frac{1}{T_{\text{synodique}}} = \frac{1}{27.3216615} - \frac{1}{365.256363} = 0.0338653 \implies T_{\text{synodique}} = \mathbf{29.53058885\text{ jours}}$$
   Soit exactement : **$29\text{ jours, } 12\text{ heures, } 44\text{ minutes, } 02.82\text{ secondes}$**.

---

### 2. Pourquoi sur Terre le mois compte 30 jours ?
- **L'année solaire terrestre** dure $365.2422$ jours (temps pour faire un tour complet du Soleil et boucler le cycle des 4 saisons).
- Pour diviser l'année en 12 saisons régulières :
  $$\frac{365.2422}{12} \approx \mathbf{30.43685\text{ jours par mois}}$$
- C'est pourquoi le calendrier solaire terrestre utilise des mois civils de **30 et 31 jours**.

---

### 3. La Logique du Décalage Terre vs Lune
- **Par mois** (base 30 jours) :
  $$30.000000 - 29.530588 = \mathbf{+0.469412\text{ jour}}\quad (11\text{h } 15\text{m } 57\text{s de moins par mois lunaire})$$
- **Par an (L'Épacte)** :
  - 1 an solaire = $365.2422$ jours (12 mois terrestres)
  - 1 an lunaire = $12 \times 29.530588 = \mathbf{354.3671\text{ jours}}$ (12 mois lunaires)
  - **Décalage annuel** : $365.2422 - 354.3671 = \mathbf{10.8751\text{ jours par an}}$ ($\approx 11$ jours d'avance lunaire chaque année).
- **Cycle de 33 ans** :
  $$33 \times 10.8751 \approx 358.9\text{ jours} \approx \mathbf{1\text{ an entier de décalage !}}$$

---

### 4. Les 5 Définitions Astronomiques du Mois de la Lune

| Type de Mois Lunaire | Définition Physique | Durée Décimale | Durée Formatée |
| :--- | :--- | :--- | :--- |
| **1. Mois Synodique (Lunaison)** | Nouvelle Lune $\rightarrow$ Nouvelle Lune (Phases) | **29.530589 j** | **29j 12h 44m 02.9s** |
| **2. Mois Sidéral** | Révolution orbitale à 360° (Étoiles fixes) | 27.321661 j | 27j 07h 43m 11.5s |
| **3. Mois Anomalistique** | Périgée $\rightarrow$ Périgée (Distance min/max) | 27.554550 j | 27j 13h 18m 33.1s |
| **4. Mois Draconitique** | Nœud orbital $\rightarrow$ Nœud (Cycle des éclipses) | 27.212221 j | 27j 05h 05m 35.8s |
| **5. Mois Tropique** | Par rapport au Point Vernal terrestre | 27.321582 j | 27j 07h 43m 04.7s |

---

## 🚀 Utilisation de l'Application Web Interactive (`index.html`)

Ouvrez simplement [index.html](file:///Users/latefriad/Downloads/astro/index.html) dans votre navigateur (ou tapez `open index.html`).

- ⚡ **Onglet "Temps Réel"** : Toutes les distances calculées chaque seconde en direct.
- 📅 **Onglet "Date & Heure"** : Entrez n'importe quelle date/heure entre 2000 et 2099.
- 🌙 **Onglet "Logique & Calculs Mois Lunaire (29.53j)"** :
  - Disque lunaire interactif avec phases réalistes.
  - Formules mathématiques complètes et démonstrations.
  - Compteurs en direct depuis l'an 2000 (Jours, Mois de 30j, Mois lunaires, Écart).
  - Convertisseur interactif Terre $\leftrightarrow$ Lune.
  - Tableau des 5 types de mois lunaires.
  - Explorateur de tous les mois lunaires par année avec durée (29 ou 30 jours).
- 🔭 **Radar Orbital Héliocentrique** : Visualisation 2D en temps réel des orbites.
- 📈 **Graphique Historique 2000-Présent** : Courbes d'évolution et export CSV.

---

## 💻 Script Python en Ligne de Commande (`astro_distances.py`)

### A. Afficher toute la logique et les formules :
```bash
python3 astro_distances.py --logic
```

### B. Rapport complet du mois lunaire actuel :
```bash
python3 astro_distances.py --lunar
```

### C. Liste de tous les mois lunaires d'une année (ex: 2026) :
```bash
python3 astro_distances.py --lunar-year 2026
```

### D. Calcul des distances instantanées :
```bash
python3 astro_distances.py
```

### E. Mode direct rafraîchi chaque seconde dans le terminal :
```bash
python3 astro_distances.py --live
```
