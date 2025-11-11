import pytest
import json
import pathlib
from application.app import app
import requests


@pytest.fixture # använder pytest fixture för att skapa en testklient
def client():
    app.config["TESTING"] = True
    with app.test_client() as client: # skapar en testklient
        yield client # yieldar testklienten för användning i tester

def test_search_sets_cookie(client): # testar att cookien sätts vid sökning
    # Gör en sökning
    response = client.get("/search?q=stockholm")
    # Kontrollera att cookien sätts
    assert response.status_code == 200
    assert "last_search" in response.headers.get("Set-Cookie") 

def test_search_cookie_value(client): # testar att cookien sparas korrekt
    # Gör en sökning
    client.get("/search?q=uppsala")
    # Gör en ny request utan sökparametern
    response = client.get("/search")
    # Kontrollera att cookien används
    cookie_value = response.request.cookies.get("last_search")
    assert cookie_value == "uppsala"

def test_is_web_online(client): # testar att webbsidan är online
    response = client.get("/")
    assert response.status_code == 302  # kollar så att man omdirigeras till /map

def test_404_response(client):  # testar 404 felhantering
    """ Testar 404 felhantering """
    response = client.get("/abc") # en icke-existerande sida
    assert response.status_code == 404 # kollar så att statuskoden är 404


def test_json_loads(): # testar att json-filen kan laddas korrekt
    path = pathlib.Path(__file__).resolve().parent.parent / "application" / "se.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, (dict, list))