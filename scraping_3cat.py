import requests
from bs4 import BeautifulSoup
import re

def hacer_scraping_real():
    url = "https://www.3cat.cat/3cat/coleccio/29850/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ca,es;q=0.9"
    }
    
    print(f"Conectando con 3Cat ({url}) para extraer HTML real...")
    
    lista_animes = []
    usando_plan_b = False
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        titulos_animes = set()
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            enlaces = soup.find_all('a', href=True)
            
            for enllac in enlaces:
                href = enllac['href']
                if "/3cat/" in href and "/video/" in href:
                    match = re.search(r'/3cat/([^/]+)/video/', href)
                    if match:
                        slug = match.group(1)
                        nombre_limpio = limpiar_nombre_anime(slug)
                        if nombre_limpio:
                            titulos_animes.add(nombre_limpio)
            
            lista_animes = sorted(list(titulos_animes))
            
            if not lista_animes:
                print("[!] Alerta: No se extrajeron títulos del HTML.")
                lista_animes = obtener_plan_b()
                usando_plan_b = True
        else:
            print(f"[!] Alerta: El servidor respondió con código {response.status_code}.")
            lista_animes = obtener_plan_b()
            usando_plan_b = True
            
    except Exception as e:
        print(f"[!] Alerta: Error durante la ejecución: {e}")
        lista_animes = obtener_plan_b()
        usando_plan_b = True

    print("\n========================================")
    if usando_plan_b:
        print("  ⚠️  ESTADO: FALLÓ EL SCRAPING EN VIVO ")
        print("  (Mostrando lista de respaldo/Plan B)  ")
    else:
        print("  ✅  ESTADO: SCRAPING EXITOSO (EN VIVO) ")
    print("========================================")
    
    for i, anime in enumerate(lista_animes, 1):
        print(f"{i}. {anime}")
        
    print("========================================\n")


def limpiar_nombre_anime(slug):
    """Limpia los slugs de las URLs para extraer el nombre de la serie"""
    slug = re.sub(r'-(cap|capitol|temporada|t\d+x\d+|t\d+|\d+).*$', '', slug, flags=re.IGNORECASE)
    nombre = slug.replace('-', ' ').title()
    
    # CORREGIDO: Ahora el nombre del diccionario coincide con el return
    correcciones = {
        "Saint Seiya El Quadre Perdut": "Saint Seiya: El Quadre Perdut",
        "Crueltat": "Guardians de la Nit (Kimetsu no Yaiba)",
        "Evangelion": "Neon Genesis Evangelion",
        "L Alquimista D Acer": "Fullmetal Alchemist: Brotherhood"
    }
    return correcciones.get(nombre, nombre)


def obtener_plan_b():
    return [
        "Bola de Drac Super",
        "Conan, el nen del futur",
        "Fullmetal Alchemist: Brotherhood",
        "Guardians de la Nit (Kimetsu no Yaiba)",
        "Haikyu!!",
        "InuYasha",
        "One Piece",
        "Neon Genesis Evangelion",
        "Saint Seiya: El Quadre Perdut"
    ]

if __name__ == "__main__":
    hacer_scraping_real()
