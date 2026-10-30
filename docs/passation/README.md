# Passation — Générateur QR code en lot

> [Contexte du dépôt et guide pour l'assistant IA](CONTEXTE_DEPOT.md).

**Lecture approfondie : [dossier technique complet](PASSATION_DETAILLEE.md) · [schéma HTML interactif et expliqué](architecture.html) · [chronologie Git complète](HISTORIQUE_GIT.md).**

État : 29 octobre 2026. Branche `master`, HEAD `59e1945` du 10 avril 2026, YlanDecode. `.venv/`, liste d'URL et images générées sont non suivies et ne sont pas reprises ici.

## Mission, stack et architecture

Utilitaire Python autonome, sans API ni base : `urls.txt` → `load_urls()` → `make_qr()` → PNG dans `qrcode_image_list/`. Dépendance `qrcode` avec Pillow ; style arrondi/dégradé si disponible, repli noir/blanc sinon. L'utilisateur lance `python main.py` depuis la racine après installation dans un environnement isolé.

Le script ignore lignes vides/commentaires et refuse liste absente/vide. Les noms d'image proviennent du domaine et chemin URL. **Les query strings ne participent pas au nom** : deux URL de même domaine/chemin peuvent écraser la même sortie. Les chemins doivent aussi être compatibles avec le système de fichiers cible.

## Chronologie et état

Un commit personnel de création est visible ; aucune campagne de test ni déploiement n'est attestée. Les sorties sont des artefacts, pas de nouveaux composants de source.

## Suite et reprise

Tester la lecture par un vrai lecteur QR, contrastes et bordure sur la taille d'impression cible. Si l'outil est industrialisé, ajouter validation URL, stratégie de noms uniques, gestion d'erreur par entrée et manifeste de génération. Ce sont des propositions, pas des fonctions présentes.

## Assistant IA

Ne pas recopier la liste d'URL réelle dans la passation. Ne pas conclure qu'un QR est lisible parce qu'un PNG a été enregistré ; vérifier le contenu décodé et l'absence d'écrasement entre entrées.
