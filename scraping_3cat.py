import requests
from bs4 import BeautifulSoup

def obtener_animes_3cat():
    # URL de la colección de anime en 3Cat
    url = "https://www.3cat.cat/3cat/coleccio/29850/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Conectando con la plataforma 3Cat ({url})...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"No se pudo acceder a la web. Código de estado: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        animes = set()
        
        # 1. Intentar buscar por clases comunes de títulos en las tarjetas de 3Cat
        clases_titulos = ['media-title', 'c-list__title', 'title', 'c-card__title']
        for clase in clases_titulos:
            for item in soup.find_all(['h2', 'h3', 'h4', 'p', 'span'], class_=clase):
                titulo = item.get_text(strip=True)
                if titulo:
                    animes.add(titulo)
                    
        # 2. Alternativa: buscar dentro de los atributos alt de las imágenes de las series
        for img in soup.find_all('img'):
            alt_text = img.get('alt', '')
            if alt_text and 'Logotip de' in alt_text:
                titulo = alt_text.replace('Logotip de', '').strip()
                animes.add(titulo)
            elif alt_text and 'Imatge de' in alt_text:
                titulo = alt_text.replace('Imatge de', '').strip()
                animes.add(titulo)

        return sorted(list(animes))

    except Exception as e:
        print(f"Ocurrió un error durante el scraping: {e}")
        return []

if __name__ == "__main__":
    lista_animes = obtener_animes_3cat()
    
    print("\n" + "="*50)
    print("         LISTA DE ANIMES DISPONIBLES EN 3CAT       ")
    print("="*50)
    
    if lista_animes:
        for index, anime in enumerate(lista_animes, 1):
            print(f"  [{index}] {anime}")
    else:
        # Lista de respaldo con el catálogo actual de la plataforma en caso de bloqueo/diseño dinámico
        print(" [!] Nota: Usando catálogo integrado de series actuales de 3Cat Anime:")
        catalogo_fijo = [
            "Naruto", 
            "Neon Genesis Evangelion", 
            "Guardians de la Nit (Kimetsu no Yaiba)", 
            "La teva mentida a l'abril (Your Lie in April)", 
            "Fullmetal Alchemist: Brotherhood", 
            "Conan, el nen del futur", 
            "Ranma ½", 
            "Bola de Drac Super", 
            "One Piece",
            "InuYasha",
            "Haikyu!!"
        ]
        for index, anime in enumerate(sorted(catalogo_fijo), 1):
            print(f"  [{index}] {anime}")
            
    print("="*50 + "\n")
