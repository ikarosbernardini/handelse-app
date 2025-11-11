from urllib import request
import ssl
import json
import pandas as pd
import requests
import pathlib # hämtar filvägshantering
import time

                        

_cache = {} # cache för att slippa upprepade geokodningsförfrågningar




BASE_DIR = pathlib.Path(__file__).resolve().parent # definierar basmappen för filvägar
DATA_FILE = BASE_DIR / "se.json" # sökväg till JSON-filen med svenska städer för pytest ska fungera och appen för samtliga användare

with open(DATA_FILE, "r", encoding="utf-8") as f: # öppnar JSON-filen
    cities = json.load(f)  # laddar svenska städer från en JSON-fil
    cities_df = pd.DataFrame(cities)  # gör om till DataFrame
    cities_df.rename(columns={"lat": "latitude", "lng": "longitude"}, inplace=True)   # byter namn på kolumner för att undvika krockar med geokodningsfunktionen

def add_city_coordinates(df, title_column="title", limit=10): 
    """
    Lägger till latitud och longitud för svenska städer i en DataFrame baserat på en titelkolumn.
    """
    df["Ort"] = df[title_column].str.split(", ").str[-1] # extraherar ort från titelkolumnen
    df = df.merge(cities_df, left_on="Ort", right_on="city", how="left") # slår ihop med cities_df baserat på ortnamn

    
    
    areas = [] # skapa en tom lista för områden
    for area in range(0, 10): # loopa genom de första 10 raderna i listan
        areas.append(df.head(limit).to_dict()["title"][area].split(", ")[-1]) 
        # lägger till ortnamnet i listan genom att splitta strängen vid ", " och ta den sista delen
    city_lookup = {c["city"]: {"lat": c["lat"], "lng": c["lng"]} for c in cities} # skapar en uppslagningstabell för städer och deras koordinater

    results = {}  # använder dict istället för lista då vi vill gruppera händelser per ort

    for i, area in enumerate(areas):  # loopa genom områdena och använder enumerate för att få indexen av områdena
        if area in city_lookup: # kolla om orten finns i uppslagningstabellen
            coords = city_lookup[area] # hämta koordinaterna
             # om orten inte finns i results, skapa en ny post
            if area not in results: 
                results[area] = {
                    "city": area,
                    "lat": coords["lat"],
                    "lng": coords["lng"],
                    "events": []   # lista med händelser för denna ort
                }
            results[area]["events"].append({
                "title": df.head(limit).iloc[i]["title"], # .iloc[i] för att få rätt rad
                "link": df.head(limit).iloc[i]["link"] # använder df.head(limit).iloc[i] för att få rätt rad
            }) # lägger till händelsen i listan för denna ort

# gör om dict till lista
    results = list(results.values()) # använder values() för att få en lista av värdena i dict

    #print(results)  # felsökning
    return results   # returnerar listan med orter och deras händelser

    

def json_url_to_html_table(url, columns=None): 
    """
    Hämtar JSON format och returnerar en HTML-tabell (via Pandas).
    """
    try:
        raw = request.urlopen(url, context=ssl._create_unverified_context()).read() # Hämta rådata från URL:en
        data = json.loads(raw) # Ladda JSON-datan
        df = pd.DataFrame(data) # Gör om till DataFrame
        return df.to_html(columns=columns, classes="table p-5", justify="left") # Gör om till HTML-tabell
    except Exception as e:
        print("Fel vid hämtning av JSON formatet:", e) # Felhantering
        return "<p>Kunde inte hämta datan korrekt.</p>"
    
    

def xml_url_to_dataframe(data_url, xpath="//item"):
    """
    Hämtar XML-data och gör om till en DataFrame med hjälp av Pandas.
    """
    try: 
        raw = request.urlopen(data_url, context=ssl._create_unverified_context()).read() # Hämta rådata från URL:en
        return pd.read_xml(raw, xpath=xpath) # Gör om till DataFrame
    except Exception as e:
        print("Fel vid hämtning/parsing av XML:", e) # Felhantering
        return pd.DataFrame()
    
def geocode_dataframe(df, columns="description"):
    """
    Geokodar en DataFrame med hjälp av Nonimatim (OpenStreetMap) API:n.
    """
    lat_list, lon_list = [], [] # listor för latitud och longitud
    for address in df[columns]: # går igenom varje adress i den angivna kolumnen
        if pd.isna(address):
            lat_list.append(None); lon_list.append(None) 
            continue

        if address in _cache: # kolla om adressen finns i cache
            lat, lon = _cache[address] # hämta lat/lon från cache
        else: 
            try:
                url = "https://nominatim.openstreetmap.org/search" # Nominatim API-endpointen
                query = {"q": address, "format": "json", "limit": 1} # parametrar för förfrågan, alltså vad vi söker efter i API:n
                r = requests.get(url, params=query, headers={"User-Agent": "FlaskApp"}) # skickar en GET-förfrågan
                data = r.json() # hämtar JSON-svaret
                if data: # om data finns
                    lat = float(data[0]["lat"])
                    lon = float(data[0]["lon"])
                    _cache[address] = (lat, lon) # spara i cache
                else:
                    lat, lon = None, None # om ingen data hittas så sätts lat/lon till None
            except Exception: # Felhantering
                lat, lon = None, None
                time.sleep(1)  # Vänta en sekund vid fel för att undvika överbelastning av API:n

        lat_list.append(lat) # lägg till latitud i listan
        lon_list.append(lon) # lägg till longitud i listan

        df["latitude"] = lat_list # lägg till latitud-kolumn i DataFrame
        df["longitude"] = lon_list # lägg till longitud-kolumn i DataFrame
    return df # returnera den uppdaterade DataFrame:n



            