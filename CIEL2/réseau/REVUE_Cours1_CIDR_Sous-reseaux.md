# Revue du cours 1 : CIDR et découpage en sous-réseaux

Date : 14 octobre 2026.

Ce document transmet à un autre agent IA les conclusions d'une revue du cours. Il ne constitue pas une demande de publication ou de modification du dépôt distant.

## Documents examinés et limites

- `Cours1_CIDR_Sous-reseaux.tex` : lecture de la source disponible sur GitHub, branche `main`.
- `Cours1_CIDR_Sous-reseaux.pdf` : extraction du texte et contrôle des métadonnées, 10 pages.
- `Cours1_CIDR_Sous-reseaux_Corrige.pdf` : extraction du texte et contrôle des métadonnées, 9 pages.
- Recalcul indépendant avec le module Python `ipaddress` de plusieurs exemples, découpages et conversions en entiers.
- Consultation de références IETF et de sujets officiels sur Éduscol.

La mise en page des PDF n'a pas fait l'objet d'une inspection visuelle exhaustive. Les cinq sessions d'examen citées n'ont pas toutes été vérifiées intégralement. Au moment de la revue, le dossier de travail local ne contenait pas encore les documents fusionnés : l'analyse a utilisé une copie temporaire du dépôt. Avant toute correction, vérifier la version actuelle de la source.

## Conclusion générale

Le cours est globalement cohérent. La progression rappels IPv4 → CIDR → caractérisation des réseaux → découpage → VLSM → VLAN → exercices est pertinente. Aucune erreur arithmétique n'a été identifiée dans les exemples et corrigés examinés. Les plans VLSM proposés respectent l'alignement des blocs et ne se chevauchent pas.

Les principales critiques concernent les hypothèses implicites, les limites des méthodes et certaines affirmations trop générales.

## Corrections prioritaires

### 1. Exercice 10 : le maximum de 30 machines ne détermine pas uniquement /27

**Constat :** l'énoncé demande des sous-réseaux pouvant accueillir « au maximum 30 machines ». Le corrigé choisit `/27`, mais `/28` ou `/29` respectent également ce maximum. Le choix du plus grand bloc admissible est implicite.

**Proposition :** écrire « Choisir les plus grands sous-réseaux dont la capacité ne dépasse pas 30 adresses IPv4 utilisables, équipements réseau compris ». Si l'objectif est de satisfaire un besoin de 30 adresses, écrire plutôt « Chaque sous-réseau doit fournir au moins 30 adresses utilisables, en minimisant la taille du bloc ».

**Validation :** le nouvel énoncé doit déterminer `/27` sans hypothèse supplémentaire ; le corrigé doit employer la même interprétation du besoin.

### 2. Distinguer postes et total des adresses nécessaires

**Constat :** le cours rappelle correctement que la passerelle consomme une adresse, mais les expressions « machines », « postes » et « hôtes » peuvent laisser planer un doute sur son inclusion dans les besoins annoncés.

**Proposition :** préciser dans chaque exemple et exercice si les besoins comprennent la passerelle, les interfaces d'administration et les équipements fixes. Un `/27` fournit 30 adresses utilisables : avec une passerelle, il reste 29 adresses pour les autres équipements.

Dans l'exercice 10, une passerelle et quatre équipements fixes laissent 25 adresses DHCP par VLAN. Les plages DHCP du corrigé sont correctes selon cette convention.

**Validation :** toutes les capacités doivent être calculées avec une convention explicite et constante.

### 3. Compléter la méthode du pas pour les préfixes multiples de 8

**Constat :** la méthode demande de trouver l'octet du masque qui n'est ni 255 ni 0. Il n'existe pas pour `/8`, `/16` et `/24`, pourtant présents dans la table.

**Proposition :** ajouter un cas distinct : pour ces préfixes, conserver les octets réseau et mettre les octets hôte à zéro pour obtenir le réseau ; mettre les octets hôte à 255 pour la diffusion. Expliquer aussi les indications de pas 1 de la table : il s'agit de l'incrément entre réseaux dans le dernier octet réseau.

**Validation :** la méthode doit fonctionner explicitement pour un `/24` et un `/16`, en plus des exemples `/27` et `/20`.

### 4. Limiter la portée de la formule 2^h − 2

