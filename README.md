# 🪐 AstroDistance (chlefastro)

Calculateur haute précision des distances astronomiques et **Calcul du Mois Lunaire (29 ou 30 Jours)**.

Ce projet calcule la distance entre la **Terre** et :
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

Et intègre désormais le **Calcul Complet du Mois de la Lune (Cycle de 29 ou 30 jours)** :
- 🌙 Détermination exacte si le mois compte **29 jours** ou **30 jours**.
- 📅 Âge précis de la Lune (ex: *Jour 7.42 sur 29.74 jours*).
- 🌓 Phase de la Lune actuelle (Nouvelle Lune, Premier Croissant / Hilal, Premier Quartier, Pleine Lune / Badr...).
- 💡 Pourcentage d'illumination du disque lunaire (ex: *43%*).
- 🗓️ Dates et heures précises des 4 phases clés du mois (Nouvelle Lune, 1er Quartier, Pleine Lune, Dernier Quartier).
- 🟢 Périgée (distance minimale du mois) et 🔴 Apogée (distance maximale du mois).
- 📜 Tableau explorateur de **tous les mois lunaires de 2000 à aujourd'hui** (avec indication 29 jours / 30 jours et export CSV).

---

## 🚀 1. Utilisation de l'Application Web Interactive (`index.html`)

L'application web fonctionne **100% hors ligne** et sans aucune dépendance externe.

### Comment l'ouvrir :
- **Option 1 (Double-clic)** : Ouvrez simplement [index.html](file:///Users/latefriad/Downloads/astro/index.html) dans votre navigateur.
- **Option 2 (Terminal Mac)** :
  ```bash
  open index.html
  ```
- **Option 3 (Serveur local)** :
  ```bash
  python3 astro_distances.py --web
  ```

### Fonctionnalités de l'interface :
1. ⚡ **Mode Temps Réel** : Actualisé chaque seconde en direct (distances et vitesses).
2. 📅 **Date & Heure au Choix (2000 - Présent)** : Entrez n'importe quel jour, année, heure, minute, seconde avec boutons de pas rapide.
3. 🌙 **Onglet "Mois Lunaire (29 / 30 Jours)"** :
   - Disque lunaire dessiné dynamiquement avec phase réaliste.
   - Badge indiquant si le mois en cours est un **Mois de 29 Jours** ou **Mois de 30 Jours**.
   - Âge de la Lune avec barre de progression de la lunaison.
   - Calendrier Hégirien / Hijri (ex: *6 Joumada ath-Thania 1448 AH*).
   - Calendrier des 4 phases clés (Nouvelle Lune, Premier Quartier, Pleine Lune, Dernier Quartier).
   - Tableau explorateur de tous les mois de l'année sélectionnée (avec export CSV).
4. 🔭 **Radar Orbital Héliocentrique** : Visualisation 2D en temps réel des orbites planétaires.
5. 📈 **Graphique Historique 2000-Présent** : Courbe des distances au fil des années avec survol interactif et export CSV.

---

## 💻 2. Script Python en Ligne de Commande (`astro_distances.py`)

### A. Rapport complet du Mois Lunaire (29 ou 30 jours) :
```bash
python3 astro_distances.py --lunar
```

### B. Lister tous les mois lunaires d'une année (ex: 2026) avec leur durée (29 ou 30 jours) :
```bash
python3 astro_distances.py --lunar-year 2026
```

### C. Calcul instantané des distances :
```bash
python3 astro_distances.py
```

### D. Calcul pour une date et heure précise :
```bash
python3 astro_distances.py --date "2000-01-01 12:00:00"
```

### E. Mode Direct (Mise à jour chaque seconde dans le terminal) :
```bash
python3 astro_distances.py --live
```

### F. Calcul jour par jour entre 2000 et aujourd'hui (Export CSV) :
```bash
python3 astro_distances.py --range 2000-01-01 2026-11-16 --step day --output distances_2000_2026.csv
```

---

## 📐 Mécanique Céleste & Mois Lunaire (29 ou 30 Jours)

- **Mois Synodique Moyen** : $\approx 29.53059\text{ jours}$ ($29\text{ jours, } 12\text{ heures, } 44\text{ minutes}$).
- **Variation Réelle** : En raison de l'excentricité de l'orbite de la Lune et de la Terre, la durée d'une lunaison réelle oscille entre **$29.27$ jours** ($\approx 29\text{j } 06\text{h}$) et **$29.83$ jours** ($\approx 29\text{j } 20\text{h}$).
- **Règle des 29 / 30 jours** :
  - Si la lunaison astronomique est inférieure à $29.5$ jours, le mois civil/calendaire compte **29 jours**.
  - Si la lunaison astronomique dépasse $29.5$ jours, le mois civil/calendaire compte **30 jours**.
