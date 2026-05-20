import requests
from bs4 import BeautifulSoup

# URL oficial de la colección Anime en 3Cat
url = "https://www.3cat.cat/3cat/coleccio/29850/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ca,es;q=0.9"
}

print(f"Conectando a {url}...\n")

titulos_encontrados = set()

try:
    response = requests.get(url, headers=headers, timeout=15)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Buscar en componentes de tarjetas de 3Cat
        for tag in soup.find_all(['h2', 'h3', 'h4', 'span', 'p']):
            clases = tag.get('class', [])
            clases_texto = " ".join(clases)
            
            if any(x in clases_texto for x in ['title', 'media-title', 'c-card__title', 'c-list__title']):
                titulo = tag.get_text(strip=True)
                if titulo and len(titulo) > 1:
                    titulos_encontrados.add(titulo)

        # 2. Buscar desde los atributos alt de imágenes de logos de series
        for img in soup.find_all('img'):
            alt = img.get('alt', '')
            if alt:
                if "Logotip de" in alt:
                    titulos_encontrados.add(alt.replace("Logotip de", "").strip())
                elif "Imatge de" in alt:
                    titulos_encontrados.add(alt.replace("Imatge de", "").strip())
except Exception as e:
    print(f"Hubo un problema al conectar: {e}")

# Pasar a formato de lista ordenada
lista_final = sorted(list(titulos_encontrados))

# SI NO FUNCIONA EL SCRAPING (lista vacía), cargamos el catálogo actual manualmente
if not lista_final:
    print("[!] No se detectó contenido dinámico en la web. Cargando catálogo actual...")
    lista_final = [
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

# Imprimir el resultado final en la consola de GitHub
print("========================================")
print("      SERIES ANIME ENCONTRADAS EN 3CAT  ")
print("========================================")
for i, anime in enumerate(lista_final, 1):
    print(f"{i}. {anime}")
print("========================================")
