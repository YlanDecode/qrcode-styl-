# Passation détaillée — QR code — Génération locale en lot et contrôle des sorties

<!-- passation-generated-v1; source=dossier.json; sha256=520ea4104313f37b3989a39075d655002b0d0c996216caf7c7fca7f5d44f0a5c -->

[Schéma HTML et lecture navigable](architecture.html) · [Index local](README.md) · [Historique Git complet](HISTORIQUE_GIT.md)

État documentaire : 2026-10-29. Référence : branche `master`, commit `59e1945`.

## Sommaire

- Mission, périmètre et lecture
- Stack et rôle des technologies
- Carte des composants
- Responsabilités et localisation du code
- Échanges et frontières
- Déroulement des parcours
- Données, portée et cycle de vie
- Contrats et interfaces
- Configuration et prérequis
- Démarrage et exploitation
- Diagnostic et reprise sur erreur
- Vérification fonctionnelle
- Interventions et chronologie
- Ce qui est présent et niveau de preuve
- Points forts et raisons des choix
- Travaux restants et critères d'acceptation
- Guide de travail pour l'assistant IA
- Sources et documents complémentaires
- Maintenir cette passation

## Mission, périmètre et lecture

Cet utilitaire Python lit urls.txt et produit un PNG par entrée dans qrcode_image_list. Il n'appelle pas les URLs, n'a ni API, ni base de données, ni traitement asynchrone. Le résultat attendu est un code réellement décodable avec le contenu exact de l'entrée.

La reprise tient dans un petit parcours mais plusieurs détails ont des effets réels : chemins relatifs au répertoire courant, lignes filtrées, nom de sortie dérivé du domaine/chemin et écrasement possible. Deux URLs qui diffèrent seulement par query string obtiennent le même nom de fichier.

Le style arrondi/dégradé dépend des imports de qrcode/Pillow ; sinon le script utilise noir/blanc. Cette différence peut modifier le rendu sans être une erreur. Un PNG enregistré ne prouve ni lecture par un téléphone ni qualité d'impression.

### Frontière du dépôt

- Local : main.py, parsing des entrées, génération et sauvegarde des PNG.
- Données d'exécution : urls.txt, environnement virtuel et images générées non suivis, sans contenu repris dans la passation.
- Hors script : navigateur/lecteur QR et destination encodée ; aucune requête réseau n'est effectuée par l'utilitaire.

Un fichier ou un commit prouve une implémentation/modification, pas un déploiement. Les validations historiques restent datées ; les contrôles de reprise proposés ne sont pas déclarés exécutés. Les systèmes externes du schéma sont des dépendances à obtenir, pas du code contenu dans ce dépôt.

## Stack et rôle des technologies

| Couche   | Version / référence                   | Rôle concret                                            | Source                                         |
| -------- | ------------------------------------- | ------------------------------------------------------- | ---------------------------------------------- |
| Runtime  | Python / pathlib / urllib.parse       | Fichiers et slug de nom de sortie.                      | main.py                                        |
| Encodage | qrcode                                | ERROR_CORRECT_H, box_size 14, border 2 et fit=True.     | main.py                                        |
| Image    | Pillow / StyledPilImage si importable | Modules arrondis et masque radial, fallback noir/blanc. | main.py                                        |
| Contrôle | Lecteur QR externe                    | Décodage réel de l'image et comparaison de la chaîne.   | Recette proposée, pas test automatique présent |

## Données, portée et cycle de vie

| Objet / stockage | Source de vérité et contenu | Portée / lifecycle                      | Point de contrôle                                       |
| ---------------- | --------------------------- | --------------------------------------- | ------------------------------------------------------- |
| Entrées          | urls.txt UTF-8              | Filtrage strip/vides/commentaires       | Chaînes complètes encodées, aucun accès HTTP.           |
| Slug             | Domaine et chemin           | Query/fragment ignorés                  | Collisions connues à traiter si besoin.                 |
| PNG              | Dossier de sortie           | État de fichier, pas preuve de décodage | Peut être remplacé par l'entrée suivante.               |
| Style            | Imports disponibles         | Arrondi/dégradé ou noir/blanc           | Versions de dépendances non verrouillées à établir.     |
| Console          | Print de l'URL et chemin    | Peut contenir paramètres de l'entrée    | Ne pas partager une sortie réelle avec données privées. |

## Contrats et interfaces

