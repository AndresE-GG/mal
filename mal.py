import requests

# REQUISITO PARA LA API OFICIAL:
# Debes registrar tu aplicación en https://myanimelist.net/apiconfig
# para obtener un "Client ID". Reemplaza el texto de abajo con tu Client ID real.
CLIENT_ID = "TU_CLIENT_ID_AQUI" 

def obtener_animes_oficial(letra):
    """
    Busca animes usando la API oficial de MyAnimeList (v2).
    """
    if not CLIENT_ID or CLIENT_ID == "TU_CLIENT_ID_AQUI":
        print("ERROR: Necesitas configurar tu CLIENT_ID en el código para usar la API Oficial.")
        print("Puedes obtener uno creando una app en: https://myanimelist.net/apiconfig")
        return

    # Endpoint oficial de búsqueda de anime
    url = "https://api.myanimelist.net/v2/anime"
    headers = {
        "X-MAL-CLIENT-ID": CLIENT_ID
    }
    
    # MAL requiere que el parámetro de búsqueda 'q' tenga. 
    # Por defecto, MAL pide al menos 3 caracteres. Si ingresan 1 letra, podríamos obtener un error 400,
    # pero enviamos la petición de todas formas en caso de que funcione o busquen algo más largo.
    parametros = {
        "q": letra,
        "limit": 100, # Límite alto para luego filtrar los que sí inicien con la letra
        "fields": "id,title,mean" 
    }

    print(f"\nConsultando a la API Oficial de MyAnimeList...")

    try:
        respuesta = requests.get(url, headers=headers, params=parametros)
        
        # Si MAL rechaza la petición por ser muy corta (menos de 3 caracteres)
        if respuesta.status_code == 400:
            print("\n[!] Error 400 Bad Request: La API oficial de MyAnimeList requiere que la búsqueda tenga por lo menos 3 caracteres.")
            print(f"Intentaste buscar con: '{letra}'.")
            
            # --- WORKAROUND (Alternativa) ---
            # Ya que la API de búsqueda no permite 1 letra, podemos buscar en el ranking general superior 
            # (top 500) y filtrar localmente los que inicien con esa letra.
            print("\nIntentando método alternativo: filtrando los mejores 500 animes...\n")
            url_ranking = "https://api.myanimelist.net/v2/anime/ranking"
            params_ranking = {"ranking_type": "all", "limit": 500, "fields": "id,title,mean"}
            respuesta = requests.get(url_ranking, headers=headers, params=params_ranking)
            respuesta.raise_for_status()
            
            todos_los_animes = respuesta.json().get("data", [])
            animes_filtrados = [
                item for item in todos_los_animes
                if item["node"]["title"].lower().startswith(letra.lower())
            ]
            
            if not animes_filtrados:
                 print(f"No se encontraron animes en el Top 500 que inicien con la letra '{letra.upper()}'.")
                 return
                 
            print(f"--- Top resultados (del ranking 500) que inician con '{letra.upper()}' ---")
            for i, item in enumerate(animes_filtrados, 1):
                anime = item.get("node", {})
                titulo = anime.get("title", "Desconocido")
                score = anime.get("mean", "N/A")
                print(f"{i}. {titulo} (⭐ {score})")
            return
            
        respuesta.raise_for_status()
        datos = respuesta.json()
        
        lista_animes = datos.get("data", [])
        
        # Filtramos estrictamente los que inician con la letra/texto asignado
        animes_filtrados = [
            item for item in lista_animes
            if item["node"]["title"].lower().startswith(letra.lower())
        ]
        
        if not animes_filtrados:
            print(f"No se encontraron animes que inicien exactamente con '{letra.upper()}' en los resultados de búsqueda.")
            return

        print(f"--- Resultados que inician con '{letra.upper()}' ---")
        for i, item in enumerate(animes_filtrados, 1):
            anime = item.get("node", {})
            titulo = anime.get("title", "Desconocido")
            score = anime.get("mean", "N/A")
            print(f"{i}. {titulo} (⭐ {score})")
            
    except requests.exceptions.RequestException as e:
        print(f"Error al conectarse a la API oficial: {e}")

if __name__ == "__main__":
    print("--- Buscador de Anime (MAL API v2) ---")
    letra_busqueda = input("Ingresa la letra inicial del anime: ")
    obtener_animes_oficial(letra_busqueda)
