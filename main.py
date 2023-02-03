from flask import Flask, render_template
import requests
from models import setup_db, db_drop_and_create_all, Movies, add_book, update_details
import os
from dotenv import find_dotenv, load_dotenv

# finds the .env file automatically in case it is not in the same directory as the python file
dotenv_path = find_dotenv()

# loads up the entries in .env file
load_dotenv(dotenv_path)

IMDB_API_KEY = os.getenv("IMDB-API-KEY")

top_movies_url = f"https://imdb-api.com/en/API/MostPopularMovies/{IMDB_API_KEY}"
update_movies_url = f"https://imdb-api.com/en/API/Title/{IMDB_API_KEY}/"
update_movies_banner_img = f"https://imdb-api.com/en/API/Images/{IMDB_API_KEY}/"

app = Flask(__name__)
setup_db(app)
# db_drop_and_create_all(app) # commented out because it will always drop and create the table when run. Needs to do that just once.


@app.route("/")
def home():
    top_movies = Movies.query.paginate(per_page=24)
    return render_template("index.html", rec_mov=top_movies)


@app.route("/get-movies")
def get_movies():
    """makes a get request to a movie api to get movie details and adds it to database"""
    top_movies = requests.get(top_movies_url).json()["items"]
    add_book(top_movies)
    return "<h1>Completed</h1>"


@app.route("/update")
def update_movie_details():
    movies = Movies.query.all()
    for movie in movies:
        movie_details = requests.get(f"{update_movies_url}{movie.movie_id}").json()
        movie_to_update = Movies.query.filter_by(movie_id=movie.movie_id).first()
        update_details(movie_to_update, movie_details)
    return "Done"
