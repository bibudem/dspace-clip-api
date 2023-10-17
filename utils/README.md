# dspace-clip-api / Dossier utils

Ce dossier contient des outils et des exemples pour travailler avec le se serveur ou l'API.

Pour utiliser les scripts Python, vous devez installer le module clip-client de Jina:

```sh
pip install clip-client
```

## Indexer des images

Le script `indexation_clip.py` permet d'*indexer* des images, c'est-à-dire d'en extraire les *features* selon le modèle CLIP et d'indexer le vecteur de *features* dans un moteur de recherche vectoriel (*Ann Lite*).

Pour l'utiliser, assurez-vous d'avoir un [serveur](../server/README.md) démarré et vérifiez que le port et le protocole utilisés correspondant à ce qu'on retrouve dans le script `indexation_clip.py`.

La ligne de commande est la suivante:

```sh
python indexation_clip.py [dossier d'images] optionnel: non d'une collection]
```

Les fichiers d'images qui sont dans le dossier spécifié seront indexés sur le serveur.

Optionnellement, si vous spécifiez une collection, celle-ci sera ajoutée comme métadonnée aux images et vous pourrez filtrer vos recherches par collection.

Vous pouvez par exemple exécuter:

```sh
python indexation_clip.py img test
```

Ceci indexera les 10 images du dossier `img` dans une collection nommée `test`.

Le résultat devrait ressembler à ceci:

```sh
  ⬇ Progress ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1/1 • unknown • 0:00:00 • 2.4 kB
  ⬇ Progress ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1/1 • unknown • 0:00:00 • 2.4 kB
  ⬇ Progress ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1/1 • unknown • 0:00:00 • 2.4 kB
  ⬇ Progress ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1/1 • unknown • 0:00:00 • 2.4 kB
  ⬇ Progress ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1/1 • unknown • 0:00:00 • 2.4 kB
  ⬇ Progress ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1/1 • unknown • 0:00:00 • 2.4 kB
  ⬇ Progress ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1/1 • unknown • 0:00:00 • 2.4 kB
  ⬇ Progress ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1/1 • unknown • 0:00:00 • 2.4 kB
  ⬇ Progress ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1/1 • unknown • 0:00:00 • 2.4 kB
  ⬇ Progress ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1/1 • unknown • 0:00:00 • 2.4 kB
Indexation terminée pour 10 fichiers.
Temps d'exécution : 36.17978024482727 secondes
```

## Rechercher des images

Le script `search_clip.py` permet d'effectuer une recherche dans les images indexées.

Pour l'utiliser, assurez-vous d'avoir un [serveur](../server/README.md) démarré et vérifiez que le port et le protocole utilisés correspondant à ce qu'on retrouve dans le script `search_clip.py`.

La ligne de commande est la suivante:

```sh
python search_clip.py ["Texte ou chemin à rechercher"] [collection]
```

Vous pouvez soit entrer du texte qui décrit l'image à chercher ou encore entrer le chemin d'une image et des images similaires seront retournées.

Par exemple, pour rechercher une image de chute d'eau dans la collection de test, vous pouvez entrer la commande suivante:

```sh
python search_clip.py "chute d'eau" test
```

Le résultat devrait être similaire à ceci:

```sh
Id : f4f9bd405e7266522e6466a1884c6bda
File name : IMG_0963.jpeg
Collection : test
Score : 0.7271528244018555
Id : 968b5ab4a0934430354d6494b3c4d6ce
File name : IMG_1106.jpeg
Collection : test
Score : 0.7361363172531128
Id : 87b76243572f2b133d6cccf28f2562aa
File name : IMG_1116.jpeg
Collection : test
Score : 0.7632312774658203
Id : ba1e9cb5512f6eea1ae1adde8a6e34ec
File name : IMG_0734.jpeg
Collection : test
Score : 0.7691144943237305
Id : e525d955b4281e37da399284828f4f8d
File name : IMG_2014.jpeg
Collection : test
Score : 0.7820137739181519
```
