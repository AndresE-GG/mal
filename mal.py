import os
import requests
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env (si existe)
load_dotenv()

# Obtiene el Client ID desde la variable de entorno
CLIENT_ID = os.getenv("MAL_CLIENT_ID")

def obtener_animes_oficial(letra):
    """
    Busca animes usando la API oficial de MyAnimeList (v2).
    """
    if not CLIENT_ID or CLIENT_ID == "TU_CLIENT_ID_AQUI":
        return {"error": "No se ha configurado el MAL_CLIENT_ID en las variables de entorno."}

    url = "https://api.myanimelist.net/v2/anime"
    headers = {"X-MAL-CLIENT-ID": CLIENT_ID}
    
    parametros = {
        "q": letra,
        "limit": 100, 
        "fields": "id,title,mean,main_picture" 
    }

    try:
        respuesta = requests.get(url, headers=headers, params=parametros)
        
        # Si MAL rechaza la petición por ser muy corta (menos de 3 caracteres)
        if respuesta.status_code == 400:
            url_ranking = "https://api.myanimelist.net/v2/anime/ranking"
            params_ranking = {"ranking_type": "tv", "limit": 500, "fields": "id,title,mean,main_picture"}
            respuesta = requests.get(url_ranking, headers=headers, params=params_ranking)
            respuesta.raise_for_status()
            
            todos_los_animes = respuesta.json().get("data", [])
            animes_filtrados = [
                item for item in todos_los_animes
                if item["node"]["title"].lower().startswith(letra.lower())
            ]
            
            return _formatear_resultados(animes_filtrados)
            
        respuesta.raise_for_status()
        datos = respuesta.json()
        
        lista_animes = datos.get("data", [])
        animes_filtrados = [
            item for item in lista_animes
            if item["node"]["title"].lower().startswith(letra.lower())
        ]
        
        return _formatear_resultados(animes_filtrados)
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al interactuar con la API: {str(e)}"}

def _formatear_resultados(items):
    resultados = []
    for item in items:
        anime = item.get("node", {})
        id_anime = anime.get("id", "N/A")
        
        imagen = ""
        if "main_picture" in anime:
            imagen = anime["main_picture"].get("large", anime["main_picture"].get("medium", ""))
            
        resultados.append({
            "id": id_anime,
            "title": anime.get("title", "Desconocido"),
            "score": anime.get("mean", "N/A"),
            "image": imagen,
            "url": f"https://myanimelist.net/anime/{id_anime}"
        })
    return resultados

if __name__ == "__main__":
    print("--- Buscador de Anime (MAL API v2) ---")
    letra_busqueda = input("Ingresa la letra inicial del anime: ")
    print(obtener_animes_oficial(letra_busqueda))