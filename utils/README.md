# dspace-clip-api / Dossier utils

Ce dossier contient des outils et des exemples pour travailler avec le serveur ou l'API.

Pour utiliser les scripts Python, vous devez installer le module clip-client de Jina:

```sh
pip install clip-client
```

## Indexer des images

Le script `indexation_clip.py` permet d'*indexer* des images, c'est-à-dire d'en extraire les *features* selon le modèle CLIP et d'indexer le vecteur de *features* dans un moteur de recherche vectoriel (*Ann Lite*).

Pour l'utiliser, assurez-vous d'avoir un [serveur](../server/README.md) démarré et vérifiez que le port et le protocole utilisés correspondant à ce qu'on retrouve dans le script `indexation_clip.py`.

Pour démarrer une indexation, la ligne de commande est la suivante:

```sh
python indexation_clip.py --folder [dossier d'images] --collection [nom de la collection]
```

Les fichiers d'images qui sont dans le dossier spécifié seront indexés sur le serveur.

Optionnellement, si vous spécifiez une collection, celle-ci sera ajoutée comme métadonnée aux images et vous pourrez filtrer vos recherches par collection.

Vous pouvez par exemple exécuter:

```sh
python indexation_clip.py --folder img  --collection test
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
Temps d'exécution : 7.418843030929565 secondes
```

## Rechercher des images

Le script `search_clip.py` permet d'effectuer une recherche dans les images indexées.

Pour l'utiliser, assurez-vous d'avoir un [serveur](../server/README.md) démarré et vérifiez que le port et le protocole utilisés correspondant à ce qu'on retrouve dans le script `search_clip.py`.

La ligne de commande est la suivante:

```sh
python search_clip.py --find ["Texte ou chemin à rechercher"] --collection [collection]
```

Vous pouvez soit entrer du texte qui décrit l'image à chercher ou encore entrer le chemin d'une image et des images similaires seront retournées.

Par exemple, pour rechercher une image de chute d'eau dans la collection de test, vous pouvez entrer la commande suivante:

```sh
python search_clip.py --find "chute d'eau"  --collection test
```

Le résultat devrait être similaire à ceci:

```sh
Recherche par mot-clé ou par le chemin de l'image
Id : b9f122135b04eda343ef0fac9e19cc67
File name : IMG_0963.jpeg
Collection : test
Score : 0.7271525263786316
Id : 72b5c17ebf4bca5d6f15e9c2c1fdff29
File name : IMG_1106.jpeg
Collection : test
Score : 0.7361361980438232
Id : b84b4bc71b936dc2213dddf841e94baf
File name : IMG_1116.jpeg
Collection : test
Score : 0.7632315754890442
```

# Application Web avec FastAPI et Clip Client

## Démarrage

1. Assurez-vous d'avoir FastAPI, Clip Client et les autres dépendances installées. Vous pouvez les installer en exécutant la commande suivante :

```bash
pip install fastapi
```

```bash
pip install "uvicorn[standard]"
```

2. Lancez le serveur FastAPI en exécutant le fichier `web.py` :

```bash
uvicorn web:app --reload
```

3. Rendez-vous sur [http://localhost:8000](http://localhost:8000) dans votre navigateur pour accéder à l'application.

## Fonctionnement du Fichier `web.py`

- Le fichier `web.py` utilise FastAPI pour créer une application Web.
- Il définit différentes routes pour gérer les requêtes et les réponses.
- Il utilise également le client Clip pour effectuer des recherches et récupérer les résultats.
- Le fichier contient des fonctions utilitaires pour traiter les données du formulaire et formater les résultats.

### Routes Principales

1. **Page d'Accueil**

   - Route : `/`
   - Méthode : GET
   - Affiche la page d'accueil avec un formulaire de recherche.

2. **Recherche au Format JSON ou HTML**

   - Route : `/search`
   - Méthode : GET
   - Accepte une requête GET avec le mot-clé et format, ensuite renvoie les résultats dans le format choisi.

### Fonctions Utilitaires

- `get_response_data(results)`: Extrait les données de réponse à partir des résultats de la recherche.
