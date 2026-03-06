import json
from database import get_connection


def get_product_categories_api(event, context):

    params = event.get("queryStringParameters")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        if params and params.get("id"):

            query = """
            SELECT id, category_name, description, status, created_at
            FROM product_categories
            WHERE id=%s
            """

            cursor.execute(query, (params.get("id"),))
            result = cursor.fetchone()

        else:

            query = """
            SELECT id, category_name, description, status, created_at
            FROM product_categories
            ORDER BY id DESC
            """

            cursor.execute(query)
            result = cursor.fetchall()

        return {
            "statusCode": 200,
            "body": json.dumps(result, default=str)
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    finally:
        cursor.close()
        conn.close()


def lambda_handler(event, context):
    return get_product_categories_api(event, context)

if __name__ == "__main__":

    # Test get all
    event = {
        "queryStringParameters": None
    }

    response = get_product_categories_api(event, None)
    print(response)

    # Test get by id
    event = {
        "queryStringParameters": {
            "id": "1"
        }
    }

    response = get_product_categories_api(event, None)
    print(response)