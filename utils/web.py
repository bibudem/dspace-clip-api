from clip_client import Client
from jina import Document
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import json
import requests

# Initialisation de l'application FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/img", StaticFiles(directory="img"), name="img")


# Lecture des configurations depuis le fichier JSON
with open('./config/config.json') as config_file:
    config = json.load(config_file)

# Initialisation du client CLIP
client = Client(config['clip_server'])
limit = config['limit']

# Route pour la page d'accueil
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("form-search.html", {"request": request})

@app.get("/search")
async def search(request: Request, keyword: str = Query(None), format: str = Query(None)):
    content = {}
    if keyword:
        search_result_keyword = client.search([keyword], limit)
        results_keyword = search_result_keyword[0].matches

        # Appel aux fonctions utilitaires pour obtenir les données de réponse
        response_data_keyword = get_response_data(results_keyword)
        message_keyword = f"Résultats pour la recherche: {keyword}"

        content["message_keyword"] = message_keyword
        content["results_keyword"] = response_data_keyword

    if format == "json":
        return JSONResponse(content)
    elif format == "html":
         content["request"] = request
         return templates.TemplateResponse("reponses.html", content)
    else:
        return "Format non pris en charge. Utilisez 'json' ou 'html'."

# Fonction utilitaire pour obtenir les données de réponse à partir des résultats de la recherche
def get_response_data(results):
    response_data = []
    path = ''
    image_name = ''

    for result in results:
        cosine_value = result.scores.get('cosine').value
        cosine_value = round(cosine_value, 2)
        if result.uri:
            path =  result.uri
            image_name = os.path.basename(path)

        item = {
            "Id": result.id,
            "Proximité": cosine_value,
            "Fichier": image_name,
            "Collection": result.tags.get('collection', ''),
        }
        response_data.append(item)

    return response_data
