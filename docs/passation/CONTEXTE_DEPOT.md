# Contexte du dépôt — Utilitaire QR code

Ce projet est un script Python local sans serveur ni base. Il lit une liste d'URL et produit des PNG avec `qrcode`/Pillow ; les styles optionnels ont un fallback noir/blanc. [La passation](README.md) couvre architecture, stack, chronologie et améliorations proposées.

## Source et exploitation

[main.py](../../main.py) contient chargement, calcul de nom et génération. Exécuter depuis la racine avec un environnement isolé et une liste de recette. Les entrées réelles et images produites ne sont pas nécessaires à la compréhension du code et ne sont pas reproduites dans la documentation.

## État

HEAD `59e1945`, 10 avril 2026, commit YlanDecode de création. Il n'existe pas de preuve d'une campagne de tests complète. Les noms dérivent du domaine et chemin, sans query string : plusieurs URL peuvent écrire le même PNG.

## Assistant IA

Avant extension, tester l'unicité des fichiers, les caractères de chemins et la lecture d'un QR rendu/imprimé. Un PNG créé n'est pas la preuve du contenu décodé correct. Conserver la distinction entre fonctionnalités présentes et propositions : validation des URL, stratégie de nom unique et traitement d'erreur par entrée restent à développer si le besoin est retenu.
