from clip_client import Client
from jina import Document
from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

# Initialisation de l'application FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/img", StaticFiles(directory="img"), name="img")

# Initialisation du client Clip
c = Client('grpc://127.0.0.1:51000')
limit = 5

# Route pour la page d'accueil
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("form-search.html", {"request": request})

# Route pour la recherche au format JSON
@app.post("/search-rjson")
async def searchForm(keyword: str = Form(None)):
    content = await get_formSearchValues(keyword)
    return JSONResponse(content)

# Route pour la recherche au format HTML
@app.post("/search-rhtml", response_class=HTMLResponse)
async def afficher_resultats_html(
    request: Request,
    keyword: str = Form(None),
    file: UploadFile = File(None)
):
    content = await get_formSearchValues(keyword)
    content["request"] = request
    return templates.TemplateResponse("reponses.html", content)

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
            "Score": cosine_value,
            "image_name": image_name,
            "collection": result.tags['collection'],
        }
        response_data.append(item)

    return response_data

# Fonction utilitaire pour traiter les données du formulaire
async def get_formSearchValues(keyword: str):
    content = {}

    if keyword:
        search_result_keyword = c.search([keyword], limit)
        results_keyword = search_result_keyword[0].matches

        # Appel aux fonctions utilitaires pour obtenir les données de réponse
        response_data_keyword = get_response_data(results_keyword)
        message_keyword = f"Voici les résultats pour le mot clé: {keyword}"

        content["message_keyword"] = message_keyword
        content["results_keyword"] = response_data_keyword

    return content
