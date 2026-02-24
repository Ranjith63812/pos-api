import json
from database import get_connection


def lambda_handler(event, context):

    print("EVENT:", event)   # ✅ temporary debug

    conn = get_connection()
    cursor = conn.cursor()

    query_params = event.get("queryStringParameters")

    # ✅ Fetch by ID using query parameter
    if query_params and query_params.get("id"):

        customer_id = query_params.get("id")

        query = "SELECT * FROM customers WHERE id = %s"
        cursor.execute(query, (customer_id,))

        result = cursor.fetchone()

    else:
        # ✅ Fetch all customers
        query = "SELECT * FROM customers"
        cursor.execute(query)

        result = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": result
        }, default=str)
    }