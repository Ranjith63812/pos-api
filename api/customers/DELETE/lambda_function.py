import json
from database import get_connection


def lambda_handler(event, context):

    # ✅ get id from query parameter
    params = event.get("queryStringParameters")

    if not params or not params.get("id"):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Customer ID required"
            })
        }

    customer_id = params.get("id")

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM customers WHERE id=%s"

    cursor.execute(query, (customer_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Customer deleted successfully"
        })
    }


# ✅ LOCAL TEST
if __name__ == "__main__":

    event = {
        "queryStringParameters": {
            "id": "3"
        }
    }

    response = lambda_handler(event, None)
    print(response)