| Interface          | Entrée et identité              | Sortie / effet                | Vérification et source                                                |
| ------------------ | ------------------------------- | ----------------------------- | --------------------------------------------------------------------- |
| load_urls(Path)    | Fichier UTF-8                   | Liste non vide ou exception   | main.py : ne valide pas schéma URL complet.                           |
| slug_from_url(str) | Chaîne                          | Nom domaine/path ou qrcode    | Identité de fichier différente de l'identité complète d'URL.          |
| make_qr(str, Path) | Contenu et dossier existant     | PNG et Path                   | Peut écraser un nom déjà présent.                                     |
| CLI                | python main.py dans cwd attendu | Print par succès ou exception | Pas de paramètres de batch, manifeste ou reprise par entrée présents. |

## Configuration et prérequis

| Paramètre / dépendance | Utilité et chargement | Effet d'un mauvais réglage                      | Contrôle de reprise                           |
| ---------------------- | --------------------- | ----------------------------------------------- | --------------------------------------------- |
| Python/qrcode/Pillow   | Environnement isolé   | Import ou style différent                       | Qualifier/pinner si besoin reproductible.     |
| Répertoire courant     | Chemins relatifs      | Entrée introuvable ou sortie au mauvais endroit | Lancer depuis la racine identifiée.           |
| Paramètres QR          | Constantes main.py    | Taille/contraste/bordure non adaptés au support | Recette avec le lecteur final.                |
| Nommage                | slug_from_url         | Écrasement de query variants                    | Prévoir stratégie de nom unique avant volume. |

## Diagnostic et reprise sur erreur

| Symptôme                 | Étape et hypothèses         | Contrôle discriminant                                   | Reprise et preuve attendue                          |
| ------------------------ | --------------------------- | ------------------------------------------------------- | --------------------------------------------------- |
| Fichier introuvable/vide | Cwd ou entrée               | Lire la présence et le message sans publier les données | Préparer une liste autorisée non vide.              |
| Moins de PNG que d'URLs  | Collision de slug           | Comparer domaine/path des entrées                       | Noms uniques si évolution décidée.                  |
| Lot partiel              | Exception dans la boucle    | Identifier dernière entrée réussie et première fautive  | Reprise ciblée proposée ; pas mécanisme déjà livré. |
| Style différent          | Imports spécialisés absents | Vérifier versions et fallback                           | Décoder, puis qualifier le rendu si nécessaire.     |
| QR illisible imprimé     | Taille/contraste/bordure    | Tester le support final                                 | Adapter les paramètres sur preuve de décodage.      |

## Ce qui est présent et niveau de preuve

| Capacité          | Preuve disponible              | Limite de la preuve                              | Recette à conserver                    |
| ----------------- | ------------------------------ | ------------------------------------------------ | -------------------------------------- |
| Génération PNG    | main.py présent                | Pas manifeste ni traitement d'erreur par entrée  | Petit lot et décodage.                 |
| Style/fallback    | Branches d'import              | Rendu varie selon environnement                  | Deux modes décodés.                    |
| Industrialisation | Propositions de reprise        | Validation URL/noms uniques/manifeste non livrés | À construire seulement si besoin réel. |
| Usage imprimé     | Non attesté par sauvegarde PNG | Qualité finale à tester                          | Support final et contenu comparé.      |

## Travaux restants et critères d'acceptation

| Priorité               | Constat et source                           | Intervention recommandée                   | Critère d'acceptation                      |
| ---------------------- | ------------------------------------------- | ------------------------------------------ | ------------------------------------------ |
| P1 si diffusion en lot | Collisions domaine/path                     | Nom unique et détection d'écrasement       | Une sortie par contenu distinct.           |
| P1 qualité             | Décodage non automatique                    | Ajouter une recette de lecture du support  | Valeur décodée exacte.                     |
| P2 industrialisation   | Erreur interrompt le lot                    | Validation/rapport/manifeste si besoin     | Erreurs par entrée sans perdre les autres. |
| P2 reproductibilité    | Dépendances non établies comme verrouillées | Figer l'environnement si rendu contractuel | Même style/résultat sur cible de reprise.  |

## Carte des composants

Ouvrir [architecture.html](architecture.html) pour le schéma SVG annoté et son zoom. Les responsabilités et échanges sont aussi décrits intégralement ci-dessous.

## Responsabilités et localisation du code

### Opérateur local

Prépare une liste autorisée puis lance depuis la racine du projet. Le script ne possède pas d'arguments CLI pour sélectionner automatiquement un autre fichier/répertoire.

