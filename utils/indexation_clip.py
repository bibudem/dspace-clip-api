import os
from clip_client import Client
from docarray import Document
import time
import argparse

def index_images_in_folder(client, folder_path,collection_name):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # Ajoutez les extensions d'images nécessaires

    for i, filename in enumerate(os.listdir(folder_path)):
        if any(filename.endswith(ext) for ext in image_extensions):
            image_path = os.path.join(folder_path, filename)
            document = Document(uri=image_path)
            #document.id = str(i) # Ajoutez une formule personnalisée pour l'identifiant si nécessaire ; sinon, le système le génère automatiquement.
            document.tags['collection'] = collection_name
            document.tags['fileName'] = filename
            client.index([document],show_progress=True)
    # Affichez le message d'indexation terminée
    print(f'Indexation terminée pour {len(os.listdir(folder_path))} fichiers.')


if __name__ == '__main__':
      parser = argparse.ArgumentParser(description='Indexation d\'images avec CLIP')
      parser.add_argument('--folder', type=str, help='Chemin du dossier contenant les images')
      parser.add_argument('--collection', type=str, help='Nom de la collection')
      args = parser.parse_args()

      folder_path = args.folder
      collection_name = args.collection

      # Enregistrez le temps de début
      start_time = time.time()

      # Créez un objet Client en spécifiant l'URL du serveur CLIP
      client = Client('grpc://127.0.0.1:51000')

      # Indexez toutes les images du dossier "files"
      index_images_in_folder(client, folder_path,collection_name)

      # Enregistrez le temps de fin
      end_time = time.time()

      # Calculez la durée d'exécution
      execution_time = end_time - start_time

      # Affichez la durée d'exécution
      print(f"Temps d'exécution : {execution_time} secondes")





