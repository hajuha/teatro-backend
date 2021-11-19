from src.core.database.mongo import get_db_client

db_client = get_db_client()

class MovieRepository:
    def __init__(self):
        self.__movie_collection = db_client['teatro']['movie']

    
    async def find_many(self):

        movie_exists = self.__movie_collection.find()

        movie_exists = movie_exists.limit(10)
        if not movie_exists:
            return None

        movie_to_list = await movie_exists.to_list(None)   
        
        return movie_to_list