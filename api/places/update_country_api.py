from api.customers.create.database import get_connection


def update_country_api(query_params, request_body):

    # ---------- Validation ----------
    if not query_params or not query_params.get("id"):
        return {
            "statusCode": 400,
            "message": "Country id required"
        }

    if not request_body.get("country_name"):
        return {
            "statusCode": 400,
            "message": "Country name required"
        }

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE countries
        SET country_name=%s
        WHERE id=%s
    """

    cursor.execute(
        query,
        (
            request_body.get("country_name"),
            query_params.get("id")
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "Country updated successfully"
    }
if __name__ == "__main__":

    query = {
        "id": 1
    }

    body = {
        "country_name": "USA Updated"
    }

    print(update_country_api(query, body))