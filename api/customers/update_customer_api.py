from api.customers.create.database import get_connection


def update_customer_api(request_body):

    if not request_body.get("id"):
        return {
            "statusCode": 400,
            "message": "Customer id required"
        }

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE customers
        SET customer_name=%s,
            mobile=%s,
            email=%s
        WHERE id=%s
    """

    cursor.execute(
        query,
        (
            request_body.get("customer_name"),
            request_body.get("mobile"),
            request_body.get("email"),
            request_body.get("id")
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "Customer updated successfully"
    }


# local test
if __name__ == "__main__":

    request = {
        "id": 1,
        "customer_name": "Updated Name",
        "mobile": "8888888888",
        "email": "updated@test.com"
    }

    print(update_customer_api(request))