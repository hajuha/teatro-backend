from bson.objectid import ObjectId
from fastapi.routing import APIRouter
from core.base_model import BaseResponse
from core.config import MESSAGES, StatusCodeEnum
import json
from core.database.mongo import get_collection


router = APIRouter()


@router.get("/similar_movies/{id}", tags=["movie"])
async def get_similar_movies(id: str):

    similar_collection = await get_collection("similar_collection")

    movie_exist = await similar_collection.find_one({"_id": id})

    result = list(
        map(
            lambda movie: {"id": str(movie["id"]), "name": movie["name"]},
            movie_exist["similar"],
        )
    )

    return BaseResponse(
        code=StatusCodeEnum.success,
        message=MESSAGES["success"],
        data=dict(id=id, name=movie_exist["name"], similar_movies=result),
    )
