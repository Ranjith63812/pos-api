import json
from database import get_connection


def delete_product_api(event, context):

    params = event.get("queryStringParameters")

    if not params or not params.get("id"):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Product id required"})
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:

        query = "DELETE FROM products WHERE id=%s"

        cursor.execute(query, (params.get("id"),))

        conn.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Product deleted successfully"
            })
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
    return delete_product_api(event, context)