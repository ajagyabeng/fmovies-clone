from models import Movies

movie = Movies.query.all()
print(movie)
