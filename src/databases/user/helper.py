def user_to_dict(user) -> dict:
    
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "email": user["email"],
    }