- **Entrées :** Liste de chaînes et environnement Python.
- **Sorties / effets :** Exécution et inspection des résultats.
- **Erreur / frontière :** Ne pas recopier une liste réelle comportant paramètres privés dans la documentation.
- **Sources :** [main.py](../../main.py)

### urls.txt

Source locale UTF-8 ; lignes vides et commentaires commençant par # sont ignorés après strip. Le script encode les chaînes sans validation complète de schéma URL.

- **Entrées :** Texte saisi par l'opérateur.
- **Sorties / effets :** Liste ordonnée des entrées retenues.
- **Erreur / frontière :** Fichier absent ou liste vide provoquent une erreur avant la boucle de génération.
- **Sources :** [main.py](../../main.py)

### load_urls / slug_from_url

Charge les entrées puis construit le nom depuis netloc sans www et path avec slash remplacé. Query et fragment ne participent pas au slug.

- **Entrées :** Ligne retenue et chemin d'entrée.
- **Sorties / effets :** Chaîne à encoder et basename.
- **Erreur / frontière :** Collision de nom possible ; contenu encodé différent peut remplacer la même image.
- **Sources :** [main.py](../../main.py)

### make_qr

Ajoute la chaîne, adapte la version avec fit et rend le style disponible. La correction H ne remplace pas le contrôle de contraste, taille et bordure dans l'usage final.

- **Entrées :** Chaîne et output_dir.
- **Sorties / effets :** Image PNG et chemin retourné.
- **Erreur / frontière :** Aucune isolation d'erreur par entrée dans main : une exception peut interrompre le reste du lot.
- **Sources :** [main.py](../../main.py)

### qrcode_image_list

Dossier créé si absent puis fichiers sauvegardés. L'état peut être partiel après erreur et une sortie de même nom est remplacée sans manifeste de collision.

- **Entrées :** Image et slug.
- **Sorties / effets :** Artefact à décoder/imprimer.
- **Erreur / frontière :** Nombre de lignes utiles et nombre de PNG distincts peuvent différer.
- **Sources :** [main.py](../../main.py)

### Lecteur / support final

Vérifie le code au format réellement utilisé. La valeur décodée doit correspondre exactement à l'entrée, paramètres inclus, même si ces paramètres ont été ignorés pour le nom de fichier.

- **Entrées :** PNG ou impression.
- **Sorties / effets :** Chaîne décodée et preuve de lecture.
- **Erreur / frontière :** Un scan réussi sur grand écran ne garantit pas la lisibilité d'une petite impression.
- **Sources :** [docs/passation/README.md](../../docs/passation/README.md)

## Échanges et frontières

| Relation              | Déclenchement / contenu  | Mode    | Contrat et frontière                                        |
| --------------------- | ------------------------ | ------- | ----------------------------------------------------------- |
| 01 — operator → input | Préparer la liste        | storage | Une chaîne par ligne, pas de secret dans l'exemple partagé. |
| 02 — input → loader   | Lecture et filtre UTF-8  | sync    | Absence/vide explicitement rejetés.                         |
| 03 — loader → encoder | Chaîne exacte et slug    | sync    | Contenu complet mais nom sans query/fragment.               |
| 04 — encoder → output | Sauvegarde PNG           | storage | Écrasement possible et pas de transaction globale de lot.   |
| 05 — output → reader  | Lecture du vrai artefact | sync    | Décoder puis comparer, pas simplement compter les fichiers. |

## Déroulement des parcours

### Générer un lot local

**Déclencheur :** python main.py depuis la bonne racine.

1. **Dossier** — Créer/repérer qrcode_image_list et charger urls.txt. Résultat / contrôle : Les chemins sont relatifs au cwd, pas au dossier du script par magie.
2. **Filtre** — Retenir les lignes utiles et refuser la liste vide. Résultat / contrôle : Commentaires ignorés ; pas de validation réseau.
3. **Encodage** — Générer chaque matrice avec fit et style disponible. Résultat / contrôle : Fallback de style possible si imports spécialisés indisponibles.
4. **Écriture** — Enregistrer le PNG nommé par slug. Résultat / contrôle : Vérifier collisions et nombre de fichiers.
5. **Lecture** — Scanner et comparer à l'entrée. Résultat / contrôle : Les paramètres de query doivent être conservés dans le contenu.

**Succès métier :** Chaque entrée attendue possède une sortie distincte lisible et correcte.

**Rejeu / incident :** Un nouveau lancement peut écraser les mêmes noms ; conserver les artefacts utiles et définir une stratégie si industrialisation.

### Diagnostiquer une sortie absente ou incorrecte

