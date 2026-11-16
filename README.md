# 🪐 AstroDistance — Calculateur de Distances Terre, Lune & Toutes les Planètes

Calcul haute précision des distances entre la **Terre** et :
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

Ce projet répond directement à votre demande :
1. **Entrez simplement l'année, le jour et l'heure**, et l'outil calcule instantanément toutes les distances.
2. **Mode temps réel (Chaque Seconde)** : actualisation automatique chaque seconde montrant l'évolution exacte en kilomètres et en vitesse d'approche ou d'éloignement.
3. **Calcul jour par jour ou seconde par seconde entre 2000 et aujourd'hui (ou n'importe quelle période)** avec graphique interactif et export CSV/JSON.

---

## 🚀 1. Utilisation de l'Application Web Interactive (`index.html`)

L'application web fonctionne **100% hors ligne** et sans aucune dépendance externe.

### Comment l'ouvrir :
- **Option 1 (Double-clic)** : Ouvrez simplement le fichier `index.html` dans votre navigateur (Chrome, Safari, Firefox, Edge).
- **Option 2 (Terminal Mac)** :
  ```bash
  open index.html
  ```
- **Option 3 (Serveur local automatique)** :
  ```bash
  python3 astro_distances.py --web
  ```

### Fonctionnalités de l'interface :
- ⚡ **Onglet "Temps Réel"** : Met à jour chaque seconde toutes les distances en direct (km, UA, miles, temps de parcours de la lumière).
- 📅 **Onglet "Date & Heure au Choix"** : Sélectionnez l'année (de 2000 à 2099), le mois, le jour, l'heure, la minute et la seconde. Boutons de raccourcis (+1s, -1s, +1j, -1j, J2000, etc.).
- ⏯️ **Onglet "Simulation"** : Avancez dans le temps à vitesse accélérée (1 heure/s, 1 jour/s, 1 mois/s).
- 🔭 **Radar Orbital Héliocentrique** : Carte 2D en temps réel des orbites du Système Solaire avec faisceau reliant la Terre à l'astre choisi.
- 📈 **Graphique Historique 2000-Présent** : Affiche la courbe des distances au fil des années, avec infobulles au survol pour identifier les oppositions (plus proches approches).
- 💾 **Bouton "Exporter CSV"** : Télécharge instantanément un tableur Excel / CSV avec toutes les valeurs calculées.
- 🌐 **Bilingue** : Basculez entre le Français et l'Anglais en un clic.

---

## 💻 2. Utilisation en Ligne de Commande Python (`astro_distances.py`)

Un script Python performant est également prêt à l'emploi.

### A. Distance actuelle instantanée :
```bash
python3 astro_distances.py --lang fr
```

### B. Distance pour une date et heure précise :
```bash
python3 astro_distances.py --date "2000-01-01 12:00:00" --lang fr
python3 astro_distances.py --date "2024-08-15 20:30:15" --lang fr
```

### C. Mode Direct dans le Terminal (Mise à jour chaque seconde) :
```bash
python3 astro_distances.py --live --lang fr
```
*(Appuyez sur `Ctrl+C` pour quitter)*

### D. Calcul jour par jour entre 2000 et aujourd'hui (Export CSV) :
```bash
python3 astro_distances.py --range 2000-01-01 2026-11-16 --step day --output distances_2000_2026.csv
```

### E. Calcul chaque seconde (sur une plage courte) :
```bash
python3 astro_distances.py --range "2026-11-16 12:00:00" "2026-11-16 12:05:00" --step second --output par_seconde.csv
```

---

## 📐 Grandeurs et Précision des Calculs

- **Algorithmes** : Basés sur les éphémérides VSOP87 (planètes) et ELP2000 (Lune), avec correction du temps de trajet de la lumière et de l'aberration.
- **Unité Astronomique (UA)** : $1\text{ UA} = 149\,597\,870.7\text{ km}$ (distance moyenne Terre-Soleil).
- **Temps lumière** : Calculé à la vitesse de la lumière $c = 299\,792.458\text{ km/s}$ :
  - Terre $\leftrightarrow$ Lune : $\approx 1.28$ à $1.35$ seconde
  - Terre $\leftrightarrow$ Soleil : $\approx 8$ minutes 13 secondes
  - Terre $\leftrightarrow$ Mars : de $3$ minutes (au plus proche) à $22$ minutes (au plus loin)
  - Terre $\leftrightarrow$ Pluton : $\approx 4$ à $5$ heures
- **Vitesse Radiale (km/s)** : Dérivée par différence finie instantanée à $1\text{ s}$, indiquant en temps réel si l'astre se rapproche (▼) ou s'éloigne (▲) de la Terre.

# chlefastro
