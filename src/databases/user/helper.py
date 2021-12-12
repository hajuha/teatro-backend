def user_to_dict(user) -> dict:

    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "email": user["email"],
    }


def get_rating(ratings) -> float:
    sum = 0
    if len(ratings) == 0:
        return 0
    for rating in ratings:
        sum += int(rating.Stars)

    average_rating = float(sum) / len(ratings)

    return "{:.1f}".format(average_rating)
