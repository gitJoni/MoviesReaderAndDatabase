import psycopg2

class Postgres:
    def __init__(self):
        self.movie_name = list()
        self.director = list()
        self.IMDB_rating = list()
        self.year_released = list()
        
    def sendToDatabase(self):
        # Opening connection to Database
        connection_to_moviedb = psycopg2.connect("dbname=moviedb user=**** password=****")
        cursor = connection_to_moviedb.cursor()
        # If connection couldn't be established this will return None
        if not connection_to_moviedb:
            return None
        for i in range(len(self.movie_name)):
            cursor.execute(f"INSERT INTO movies (movieid, moviename, year, director, \"IMDB rating\") VALUES ({i + 1}, '{self.movie_name[i]}', {self.year_released[i]}, '{self.director[i]}', {self.IMDB_rating[i]});")
        connection_to_moviedb.commit()
        cursor.close()
        connection_to_moviedb.close()
    
    def setToList(self, movie_name:str = "Not found", director:str = "Not found", IMDB_rating:float = 0, year_released:int = 0):
        self.movie_name.append(movie_name)
        self.director.append(director)
        self.IMDB_rating.append(IMDB_rating)
        self.year_released.append(year_released)
        