from typing import Any
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from core.base_model import DataWithPagination, Pagination
from core.config import settings
from core.database.mongo import get_collection
from databases.movie.model import MovieModel
import uuid


class MovieRepository:
    async def find_many(
        self,
        params,
        pagination: Pagination,
        sort: Any,
    ):
        max_per_page = settings.PAGINATION.MAX_PER_PAGE
        movie_collection = await get_collection("Movies")

        founds = movie_collection.find(params)
        total_entries = await movie_collection.count_documents({})
        if pagination["page"]:
            founds = founds.skip((pagination["page"] - 1) * pagination["per_page"])

        if pagination["per_page"]:
            founds = founds.limit(min(max_per_page, pagination["per_page"]))

        if sort:
            founds = founds.sort(sort["key"], int(sort["direction"]))

        if not founds:
            return None

        founds.limit(10)

        movie_to_list = await founds.to_list(None)

        movies = list(
            map(
                lambda movie: MovieModel(**movie, id=movie["_id"]),
                movie_to_list,
            )
        )

        return DataWithPagination(
            total_entries=total_entries,
            per_page=pagination["per_page"],
            page=pagination["page"],
            data=movies,
        )

    async def find_one(self, id):
        movie_collection = await get_collection("Movies")

        movie_exist = await movie_collection.find_one({"_id": ObjectId(id)})

        if not movie_exist:
            return None

        return MovieModel(**movie_exist, id=movie_exist["_id"])

    async def update_one(self, id, changes):
        movie_collection = await get_collection("Movies")

        changes = changes.__dict__

        await movie_collection.update_one({"_id": ObjectId(id)}, {"$set": changes})

        movie_exist = await movie_collection.find_one({"_id": ObjectId(id)})

        return MovieModel(**movie_exist)

    async def delete_one(self, id):
        movie_collection = await get_collection("Movies")

        result = await movie_collection.delete_one({"_id": ObjectId(id)})
    
        return result
    
    async def create(self, movie):
        movie_collection = await get_collection("Movies")
        
        movie_in_db = movie.__dict__
        movie_in_db['ratings'] = []
        
        result = await movie_collection.insert_one(jsonable_encoder(movie_in_db))
        
        new_movie = await movie_collection.find_one({"_id": result.inserted_id})

        return MovieModel(**new_movie, id=new_movie['_id'])
