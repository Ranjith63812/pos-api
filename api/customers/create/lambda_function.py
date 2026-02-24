import json
from database import get_connection


def lambda_handler(event, context):

    # ✅ get data from API Gateway body
    request_body = json.loads(event.get("body", "{}"))

    # validation
    if not request_body.get("customer_name"):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Customer name required"
            })
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
        "body": json.dumps({
            "message": "Customer created successfully"
        })
    }


# ✅ LOCAL TEST
if __name__ == "__main__":

    event = {
        "body": json.dumps({
            "customer_name": "kumar",
            "mobile": "9876543210",
            "email": "kumar@test.com"
        })
    }

    response = lambda_handler(event, None)

    print(response)