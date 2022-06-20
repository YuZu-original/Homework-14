import sqlite3
import os.path

from exceptions import FileExtensionError


class FilmsDataBase:
    def __init__(self, path:str="netflix.db", name:str="netflix"):
        # Exceptions
        if not isinstance(path, str): raise TypeError("[!]The path must be a string")
        if not isinstance(name, str): raise TypeError("[!]The name must be a string")
        if not os.path.isfile(path): raise FileNotFoundError("[!]File {} not found".format(path))
        if (extension := os.path.splitext(path)[-1]) != ".db": raise FileExtensionError("[!]File extension is '{}' not '.db'".format(extension))
        
        self.path = path
        self.name = name
        
        with sqlite3.connect(path) as connection:
            self.cursor = connection.cursor()
    
    
    
    def get_film_by_title(self, title:str):
        """returns information about the movie by title
        
        :param title: movie name (str type)
        :return: dict with information about the movie (title, country, release_year, genre, description)
        """
        self.cursor.execute("""
                            SELECT title, country, release_year, listed_in, description
                            FROM {}
                            WHERE title = '{}'
                            ORDER BY release_year DESC
                            """.format(self.name, title))
        
        film_info = self.cursor.fetchone()
        if film_info == None: return
        return dict(zip(["title","country","release_year","genre","description"], film_info))
    
    def get_films_from_year_to_year(self, year_from:int, year_to:int):
        """returns informations about the movies which was release from year to year
        
        :param year_from: int year from (start)
        :param year_to: int year to (end)
        :return: list with dicts with information about the movie (title, release_year)
        """
        self.cursor.execute("""
                            SELECT title, release_year
                            FROM {}
                            WHERE release_year BETWEEN {} AND {}
                            LIMIT 100
                            """.format(self.name, year_from, year_to))
        return [dict(zip(["title", "release_year"], film_info)) for film_info in self.cursor.fetchall()]
    
    def get_films_by_rating(self, ratings:str|tuple|list|set):
        """returns informations about the movie by rating
        
        :param ratings: rating or ratings
        :return: list with dicts with information about the movies (title, rating, description)
        """
        ratings_str = ratings
        if isinstance(ratings, (tuple,list,set)):
            ratings_str = ', '.join([str(i).join(["'","'"]) for i in ratings])
            print(ratings_str)
        self.cursor.execute("""
                            SELECT title, rating, description
                            FROM {}
                            WHERE rating IN ({})
                            LIMIT 100
                            """.format(self.name, ratings_str))
        return [dict(zip(["title", "rating", "description"], film_info)) for film_info in self.cursor.fetchall()]
    
    
    def get_films_by_genre(self, genre):
        """returns informations about the movies by genre
        
        :param genre: genre
        :return: list with dicts with information about the movies (title, description)
        """
        self.cursor.execute("""
                            SELECT title, description
                            FROM {}
                            WHERE listed_in LIKE '%{}%'
                            ORDER BY release_year DESC
                            LIMIT 10
                            """.format(self.name, genre))
        return [dict(zip(["title", "description"], film_info)) for film_info in self.cursor.fetchall()]
    
    
    
    
    def get_actors_in_pair(self, actor1, actor2):
        """Возвращает список актеров, которые играют в паре с другими двумя больше 2 раз.
        
        На вход подаются два актера
        """
        self.cursor.execute("""
                            SELECT "cast"
                            FROM {}
                            WHERE "cast" LIKE '%{}%'
                            AND "cast" LIKE '%{}%'
                            """.format(self.name, actor1, actor2))
        all_actors = []
        for i in self.cursor.fetchall():
            all_actors += i[0].split(", ")
        
        return [x for x in set(all_actors) if all_actors.count(x) > 1 and x not in [actor1, actor2]]
    
    def get_films_by_type_year_genre(self, type, year, genre):
        """Передаем тип картины (фильм или сериал), год выпуска и ее жанр и получаем список названий картин с их описаниями в JSON."""
        self.cursor.execute("""
                            SELECT title, type, release_year, listed_in
                            FROM {}
                            WHERE type LIKE '%{}%'
                            AND release_year = {}
                            AND listed_in LIKE '%{}%'
                            """.format(self.name, type, year, genre))
        
        return [dict(zip(["title", "type", "release_year", "listed_in"], film_info)) for film_info in self.cursor.fetchall()]


#################### ДЛЯ ТЕСТОВ #####################
# test_data_base = FilmsDataBase("netflix.db", "netflix")
# 1
# print(test_data_base.get_actors_in_pair("Jack Black", "Dustin Hoffman"))
# 2
# print(test_data_base.get_films_by_type_year_genre("Movie", 2019, "Horror"))