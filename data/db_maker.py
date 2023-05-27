# Do NOT run this file

import requests
from dotenv import load_dotenv
import os

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

# movie = MovieAPI("spiderman")
# #print(movie.search())
# print(f"rating is {movie.search()['vote_average']}/10")
# print(f"Summary : {movie.search()['overview']}")
# print(f"image URL : {movie.IMAGE_URL}{movie.search()['poster_path']}?api_key={movie.API_KEY}")
# print(f"Year of release is {movie.search()['release_date'].split('-')[0]}")
# Name, Genre and Price is provided by me.

# movie_object = open("data/movie_list.txt", "r")
# movie_list = movie_object.readlines()
# movies = []
# for _ in movie_list:
#     print(_.split("\n")[0])
#     movies.append(_.split("\n")[0])

# for movie in movies:
#     object = MovieAPI(movie)
#     print(f"movie name is {movie}")
#     print(f"genre is ")
#     print(f"rating is {object.search()['vote_average']}/10")
#     print(f"Summary : {object.search()['overview']}")
#     print(f"image URL : {object.IMAGE_URL}{object.search()['poster_path']}?api_key={object.API_KEY}")
#     print(f"Year of release is {object.search()['release_date'].split('-')[0]}")
#     print(f"Price is only INR")
#     print("\n\n\n")

# import pandas

# # movie_object = pandas.read_csv("data/movie_list.csv")
# # for movie in movie_object.iterrows():
# #     object = MovieAPI(movie[1]["name"])
# #     print(f"movie name is {object.search()['title']}")
# #     print(f"genre is {movie[1]['genre']}")
# #     print(f"rating is {object.search()['vote_average']}/10")
# #     print(f"Summary : {object.search()['overview']}")
# #     print(f"image URL : {object.IMAGE_URL}{object.search()['poster_path']}?api_key={object.API_KEY}")
# #     print(f"Year of release is {object.search()['release_date'].split('-')[0]}")
# #     print(f"Price is only {movie[1]['price']} INR")
# #     print("\n\n")

movie = MovieAPI("LA 92")
print(movie.search())     