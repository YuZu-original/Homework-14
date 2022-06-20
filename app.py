from flask import Flask, jsonify

from films_data_base import FilmsDataBase


app = Flask(__name__)

@app.route('/movie/<title>')
def movie_by_title_page(title):
    return jsonify(FilmsDataBase().get_film_by_title(title))


@app.route('/movie/<int:year_from>/to/<int:year_to>')
def movies_from_year_to_year(year_from, year_to):
    return jsonify(FilmsDataBase().get_films_from_year_to_year(year_from, year_to))


@app.route('/rating/children')
def movies_by_rating_children():
    return jsonify(FilmsDataBase().get_films_by_rating(["G","TV-G"]))


@app.route('/rating/family')
def movies_by_rating_family():
    return jsonify(FilmsDataBase().get_films_by_rating(["G", "PG", "PG-13"]))


@app.route('/rating/adult')
def movies_by_rating_adult():
    return jsonify(FilmsDataBase().get_films_by_rating(["R", "NC-17"]))


@app.route('/genre/<genre>')
def movies_by_genre(genre):
    return jsonify(FilmsDataBase().get_films_by_genre(genre))

if __name__ == '__main__':
    app.run(debug=True)