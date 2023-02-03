from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
db_path = "sqlite:///fmovies_clone.db"


def setup_db(app):
    """sets up and configure db with the flask app and migrations"""
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)


def db_drop_and_create_all(app):
    """drops all tables created and creates tables again"""
    with app.app_context():
        db.drop_all()
        db.create_all()


def add_book(movie_list):
    """takes a list of movies adds them to the database"""
    for item in movie_list:
        movie = Movies(
            movie_id=item["id"],
            title=item["title"],
            year=item["year"],
            rating=item["imDbRating"],
            image=item["image"],
            tag="Movie"
        )
        db.session.add(movie)
        db.session.commit()


def update_details(movie_to_update, movie_details):
    """
    updates the movie duration, genre, summary and country
    :param movie_details: request response from imdb-api
    :param movie_to_update: selected movie to be updated
    :return:
    """
    # movie_to_update.duration = movie_details["runtimeMins"]
    # movie_to_update.genre = movie_details["genres"]
    # movie_to_update.summary = movie_details["plot"]
    # movie_to_update.country = movie_details["countries"]

    # this is for just the banner images
    movie_to_update.banner_img = movie_details
    db.session.commit()


def first_item(items_list):
    """
    checks the imdb api result if the image has the right resolution
    :param items_list: list of image result from imdb api
    :return:
    """
    for item in items_list:
        if item["image"].endswith("Ratio1.5000_AL_.jpg") or item["image"].endswith("Ratio1.4600_AL_.jpg") or item["image"].endswith("Ratio1.7600_AL_.jpg"):
            return item["image"]


class Movies(db.Model):
    """creates the table in the database"""
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, unique=True, nullable=False)
    year = db.Column(db.String(20))
    duration = db.Column(db.String(20))
    rating = db.Column(db.String(20))
    genre = db.Column(db.String(100))
    image = db.Column(db.String(200))
    summary = db.Column(db.String)
    country = db.Column(db.String(100))
    tag = db.Column(db.String, nullable=False)
    banner_img = db.Column(db.String(200))
