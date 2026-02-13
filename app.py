from flask import Flask, render_template, request
import tmdb_client
import random

app = Flask(__name__)

@app.route('/')
def homepage():
    movie_lists = tmdb_client.get_all_lists()
    requested_list_type = request.args.get('list_type')
    available_api_names = [item["api_name"] for item in movie_lists]

    if requested_list_type not in available_api_names:
        requested_list_type = "popular"
    
    movies = []
    for item in movie_lists:
        if item["api_name"] == requested_list_type:
            movies = item["movies"]
            break

    return render_template("homepage.html", movies=movies[:8], movie_lists=movie_lists)

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    movie_images = tmdb_client.get_movie_images(movie_id)
    selected_backdrop = random.choice(movie_images['backdrops'])
    return render_template("movie_details.html", movie=details, cast=cast, selected_backdrop=selected_backdrop)

if __name__ == '__main__':
    app.run(debug=True)