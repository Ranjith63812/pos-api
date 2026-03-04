from api.customers.create.database import get_connection


def change_password_api(request_body):

    # ---------- Validation ----------
    if not request_body.get("username"):
        return {
            "statusCode": 400,
            "message": "Username required"
        }

    if not request_body.get("current_password"):
        return {
            "statusCode": 400,
            "message": "Current password required"
        }

    if not request_body.get("new_password"):
        return {
            "statusCode": 400,
            "message": "New password required"
        }

    if not request_body.get("confirm_password"):
        return {
            "statusCode": 400,
            "message": "Confirm password required"
        }

    if request_body.get("new_password") != request_body.get("confirm_password"):
        return {
            "statusCode": 400,
            "message": "Passwords do not match"
        }

    conn = get_connection()
    cursor = conn.cursor()

    # ---------- Check Current Password ----------
    query = """
        SELECT password
        FROM users
        WHERE username=%s
    """

    cursor.execute(query, (request_body.get("username"),))
    result = cursor.fetchone()

    if not result:
        return {
            "statusCode": 404,
            "message": "User not found"
        }

    db_password = result["password"]

    if db_password != request_body.get("current_password"):
        return {
            "statusCode": 400,
            "message": "Current password incorrect"
        }

    # ---------- Update Password ----------
    update_query = """
        UPDATE users
        SET password=%s
        WHERE username=%s
    """

    cursor.execute(
        update_query,
        (
            request_body.get("new_password"),
            request_body.get("username")
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "Password updated successfully"
    }


# ---------- Local Testing ----------
if __name__ == "__main__":

    body = {
        "username": "Sales",
        "current_password": "123456",
        "new_password": "abcdef",
        "confirm_password": "abcdef"
    }

    print(change_password_api(body))