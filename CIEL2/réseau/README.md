# Réseau — BTS CIEL IR 2ᵉ année

Supports LaTeX (cours Beamer, TD, TP Packet Tracer, TP Wireshark) bâtis sur un
**fil rouge** unique : la plage `192.168.10.0/24` découpée en VLSM.

| Service | Réseau | Passerelle |
|---|---|---|
| Production VLAN 10 | 192.168.10.0/25 | .126 |
| Administration VLAN 20 | 192.168.10.128/26 | .190 |
| Wi-Fi invité VLAN 30 | 192.168.10.192/27 | .222 |
| Liaison R1–R2 | 192.168.10.224/30 | — |
| Liaison R2–FW | 192.168.10.228/30 | — |

Convention : passerelle = dernière adresse utilisable. Espace libre : `.232/29`, `.240/28`.

## Progression (dossiers par thématique)

| Ordre | Dossier | Contenu | Durée | État |
|---|---|---|---|---|
| 1 | `subnetting-vlsm/` | Ch. 2 — cours + TD : binaire, ET logique, taille de bloc, subnetting, VLSM | 8–10 h | séance 1 (pilote) |
| 2 | `subnetting-vlsm/` | Ch. 3 — TP Packet Tracer : plan fil rouge (VLAN, inter-VLAN, DHCP, statique) + éval courte | 4–6 h | TP (pilote) |
| 3 | `ospf/` | Ch. 4 — cours + TP Packet Tracer OSPF zone unique + éval courte | 6–8 h | à faire |
| 4 | `wireshark-transport/` | Ch. 5 — cours TCP/UDP + TP captures (ARP, ICMP, DHCP, DNS, TCP) | 8–10 h | à faire |

Chaque thématique contient `cours/` (Beamer), `tp/` (TD, TP, évaluations), `pdf/` (sorties)
et `packet-tracer/` ou `captures/`. Le cours `Cours1_CIDR_Sous-reseaux` (à la racine) est antérieur
à cette série.

Prérequis supposés : VLAN/trunk 802.1Q, routage inter-VLAN + DHCP, routage statique.

## Compilation

```bash
make            # tout (versions élève + prof/corrigé)
make ospf       # une thématique : subnetting-vlsm, ospf, wireshark-transport
make verif      # contrôle arithmétique des adresses (Python ipaddress)
make png        # PNG de contrôle visuel dans build/png
make clean      # supprime build/ ; make distclean supprime aussi les PDF
```

Chaque `NOM.tex` de `cours/` ou `tp/` produit dans `pdf/` :
`NOM.pdf` (élève) et `NOM-prof.pdf` (cours) ou `NOM-corrige.pdf` (TP/TD/éval).
Le booléen est `\ifcorrige`, positionné par `\def\cielcorrige{1}` en ligne de commande.

Compilation manuelle d'un fichier (depuis son dossier) :

```bash
export TEXINPUTS=/chemin/ensignement_2027/CIEL2/réseau/commun//:
lualatex fichier.tex                                   # élève
lualatex -jobname=fichier-corrige "\def\cielcorrige{1}\input{fichier.tex}"
```

### Paquets (Ubuntu / WSL)

```bash
sudo apt install texlive-luatex texlive-latex-extra texlive-pictures \
                 texlive-lang-french texlive-fonts-recommended fonts-inter \
                 fonts-dejavu poppler-utils python3
```

### Polices

| Usage | Police | Installation |
|---|---|---|
| Titres et texte | Libre Baskerville (Regular, Bold, Italic) | Google Fonts → `~/.fonts/`, puis `fc-cache -f` |
| Étiquettes, numéros, tags | Inter SemiBold / Bold | paquet `fonts-inter` |
| Commandes | JetBrains Mono, sinon DejaVu Sans Mono | `fonts-jetbrains-mono` (facultatif) / `fonts-dejavu` |

Vérification : `fc-list | grep -E "Libre Baskerville|Inter-SemiBold"`.
Une police manquante provoque une erreur explicite à la compilation (`ciel-commun.sty`).

## Arborescence

```
commun/
  ciel-commun.sty     polices, \ifcorrige, macros d'adressage (chargé par les deux suivants)
  ciel-beamer.sty     thème Beamer « plat moderne » (cartes, tags, callouts, diapo finale inversée)
  ciel-tp.sty         TP compacts, impression noir et blanc
  icones/ciel-icones.tex  pictos TikZ : routeur, switch, pc, parefeu, serveur, nuage ; liens lien/trunk/serie
  verif_adressage.py  contrôle du plan, des configurations Cisco et des adresses citées dans les .tex
subnetting-vlsm/  ospf/  wireshark-transport/
  cours/  tp/  pdf/  packet-tracer/ | captures/
```

## Charte

* **Beamer** : vert `#1C322D`, crème `#F8F3EE`, or `#EBB552`, rose `#F1CDBE`, gris `#A1A1AA`.
  `\frametitle{Titre}` + `\framesubtitle{EYEBROW}` ; `carte`, `callout[or|rose|vert]`,
  `\reponse{…}` (visible en version prof), environnement `finale`.
* **TP** : N&B (aucune information portée par la seule couleur), 10 pt, marges 1,5 cm,
  en-tête d'une ligne ; chaque partie = configuration → vérification → test → **une** réflexion.
  `\trou{réponse}`, `\question[n]{énoncé}{réponse}`, `\config \verif \test`.
