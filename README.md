**Händelse App**

En webbapplikation byggd i Flask som hämtar aktuella händelser från polisens RSS-flöde, geokodar adresser och visar dem på en interaktiv karta med Leaflet. Projektet började som en löneprognos-app men omstrukturerades till att fokusera på polishändelser.


***Instruktioner***

För att köra projektet lokalt behöver du först klona repot och gå in i projektmappen:

git clone <repo-url> 

cd handelse-app


Skapa sedan en virtuell miljö och aktivera den:

python3 -m venv venv 

source venv/bin/activate # Linux/Mac venv\Scripts\activate # Windows


Installera alla beroenden från `requirements.txt`:

pip install -r requirements.txt



Gå därefter in i `application`-mappen och starta appen:

cd application 

flask --app app run


Öppna sedan i webbläsaren:

http://127.0.0.1:5000



***Funktioner***

- Hämtar händelser från polisens RSS
- Geokodar adresser med Nominatim
- Visar händelser på karta och i tabell
- Testläge med hårdkodade exempel


***Källor och API:er***

- Kart api : https://leafletjs.com/ och https://nominatim.openstreetmap.org/ui/search.html  
- Polisens händelse api : https://polisen.se/aktuellt/rss/stockholms-lan/handelser-rss---stockholms-lan/  
- Geolocation HTML : https://www.w3schools.com/html/html5_geolocation.asp  
- HTML strukturering : https://getbootstrap.com/  
- Jinja strukturering : https://jinja.palletsprojects.com/en/stable/templates/  
- Flask quickstart : https://flask.palletsprojects.com/en/stable/quickstart/  

För renskrivning och små förbättringsförslag etc har jag använt följande AI-modeller :  
- Copilot  
- ChatGPT  
- Ollamas - qwen3-coder:480b-cloud, qwen3-coder:30b  

Jag har även använt oss av Google Maps för att få exakta koordinater på latitud och longitud.







