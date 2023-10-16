import os
from clip_client import Client
from docarray import Document

# Créez un objet Client en spécifiant l'URL du serveur CLIP
client = Client('grpc://127.0.0.1:51000')

def search_score(keyword, collection):
    # Effectue la recherche en utilisant le mot-clé saisi
    filterAdd = {"collection": {"$eq": collection}}
    search_result = client.search([keyword], parameters={"filter": filterAdd},limit=5)
    if(len(search_result[0].matches)==0):
       print(f"Aucun résultat trouvé dans la collection '{collection}'.")
       print("Résultas d'une recherche globale...")
       search_result = client.search([keyword],limit=5)
    return search_result[0].matches

if __name__ == '__main__':
    option = input("Entrez le mot-clé de recherche ou le chemin de l'image pour la recherche: ")

    # Demander à l'utilisateur de spécifier une collection
    collection = input("Entrez le nom de la collection pour la recherche spécifique sinon Enter : ")

    results = search_score(option, collection)

    # Ensemble pour éviter les doublons
    seen_images = set()

    # Affiche le score de chaque image
    for result in results:
        cosine_value = result.scores.get('cosine').value
        image_name = os.path.basename(result.uri)
        # Vérifie si l'image n'a pas déjà été affichée et si le score est supérieur à un certain seuil (par exemple 0.5)
        if image_name not in seen_images:
            seen_images.add(image_name)
            if image_name:
                print(f"Id : {result.id}")
                print(f"File name : {image_name}")
                print(f"Collection : {result.tags['collection']}")
                print(f"Score : {cosine_value}")


