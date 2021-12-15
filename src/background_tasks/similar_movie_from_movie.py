from core.database.mongo import get_collection, get_db_client
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import time
import asyncio


async def main():
    t1 = time.time()
    movie_collection = await get_collection("Movies")
    similar_collection = await get_collection("similar_movie_from_movie")
    similar_collection.drop()

    movie_exist = movie_collection.find()
    # movie_exist.limit(100)
    movie_to_list = await movie_exist.to_list(None)

    temp_list = list(movie for movie in movie_to_list if not len(movie["Reviews"]) < 1)

    temp_list = list(
        map(
            lambda movie: {
                "MovieId": movie["_id"],
                "Name": movie["Name"],
                "Reviews": movie["Reviews"],
            },
            temp_list,
        )
    )

    raw_df = pd.DataFrame(temp_list)
    df = raw_df.drop(columns=["Name"])
    df = df.explode("Reviews")

    df[["CustomerId", "Stars", "Comment"]] = df.Reviews.apply(pd.Series)
    df = (
        df.drop(columns=["Reviews"])
        .set_index(["MovieId", "CustomerId"])
        .unstack(["CustomerId"])
        .fillna(0)
    )

    df = df.drop(columns=["Comment"])
    knn = NearestNeighbors(metric="cosine", algorithm="brute")

    knn.fit(df.values)

    distances, indices = knn.kneighbors(df.values, n_neighbors=5)

    for title in df.index:
        try:
            index_user_likes = df.index.tolist().index(title)
            sim_movies = indices[index_user_likes].tolist()
            movie_distances = distances[index_user_likes].tolist()
            id_movie = sim_movies.index(index_user_likes)

            sim_movies.remove(index_user_likes)
            movie_distances.pop(id_movie)
            sim_movies_ids = list(
                map(
                    lambda row: {
                        "name": movie_name_from_id(raw_df, df.index[row]),
                        "id": df.index[row],
                    },
                    sim_movies,
                )
            )

            await similar_collection.insert_one(
                dict(
                    _id=title,
                    name=movie_name_from_id(raw_df, title),
                    similar=sim_movies_ids,
                )
            )
        except Exception as e:
            print(e)
            
    t2 = time.time()

    print("Stop job: calculate similarities after {} seconds".format((t2 - t1)))


def movie_name_from_id(df, MovieId):
    names = df[df.MovieId == MovieId].Name

    return names.iloc[0]
