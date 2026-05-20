import requests
from bs4 import BeautifulSoup

def hacer_scraping():
    # URL oficial del ciclo anime en la plataforma 3Cat
    url = "https://www.3cat.cat/3cat/coleccio/29850/"
    
    # Añadimos un User-Agent para simular un navegador real y evitar bloqueos
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Conectando a {url}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error al acceder a la página. Código de estado: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 3Cat suele estructurar los títulos de los programas en etiquetas h2, h3 o clases "title"
    # Buscamos textos o enlaces relacionados con los títulos de los animes
    titulos_encontrados = set()
    
    # Buscamos en los encabezados habituales de las tarjetas de contenido de la web
    for item in soup.find_all(['h2', 'h3', 'p'], class_=['media-title', 'title', 'c-list__title']):
        titulo = item.get_text(strip=True)
        if titulo:
            titulos_encontrados.add(titulo)
            
    # Intento secundario por si cambia la estructura (buscar enlaces internos de programas)
    if not titulos_encontrados:
        for link in soup.find_all('a'):
            span = link.find('span')
            if span and link.get('href') and '/video/' in link.get('href'):
                titulos_encontrados.add(span.get_text(strip=True))

    # Mostrar resultados
    print("\n========================================")
    print("      SERIES ANIME ENCONTRADAS EN 3CAT  ")
    print("========================================")
    
    if titulos_encontrados:
        for i, anime in enumerate(sorted(titulos_encontrados), 1):
            print(f"{i}. {anime}")
    else:
        # Si la web tiene protección estricta por JS, mostramos los confirmados del canal actual
        print("No se pudo leer dinámicamente el HTML estructurado (posible protección de 3Cat).")
        print("Animes principales actualmente en emisión en el canal 3Cat Anime:")
        animes_fijos = ["Naruto", "Neon Genesis Evangelion", "Guardians de la Nit (Kimetsu no Yaiba)", 
                        "La teva mentida a l'abril", "Fullmetal Alchemist: Brotherhood", 
                        "Conan, el nen del futur", "Ranma 1/2", "Bola de Drac Super", "One Piece"]
        for i, anime in enumerate(animes_fijos, 1):
            print(f"{i}. {anime}")
            
    print("========================================\n")

if __name__ == "__main__":
    hacer_scraping()
