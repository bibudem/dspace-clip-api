# dspace-clip-api / Dossier utils

Ce dossier contient des utilitaires pour tester les outils et l'API.

## Description des utilitaires

### Indexer des images

---

# Script d'Indexation pour CLIP

Le script `indexation_clip.py` permet d'indexer des images en utilisant le modèle CLIP. Il se connecte au serveur CLIP et traite les images d'un dossier spécifié, en ajoutant des métadonnées telles que le nom de collection et le nom de fichier. Une fois l'indexation terminée, il affiche le nombre total de fichiers indexés et le temps d'exécution.

Exemple de sortie :

```
Indexation terminée pour 100 fichiers.
Temps d'exécution : 12.3781156539917 secondes
```

Utilisation :

```bash
python indexation_clip.py
```

Lors de l'exécution, vous serez invité à entrer le chemin du dossier contenant les images à indexer, ainsi que le nom de la collection à laquelle elles appartiennent.

---


### Recherche du texte ou des images

---

# Script de Recherche avec CLIP

Le script `search_clip.py` permet d'effectuer une recherche sémantique d'images en utilisant le modèle CLIP. L'utilisateur peut saisir un mot-clé de recherche ou le chemin d'une image pour lancer la recherche. De plus, l'utilisateur peut spécifier une collection particulière pour la recherche ou laisser le champ vide pour effectuer une recherche globale.

Exemple de sortie :

```
python search_clip.py
Entrez le mot-clé de recherche ou le chemin de l'image pour la recherche: maison
Entrez le nom de la collection pour la recherche spécifique sinon Enter : test

Id : 7fade30656ad466f2d747506083a5fed
Nom de l'image : _madeleine_275_large.jpg
Collection : test
Score : 0.7509268522262573

Id : 6d8aa6daf1c4269871f556a826cbf0b7
Nom de l'image : _madeleine_652_large.jpg
Collection : test
Score : 0.7538365721702576

Id : 977fb35c1560868addfa1c970e444425
Nom de l'image : _madeleine_860_large.jpg
Collection : test
Score : 0.755467414855957

Id : cde16eca57c458318b105f693fb9e5ac
Nom de l'image : _madeleine_571_large.jpg
Collection : test
Score : 0.7641065120697021

Id : f2328df0394e6fd6d6a3f839d25b772d
Nom de l'image : _madeleine_664_large.jpg
Collection : test
Score : 0.7538365721702576
```

Utilisation :

```bash
python search_clip.py
```

Lors de l'exécution, vous serez invité à entrer un mot-clé de recherche ou le chemin d'une image. Vous pourrez également spécifier une collection pour une recherche plus spécifique.

---

