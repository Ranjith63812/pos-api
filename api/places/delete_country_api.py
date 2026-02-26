from api.customers.create.database import get_connection


def delete_country_api(query_params):

    # ---------- Validation ----------
    if not query_params or not query_params.get("id"):
        return {
            "statusCode": 400,
            "message": "Country id required"
        }

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM countries WHERE id=%s"

    cursor.execute(
        query,
        (query_params.get("id"),)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "Country deleted successfully"
    }
if __name__ == "__main__":

    query = {
        "id": 2
    }

    print(delete_country_api(query))