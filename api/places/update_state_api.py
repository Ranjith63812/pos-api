from api.customers.create.database import get_connection


def update_state_api(query_params, request_body):

    # ---------- Validation ----------
    if not query_params or not query_params.get("id"):
        return {
            "statusCode": 400,
            "message": "State id required"
        }

    if not request_body.get("state_name"):
        return {
            "statusCode": 400,
            "message": "State name required"
        }

    if not request_body.get("country_id"):
        return {
            "statusCode": 400,
            "message": "Country required"
        }

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE states
        SET state_name=%s,
            country_id=%s
        WHERE id=%s
    """

    cursor.execute(
        query,
        (
            request_body.get("state_name"),
            request_body.get("country_id"),
            query_params.get("id")
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "State updated successfully"
    }
if __name__ == "__main__":

    query = {
        "id": 2
    }

    body = {
        "state_name": "Tamil Nadu Updated",
        "country_id": 3
    }

    print(update_state_api(query, body))