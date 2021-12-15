from core.database.mongo import get_collection, get_db_client
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import time
import asyncio


async def main():
    t0 = time.time()
    similar_collection = await get_collection("similar_movie_from_user")
    user_collection = await get_collection("Customers")
    similar_collection.drop()
    num_neighbors = 5
    num_recommendation = 5
    user = "0033104c-2783-3bef-88bc-b050fcebdc83"
    number_neighbors = num_neighbors
    print("Start job: calculate similarities")
    movie_collection = await get_collection("Movies")

    movie_exist = movie_collection.find()
    customer_exist = user_collection.find()
    # movie_exist.limit(100)
    
    movie_to_list = await movie_exist.to_list(None)
    customer_to_list = await customer_exist.to_list(None)

    temp_list = list(movie for movie in movie_to_list if not len(movie["Reviews"]) < 1)
    temp_customer_id = list(customer["_id"] for customer in customer_to_list)
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
    df = raw_df.explode("Reviews")

    df[["CustomerId", "Stars", "Comment"]] = df.Reviews.apply(pd.Series)
    df = df.pivot_table(index="MovieId", columns="CustomerId", values="Stars").fillna(0)
    df.to_csv("1232.csv")
    df1 = df.copy()

    async def recommend_movies(user, num_recommended_movies):
        recommended_movies = []
        t1 = time.time()

        for m in df[df[user] == 0].index.tolist():

            index_df = df.index.tolist().index(m)
            predicted_rating = df1.iloc[index_df, df1.columns.tolist().index(user)]
            recommended_movies.append((m, predicted_rating))

        sorted_rm = sorted(recommended_movies, key=lambda x: x[1], reverse=True)
        rank = 1

        try:
            await similar_collection.insert_one(
                dict(
                    _id=user,
                    similar=list(
                        {
                            "name": movie_name_from_id(
                                raw_df, recommended_movie[0]
                            ),
                            "id": recommended_movie[0],
                        }
                        for recommended_movie in sorted_rm[
                            :num_recommended_movies
                        ]
                    ),
                    # name=movie_name_from_id(raw_df, title),
                ),
                session=s,
            )
        except Exception as e:
            print(e)                

    knn = NearestNeighbors(metric="cosine", algorithm="brute")

    knn.fit(df.values)

    distances, indices = knn.kneighbors(df.values, n_neighbors=num_neighbors)
    t1 = time.time()
    for user in temp_customer_id:
        t3 = time.time()
        print("Stop job: calculate similarities after {} seconds".format((t3 - t1)))
        t1 = time.time()

        try:
            user_index = df.columns.tolist().index(user)

            for m, t in list(enumerate(df.index)):
                if df.iloc[m, user_index] == 0:
                    sim_movies = indices[m].tolist()
                    movie_distances = distances[m].tolist()

                    if m in sim_movies:
                        id_movie = sim_movies.index(m)
                        sim_movies.remove(m)
                        movie_distances.pop(id_movie)

                    else:
                        sim_movies = sim_movies[: num_neighbors - 1]
                        movie_distances = movie_distances[: num_neighbors - 1]

                    movie_similarity = [1 - x for x in movie_distances]
                    movie_similarity_copy = movie_similarity.copy()
                    nominator = 0

                    for s in range(0, len(movie_similarity)):
                        if df.iloc[sim_movies[s], user_index] == 0:
                            if len(movie_similarity_copy) == (number_neighbors - 1):
                                movie_similarity_copy.pop(s)

                            else:
                                movie_similarity_copy.pop(
                                    s
                                    - (
                                        len(movie_similarity)
                                        - len(movie_similarity_copy)
                                    )
                                )

                        else:
                            nominator = (
                                nominator
                                + movie_similarity[s]
                                * df.iloc[sim_movies[s], user_index]
                            )

                    if len(movie_similarity_copy) > 0:
                        if sum(movie_similarity_copy) > 0:
                            predicted_r = nominator / sum(movie_similarity_copy)

                        else:
                            predicted_r = 0

                    else:
                        predicted_r = 0

                    df1.iloc[m, user_index] = predicted_r

            await recommend_movies(user, num_recommendation)
        except Exception as e:
            print(e)
    t2 = time.time()

    print("Stop job: calculate similarities after {} seconds".format((t2 - t0)))


def movie_name_from_id(df, MovieId):
    names = df[df.MovieId == MovieId].Name

    return names.iloc[0]
