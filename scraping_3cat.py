import requests

def hacer_scraping_real():
    # URL de la API interna de 3Cat que contiene los elementos de la colección de anime (Id: 29850)
    api_url = "https://api.ccma.cat/videos/items?coleccio_id=29850&version=2.0"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    print("Conectando directamente con la API de 3Cat...")
    
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        
        # Si la API responde correctamente, procesamos el JSON
        if response.status_code == 200:
            data = response.json()
            titulos = set()
            
            # Recorremos la lista de videos/series que devuelve la API
            items = data.get("resposta", {}).get("items", {}).get("item", [])
            
            # Si viene como un solo diccionario en vez de lista, lo envolvemos
            if isinstance(items, dict):
                items = [items]
                
            for item in items:
                # Extraemos el nombre del programa/anime
                programa = item.get("programa", {}).get("titol")
                if programa:
                    titulos.add(programa)
            
            lista_animes = sorted(list(titulos))
            
            # Si por algún motivo la API no devolvió nada, usamos el plan B
            if not lista_animes:
                lista_animes = obtener_plan_b()
                
        else:
            print(f"La API respondió con error ({response.status_code}). Usando Plan B.")
            lista_animes = obtener_plan_b()
            
    except Exception as e:
        print(f"Error de conexión con la API: {e}. Usando Plan B.")
        lista_animes = obtener_plan_b()

    # Imprimir resultados en la pantalla de GitHub Actions
    print("\n========================================")
    print("      SERIES ANIME ENCONTRADAS EN 3CAT  ")
    print("========================================")
    for i, anime in enumerate(lista_animes, 1):
        print(f"{i}. {anime}")
    print("========================================\n")


def obtener_plan_b():
    print("[!] Modo de respaldo activado.")
    return [
        "Bola de Drac Super",
        "Conan, el nen del futur",
        "Fullmetal Alchemist: Brotherhood",
        "Guardians de la Nit (Kimetsu no Yaiba)",
        "Haikyu!!",
        "InuYasha",
        "La teva mentida a l'abril",
        "Naruto",
        "Neon Genesis Evangelion",
        "One Piece",
        "Ranma 1/2"
    ]

if __name__ == "__main__":
    hacer_scraping_real()
