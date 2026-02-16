import requests
import random

API_TOKEN = "Top_Secret"

def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"

def get_movies(how_many=4, list_type = "popular"):
    data = get_movies_list(list_type)
    results = data["results"][:]
    random.shuffle(results)
    return results[:how_many]

def get_single_movie(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_single_movie_cast(movie_id, limit=8):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response_json = response.json()
    return response_json["cast"][:limit]


def get_movie_images(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

def get_movies_list(list_name):
    endpoint = f"https://api.themoviedb.org/3/movie/{list_name}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()

def get_all_lists():
    now_playing = {
        "button_name": "Now playing",
        "api_name": "now_playing",
        "movies": get_movies_list("now_playing")["results"]
    }
    popular = {
        "button_name": "Popular",
        "api_name": "popular",
        "movies": get_movies_list("popular")["results"]
    }
    top_rated = {
        "button_name": "Top rated",
        "api_name": "top_rated",
        "movies": get_movies_list("top_rated")["results"]
    }
    upcoming = {
        "button_name": "Upcoming",
        "api_name": "upcoming",
        "movies": get_movies_list("upcoming")["results"]
    }
    movie_lists = [now_playing, popular, top_rated, upcoming]
    return movie_lists