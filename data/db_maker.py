import requests
from dotenv import load_dotenv
import os
import math
from data.models import Movie
import pandas

load_dotenv(".env")

class MovieAPI:
    API_KEY = os.getenv("API_KEY")
    IMAGE_URL = "https://image.tmdb.org/t/p/w500"
    SEARCH_URL = "https://api.themoviedb.org/3"
    MORE_INFO_URL = "https://api.themoviedb.org/3/movie"
    params_search = {
    "api_key" : API_KEY,
    "query" : "captain america"
    }

    def __init__(self, movie_name:str) -> None:
        """Enter the movie name to search"""
        self.params_search["query"] = movie_name

    def search(self) -> list: 
        response = requests.get(url=f"{self.SEARCH_URL}/search/movie", params=self.params_search)
        data = response.json()["results"][0]
        return data

def add_data():
    movie_object = pandas.read_csv("data/movies.csv")
    for movie in movie_object.iterrows():
        object = MovieAPI(movie[1]["name"])
        Movie.objects.create(name = object.search()['title'],
                            genre = movie[1]['genre'],
                            rating = round(object.search()['vote_average'] , 2),
                            popularity = math.floor(float(object.search()['popularity'])),
                            year = object.search()['release_date'].split('-')[0],
                            synopsis = object.search()['overview'],
                            image = f"{object.IMAGE_URL}{object.search()['poster_path']}?api_key={object.API_KEY}",
                            price = movie[1]['price'])

