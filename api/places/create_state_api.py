from api.customers.create.database import get_connection


def create_state_api(request_body):

    # ---------- Validation ----------
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
        INSERT INTO states (state_name, country_id)
        VALUES (%s,%s)
    """

    cursor.execute(
        query,
        (
            request_body.get("state_name"),
            request_body.get("country_id")
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "State created successfully"
    }

if __name__ == "__main__":

    body = {
        "state_name": "Tamil Nadu",
        "country_id": 3
    }

    print(create_state_api(body))