**Déclencheur :** Fichier manquant, lot interrompu ou décodage incohérent.

1. **Entrée** — Vérifier cwd, encodage et lignes retenues. Résultat / contrôle : Pas de diagnostic à partir d'une liste client publiée.
2. **Nom** — Comparer domaine/path et collisions query/fragment. Résultat / contrôle : Deux contenus peuvent viser un même PNG.
3. **Runtime** — Vérifier qrcode/Pillow et mode de style. Résultat / contrôle : Une différence visuelle peut être un fallback, pas mauvais contenu.
4. **Support** — Décoder le PNG puis le support imprimé. Résultat / contrôle : Contraste/bordure/taille qualifiés sur usage réel.

**Succès métier :** Cause localisée et contenu vérifié avant diffusion.

**Rejeu / incident :** Ne pas régénérer le lot sur les sorties utiles sans comprendre l'écrasement ; pas de transaction de rollback existante.

## Démarrage et exploitation

### Préparer et générer

**Préconditions :** Environnement isolé et urls.txt synthétique dans la racine.

```text
python -m pip install "qrcode[pil]"
python main.py
```

**Attendu :** PNG générés et compte de sorties compris.

**Effets et limites :** Écrit/remplace des PNG et affiche les entrées ; ne pas utiliser une liste privée dans une capture.

### Contrôle d'usage

**Préconditions :** Lecteur QR et support d'impression cible.

**Attendu :** Contenu exact et lisibilité à la taille réelle.

**Effets et limites :** Le script lui-même ne visite pas les URLs ; le lecteur peut ensuite le faire.

## Vérification fonctionnelle

1. Fichier absent, vide, commentaires et Unicode.
2. URL avec query et deux variantes partageant domaine/path.
3. Contenu décodé identique, sans visiter d'URL privée.
4. Mode stylé et fallback noir/blanc.
5. Erreur d'une entrée avec état des sorties précédentes.
6. Lecture sur la taille d'impression visée.

## Interventions et chronologie

L'annexe recense 1 commits signés par Ylan/YlanDecode dans les ancêtres du commit de référence. Elle est exhaustive pour ce filtre et cette révision, pas pour les autres auteurs ni les branches non intégrées. Les merges sont des intégrations collectives, pas une attribution exclusive du code.

| Date       | Référence        | Auteur / statut     | Intervention                                   | Portée de la preuve                                                 |
| ---------- | ---------------- | ------------------- | ---------------------------------------------- | ------------------------------------------------------------------- |
| 2026-04-10 | 59e1945          | YlanDecode          | Générateur en lot.                             | Un commit de création visible ; aucune recette de campagne inférée. |
| État local | document / local | Données non suivies | Liste d'URL, environnement et images générées. | Artefacts d'exécution, pas sources à publier.                       |

[Annexe Git complète](HISTORIQUE_GIT.md).

## Points forts et raisons des choix

- Un script compact et sans réseau est facile à comprendre et à exécuter localement.
- Le fallback permet de générer même sans les composants de style spécialisés.
- fit adapte la matrice au contenu au lieu d'imposer une taille logique fixe.
- Le chemin retourné et le print donnent une corrélation simple entre entrée et fichier.

## Guide de travail pour l'assistant IA

1. Ne pas lire/copier la liste d'URL réelle pour écrire un exemple.
2. Un PNG sauvé ne prouve pas un QR correct : décoder.
3. Ne pas confondre slug sans query et contenu complet.
4. Toute reprise doit tenir compte des sorties déjà écrites et écrasables.
5. Ne pas ajouter API/base/queue à cet utilitaire sans besoin explicite.

## Sources et documents complémentaires

- [main.py](../../main.py) — Parcours entier, paramètres, nommage et erreurs.
- [README.md](../../README.md) — Entrée locale de reprise et rôle de l'outil.

### Synthèses locales

- [CONTEXTE_DEPOT.md](CONTEXTE_DEPOT.md)
- [DESIGN.md](DESIGN.md)
- [README.md](README.md)

## Maintenir cette passation

Modifier dossier.json pour faire évoluer le fond de cette passation, puis générer les fichiers dérivés avec l'outil local et Python 3.10 ou plus récent. Actualiser les références et les preuves lorsqu'un contrat change. Le snapshot historique est figé à la révision annoncée ; --refresh-history le reconstruit depuis cette révision. --check contrôle sans écriture. Aucune clé ni donnée métier privée n'est nécessaire au rendu.

```text
python -B docs/passation/generer_passation.py
python -B docs/passation/generer_passation.py --check
```
