from typing import List
from fastapi import Depends
from fastapi.routing import APIRouter
from apis.user import get_current_user
from core.base_model import BaseResponse
from core.config import MESSAGES, settings, StatusCodeEnum
from databases.movie.model import (
    RequestUpdateMovie,
    ResponseManyMovies,
    ResponseSingleMovie,
    SearchMovieRequest,
    SingleMovie,
)

from databases.movie.repository import MovieRepository
from databases.user.helper import get_rating
from databases.user.model import UserModel


router = APIRouter()

movie_repository = MovieRepository()


@router.post("/search", tags=["movie"], response_model=ResponseManyMovies)
async def search_movie(request: SearchMovieRequest):
    query = {}
    
    if request.search_text:
        query = {"$text": {"$search": request.search_text}}

    pagination = {
        "page": settings.PAGINATION.DEFAULT_PAGE,
        "per_page": settings.PAGINATION.DEFAULT_PER_PAGE,
    }
    
    pagination['page'] = abs(int(request.page))       

    pagination['per_page'] = abs(int(request.per_page))
 

    sort = {"key": "created_at", "direction": request.sort}

    movie_exists = await movie_repository.find_many(query, pagination, sort)

    for movie in movie_exists.data:
        movie.ratings = get_rating(movie.ratings)
        movie.id = str(movie.id)

    return BaseResponse(
        code=StatusCodeEnum.success, message=MESSAGES["success"], data=movie_exists
    )

@router.get("/{id}", tags=["movie"], response_model=ResponseSingleMovie)
async def get_movie(id: str) -> ResponseSingleMovie:

    movie_exist = await movie_repository.find_one(id)
    
    if movie_exist is None:
        return BaseResponse(
        code=StatusCodeEnum.failed, message=MESSAGES["movie_not_found"]
    )
        
    movie_exist.ratings = get_rating(movie_exist.ratings)
    movie_exist.id = str(movie_exist.id)

    return BaseResponse(
        code=StatusCodeEnum.success, message=MESSAGES["success"], data=movie_exist
    )


@router.put("/{id}", tags=["movie"], response_model=BaseResponse)
async def update_movie(
    id: str,
    changes: RequestUpdateMovie,
    current_user: UserModel = Depends(get_current_user),
) -> ResponseSingleMovie:
    # changes.id = id
    movie_exist = await movie_repository.update_one(id, changes)

    movie_exist.ratings = get_rating(movie_exist.ratings)
    movie_exist.id = str(movie_exist.id)

    return BaseResponse(
        code=StatusCodeEnum.success, message=MESSAGES["success"], data=movie_exist
    )
    
@router.post("", tags=["movie"], response_model=BaseResponse)
async def create_movie(
    movie: RequestUpdateMovie,
    # current_user: UserModel = Depends(get_current_user),
) -> ResponseSingleMovie:
    movie_exist = await movie_repository.create(movie)

    movie_exist.ratings = get_rating(movie_exist.ratings)
    movie_exist.id = str(movie_exist.id)

    return BaseResponse(
        code=StatusCodeEnum.success, message=MESSAGES["success"], data=movie_exist
    )
    
@router.delete("/{id}", tags=["movie"], response_model=BaseResponse)
async def delete_movie(
    id: str,
    current_user: UserModel = Depends(get_current_user),
) -> ResponseSingleMovie:
    # changes.id = id
    await movie_repository.delete_one(id)

    return BaseResponse(
        code=StatusCodeEnum.success, message=MESSAGES["success"]
    )
