# TP 3 — fichiers Packet Tracer

Le format `.pkt` est binaire et chiffré : il ne peut pas être généré par script.
Ce dossier contient donc la **configuration complète de chaque équipement**
(`R1.txt`, `R2.txt`, `FW.txt`, `SW1.txt`, `SW2.txt`), source unique reprise
dans l'annexe du corrigé PDF et contrôlée par `make verif`.

## Produire le corrigé `.pkt` (≈ 10 min)
1. Placer : 3 routeurs **2911** (R1, R2, FW), 2 switchs **2960-24TT** (SW1, SW2), 4 PC.
2. Câbler selon le tableau du TP (droit routeur–switch et PC–switch ; croisé
   switch–switch et routeur–routeur).
3. Pour chaque équipement : onglet *CLI*, coller le contenu du `.txt`
   (la dernière ligne `copy running-config startup-config` demande une validation : Entrée).
4. PC : PC-ADM en statique (192.168.10.129/26, passerelle 192.168.10.190) ;
   PC-P1, PC-P2, PC-I1 en DHCP.
5. Enregistrer sous `tp03-corrige.pkt` dans ce dossier.

## Fichier de départ élève (optionnel)
Même topologie câblée, sans aucune configuration : `tp03-depart.pkt`.
Le TP est conçu pour que l'élève construise la topologie lui-même (partie 1).
