import pytest
from unittest.mock import Mock
from movies_catalogue import tmdb_client
from movies_catalogue.app import app

def test_get_single_movie_calls_correct_endpoint(monkeypatch):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 10, "title": "Test Movie"}

    mock_get = Mock(return_value=mock_response)
    monkeypatch.setattr("requests.get", mock_get)
    result = tmdb_client.get_single_movie(10)
    called_url = mock_get.call_args[0][0]
    called_headers = mock_get.call_args[1]["headers"]
    
    assert result["title"] == "Test Movie"
    assert result["id"] == 10
    assert called_url == "https://api.themoviedb.org/3/movie/10"
    assert "Authorization" in called_headers
    assert called_headers["Authorization"] == f"Bearer {tmdb_client.API_TOKEN}"


def test_get_single_movie_cast_limit(monkeypatch):
    fake_cast = [{"name": f"Actor {i}"} for i in range(20)]
    mock_response = Mock()
    mock_response.json.return_value = {"cast": fake_cast}
    monkeypatch.setattr("requests.get", Mock(return_value=mock_response))
    result = tmdb_client.get_single_movie_cast(1, limit=5)

    assert len(result) == 5
    assert result[0]["name"] == "Actor 0"
    assert result[4]["name"] == "Actor 4"

def test_get_single_movie_cast_endpoint(monkeypatch):
    mock_response = Mock()
    mock_response.json.return_value = {"cast": []}

    mock_get = Mock(return_value=mock_response)
    monkeypatch.setattr("requests.get", mock_get)
    tmdb_client.get_single_movie_cast(3)
    called_url = mock_get.call_args[0][0]

    assert called_url == "https://api.themoviedb.org/3/movie/3/credits"


def test_get_movie_images(monkeypatch):
    test_images = {
        "backdrops": [{"file_path": "/image1.jpg"}],
        "posters": []
    }

    mock_response = Mock()
    mock_response.json.return_value = test_images
    monkeypatch.setattr("requests.get", Mock(return_value=mock_response))
    result = tmdb_client.get_movie_images(11)

    assert "backdrops" in result
    assert result["backdrops"][0]["file_path"] == "/image1.jpg"


def test_get_movie_images_empty_backdrops(monkeypatch):
    mock_response = Mock()
    mock_response.json.return_value = {"backdrops": []}
    monkeypatch.setattr("requests.get", Mock(return_value=mock_response))
    result = tmdb_client.get_movie_images(1)

    assert result["backdrops"] == []


def test_get_poster_url_default_size():
    path = "/abc.jpg"
    url = tmdb_client.get_poster_url(path)
    
    assert "w342" in url
    assert url == "https://image.tmdb.org/t/p/w342//abc.jpg"


def test_get_poster_url_custom_size():
    path = "/abc.jpg"
    url = tmdb_client.get_poster_url(path, size="w500")

    assert "w500" in url
    assert url.endswith("/abc.jpg")


def test_get_movies_random_and_limit(monkeypatch):
    test_results = [{"id": i} for i in range(10)]

    mock_response = Mock()
    mock_response.json.return_value = {"results": test_results}
    mock_response.raise_for_status = Mock()

    monkeypatch.setattr("requests.get", Mock(return_value=mock_response))
    movies = tmdb_client.get_movies(how_many=3, list_type="popular")

    assert len(movies) == 3
    assert all("id" in movie for movie in movies)


def test_get_movies_list_correct_endpoint(monkeypatch):
    mock_response = Mock()
    mock_response.json.return_value = {"results": []}
    mock_response.raise_for_status = Mock()

    mock_get = Mock(return_value=mock_response)
    monkeypatch.setattr("requests.get", mock_get)
    tmdb_client.get_movies_list("top_rated")
    called_url = mock_get.call_args[0][0]
    
    assert called_url == "https://api.themoviedb.org/3/movie/top_rated"


# @pytest.mark.parametrize("list_type", ["popular", "top_rated", "upcoming", "now_playing"])
# def test_homepage_with_list_types(monkeypatch, list_type):
#     test_movie_list = [
#         {"api_name": list_type, "movies": [{"id": 1, "title": "Test Movie 1"}]},
#         {"api_name": list_type, "movies": [{"id": 2, "title": "Teste Movie 2"}]}
#     ]
#     api_mock = Mock(return_value=test_movie_list)
#     monkeypatch.setattr(tmdb_client, "get_all_lists", api_mock)

#     with app.test_client() as client:
#         response = client.get(f'/?list_type={list_type}')
#         assert response.status_code == 200
#         api_mock.assert_called_once()


@pytest.mark.parametrize("list_type", ["popular", "top_rated", "upcoming", "now_playing"])
def test_homepage_with_list_types(monkeypatch, list_type):
    test_movie_list = {"results": [{"id": 1, "title": "Test Movie 1"}]}
    api_mock = Mock(return_value=test_movie_list)
    monkeypatch.setattr(tmdb_client, "get_movies_list", api_mock)

    with app.test_client() as client:
        response = client.get(f'/?list_type={list_type}')
        assert response.status_code == 200
        api_mock.assert_called_once_with(list_type)