**Constat :** la formule du nombre d'hôtes est présentée comme générale, alors que la table contient `/31` et `/32`. La note sur `/31` est utile mais ne suffit pas à encadrer toutes les formulations générales du cours.

**Proposition :** présenter `2^h − 2` comme la formule des sous-réseaux IPv4 ordinaires traités ici, jusqu'à `/30`. Rappeler les exceptions : `/31` point à point fournit deux adresses d'extrémité ; `/32` désigne une adresse unique, notamment dans une route d'hôte.

**Source :** [RFC 3021, section 2.1](https://datatracker.ietf.org/doc/html/rfc3021#section-2.1).

**Validation :** éviter d'appliquer la soustraction de deux aux lignes `/31` et `/32`.

### 5. Le test IP ET masque ne garantit pas la communication

**Constat :** l'encadré de vérification dit qu'un poste peut joindre directement une autre machine « si et seulement si » les résultats du ET logique sont égaux. Cela exprime la décision de considérer une destination comme locale dans le modèle étudié, mais ne garantit pas une communication effective : VLAN, lien physique, filtrage et configuration du destinataire interviennent aussi.

**Proposition :** écrire « Dans le modèle étudié, le poste considère la destination comme appartenant à son sous-réseau si les deux résultats sont égaux. Une communication directe suppose également une connectivité de couche 2 et des configurations cohérentes ». Préciser que, pour une destination distante, le prochain saut dépend de la table de routage ; dans les exercices simples, il s'agit de la passerelle par défaut.

**Validation :** deux machines portant des adresses du même sous-réseau mais placées dans deux VLAN isolés ne doivent pas être présentées comme nécessairement joignables.

### 6. La fiche réflexe mélange découpage complet et VLSM

**Constat :** « le dernier bloc se termine à la diffusion du réseau d'origine » est vrai pour un découpage complet en blocs égaux. Ce n'est pas une exigence pour un plan VLSM laissant une plage libre, comme ceux du cours.

**Proposition :** réserver ce contrôle au découpage complet en sous-réseaux égaux. Pour le VLSM, contrôler l'alignement, l'inclusion dans le bloc initial, les capacités et l'absence de chevauchement. Identifier explicitement les plages restantes.

**Validation :** les exemples VLSM du cours doivent satisfaire la fiche réflexe sans devoir attribuer les plages libres.

## Références aux examens et conventions pédagogiques

### 7. Exercice 9 : préciser l'adaptation du plan officiel de 2025

**Constat confirmé :** le sujet officiel 2025 impose le bloc `192.168.7.0/24` divisé en huit sous-réseaux et la dernière adresse utilisable comme passerelle (Q28–Q29). Il configure aussi l'administration du switch dans le VLAN 160 avec `192.168.7.161/27` (Q31), donc dans `192.168.7.160/27`.

Le cours place l'Administration dans `192.168.7.128/27` selon son propre énoncé simplifié. Le calcul est cohérent avec cet énoncé, mais ne reproduit pas l'affectation officielle.

**Proposition :** indiquer expressément « Adaptation : l'ordre et l'affectation des VLAN sont simplifiés pour cet exercice », ou rétablir le plan officiel après lecture de la figure et du document réponses. Ne pas changer uniquement une ligne sans vérifier l'ensemble des affectations.

**Source :** [Sujet complet E4 CIEL 2025, Q28–Q31](https://sti.eduscol.education.fr/sites/eduscol.education.fr.sti/files/concours-examens/18615/18615-25cielaecri-sujet-complet-ir.pdf).

### 8. Éviter les affirmations absolues sur les sujets de BTS

**Formulations à vérifier :**

- « seule notion présente dans tous les sujets d'E4 » de 2022 à 2026 ;
- « dans les sujets de BTS, une liaison point à point est en /30 » ;
- « interdit le jour de l'examen », à propos de l'utilisation de Python.

**Proposition :** limiter les affirmations au corpus précisément étudié, avec session, territoire, option et lien vers le sujet. Pour les exercices, annoncer simplement la convention `/30` retenue. Pour Python, distinguer le calcul autonome d'entraînement des outils effectivement autorisés par les consignes de l'épreuve.

L'affirmation « seule notion » nécessite une comparaison de toutes les autres notions des cinq sujets ; elle n'a pas été établie par cette revue.

**Vérification partielle :** le sujet officiel 2024 confirme bien le découpage de `172.20.0.0/16` pour créer dix sous-réseaux (Q22–Q23).

**Source :** [Sujet E4 SN 2024, domaine professionnel](https://sti.eduscol.education.fr/sites/eduscol.education.fr.sti/files/concours-examens/17194/17194-bts-sn-2024-e4-metropole-sujet-documents-reponses-professionnel-snir.pdf).

### 9. Présenter « un VLAN = un sous-réseau IP » comme une convention

**Constat :** cette phrase est adaptée aux architectures des exercices mais ne constitue pas une identité technique universelle.

**Proposition :** « Dans les architectures étudiées, on associe un sous-réseau IP à chaque VLAN ». Conserver l'explication du routage inter-VLAN dans ce cadre.

## Précisions secondaires utiles

- Dans le tableau des adresses privées, « il faut un NAT pour sortir » est trop général. Préciser le cas courant d'un accès IPv4 direct à Internet avec traduction vers une adresse publique ; un accès par proxy constitue notamment un autre scénario.
- Pour APIPA, indiquer qu'il s'agit d'adresses IPv4 de portée locale au lien. Si la plage d'auto-attribution est détaillée, elle va de `169.254.1.0` à `169.254.254.255`, les premiers et derniers 256 éléments du `/16` étant réservés. Source : [RFC 3927, section 2.1](https://www.rfc-editor.org/rfc/rfc3927.html#section-2.1).
- Dans la méthode VLSM, préciser que la garantie d'alignement suppose un départ sur une adresse réseau correctement alignée et des allocations par tailles décroissantes. Les exemples actuels satisfont ces conditions.
- En cas de passage d'un VLAN de `/27` à `/26`, rappeler que les blocs voisins peuvent devoir être déplacés pour éviter un chevauchement. La réponse de l'exercice 10 évoque déjà une reconstruction du plan en VLSM ; une phrase explicite rendrait la conséquence plus claire.

## Éléments vérifiés à préserver

- `192.168.1.100/27` : réseau `.96`, diffusion `.127`, 30 adresses utilisables.
- `172.16.45.200/20` : réseau `172.16.32.0`, diffusion `172.16.47.255`, 4 094 adresses utilisables.
- Les trois lignes du corrigé de l'exercice 3 sont correctes.
- Les plans VLSM des exemples et de l'exercice 5 sont cohérents ; la plage libre de l'exercice 5 est `192.168.50.248/29`.
- Les découpages des exercices 6 à 10 sont arithmétiquement corrects selon leurs énoncés et les hypothèses indiquées ci-dessus.
- Les conversions `10.0.1.5 → 167772421`, `192.168.1.10 → 3232235786` et `2886729738 → 172.16.0.10` sont correctes.
- L'extraction de texte confirme des tableaux à compléter dans le PDF élève et des réponses présentes dans le PDF corrigé.

## Consignes de reprise pour l'agent IA

1. Lire la source actuelle et distinguer erreurs, ambiguïtés et simplifications pédagogiques.
2. Corriger en priorité les six points techniques, en conservant le niveau BTS CIEL et la progression.
3. Vérifier les sujets officiels avant de modifier les références aux examens. Ne pas présenter les références non vérifiées comme confirmées.
4. Si une modification du cours est demandée, garder une source LaTeX commune aux versions élève et enseignant.
5. Après modification, recalculer les exemples concernés, compiler les deux versions et inspecter visuellement les tableaux, zones de réponse et sauts de page.
6. Ne publier sur GitHub que si cette action est autorisée dans la session de travail de l'agent.

## Suivi des corrections — 14 octobre 2026

Les corrections techniques et pédagogiques proposées ont été appliquées à la source : capacité maximale explicite, convention de comptage des adresses, cas des préfixes multiples de 8, exceptions /31 et /32, décision de destination locale, contrôles VLSM et adaptation explicite du sujet 2025. Les formulations absolues sur les examens ont été retirées ou remplacées par des conventions propres aux exercices. Les précisions sur NAT, APIPA et la réallocation lors du passage en /26 ont également été ajoutées.

Les deux PDF ont été régénérés avec pdflatex, sans avertissement ni débordement signalé. Un contrôle visuel des pages a été réalisé et la pagination des exercices ajustée. Les références aux cinq sessions restent à vérifier exhaustivement ; aucune nouvelle validation de ce corpus n’est revendiquée. Les modifications sont locales et ne sont pas publiées sur GitHub.
