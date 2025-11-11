import requests
import time

def geografisk_adress(address):
    """ Geokodar en adress med hjälp av Nominatim (OpenStreetMap).
    """

    url = "https://nominatim.openstreetmap.org/search" # Nominatim API-endpoint för interaktiva kartan
    query = {"q": address, "format": "json", "limit": 1} # Parametrar för förfrågan
    try:
        r = requests.get(url, params=query, headers={"User-Agent": "FlaskApp"}) # Skicka GET-förfrågan
        data = r.json() # Hämta JSON-svar
        if data:
            lat = float(data[0]["lat"]) # latitud
            lon = float(data[0]["lon"]) # longitud
            return lat, lon
    except Exception:
        return None, None # Felhantering för nätverksfel eller JSON-fel
    return None, None # om inte latitud/longitud hittas

