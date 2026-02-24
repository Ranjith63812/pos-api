from config.database import get_connection


def create_customer_api(request_body):

    # validation
    if not request_body.get("customer_name"):
        return {
            "statusCode": 400,
            "message": "Customer name required"
        }

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO customers
        (customer_name, mobile, email)
        VALUES (%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            request_body.get("customer_name"),
            request_body.get("mobile"),
            request_body.get("email")
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "Customer created successfully"
    }


# ✅ LOCAL API TEST
if __name__ == "__main__":

    request = {
        "customer_name": "Ranjith",
        "mobile": "9876543210",
        "email": "ranjith@test.com"
    }

    response = create_customer_api(request)

    print(response)