from fastapi.routing import APIRouter

from src.databases.movie.repository import MovieRepository


router = APIRouter()

movie_repository = MovieRepository()

@router.post("/movie/search")
async def search_movie():

    movie_exist = await movie_repository.find_many()
    
    movies = list(
        map(
            lambda movie: {
                "id": str(movie['_id']),
                "name": movie['name'],
                "release_date": movie['release_date'],
                "video_release_date": movie['video_release_date'],
                "imdb_link": movie['imdb_link'],
                "tags": movie['tags'],
                "ratings": movie['ratings'],
                "running_time": movie['running_time'],
                "desc": movie['desc'],
            },
            movie_exist,
        )
    )

    return {"movie_exist": movies}
