from flask import Flask, render_template, redirect, url_for, request, make_response
from application import func

app = Flask(__name__)

@app.route("/")
def index():
    """ Omdirigerar till kartvyn."""
    return redirect(url_for("map_view")) 

@app.route("/map")
def map_view():
    """ Visar en karta med händelser."""
    data_url = "https://polisen.se/aktuellt/rss/stockholms-lan/handelser-rss---stockholms-lan/"
    df = func.xml_url_to_dataframe(data_url, xpath="//item") # här hämtar jag datan från RSS-flödet och gör om den till en DataFrame
    results = func.add_city_coordinates(df, title_column="title", limit=25) # lägger till latitud och longitud baserat på ortnamn i titelkolumnen
    
    events = df.to_dict(orient="records") # här gör jag om DataFrame till en lista av ordböcker
    
  
    return render_template("map.html", events=events,results=results) #pins =df.head(10).to_dict())

@app.route("/search")
def search_view():
    """ Sökvyn för att filtrera händelser efter ort """
    query = request.args.get('q', '').strip().lower() # använder mig utav .strip() för att ta bort eventuella mellanslag före och efter sökordet och .lower() för att göra sökningen case-insensitive
    data_url = "https://polisen.se/aktuellt/rss/stockholms-lan/handelser-rss---stockholms-lan/" # RSS-flödet
    df = func.xml_url_to_dataframe(data_url, xpath="//item") # hämtar datan och gör om till DataFrame från RSS-flödet
    
    # Lägg till ort-kolumn precis som i map_view
    df["Ort"] = df["title"].str.split(", ").str[-1]
    
    # Filtrera baserat på söktermen i ort-kolumnen
    if query:
        filtered_df = df[df["Ort"].str.lower().str.contains(query, na=False)]
    else:
        filtered_df = df
    
    events = filtered_df.to_dict(orient="records")

    
    resp = make_response(render_template("search_results.html", events=events, query=query))
    if query:
        resp.set_cookie("last_search", query, max_age=60*60*24) # spara i 1 dagar
    return resp


@app.route("/back") # enkel omdirigering tillbaka till kartvyn
def back():
    return redirect(url_for("map_view"))

@app.errorhandler(404)
def page_not_found(e):
    """ Hanterar 404-fel med en anpassad sida."""
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)