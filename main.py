
from flask import Flask, render_template, request
from model import recommend_movies

app = Flask(__name__)

@app.route('/')
def home():

    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def recommend():

    genre = request.form.get(
        'genre',
        ''
    ).strip()

    movies = recommend_movies(genre)

    return render_template(

        "index.html",

        movies=movies,

        selected_genre=genre
    )

if __name__ == "__main__":

    app.run(debug=True)