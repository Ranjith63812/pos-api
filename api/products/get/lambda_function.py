import json
from database import get_connection


def get_products_api(event, context):

    params = event.get("queryStringParameters")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        if params and params.get("id"):

            query = """
            SELECT 
                p.id,
                p.product_name,
                p.barcode,
                p.price,
                p.stock,
                p.tax,
                p.created_at,
                c.id AS category_id,
                c.category_name,
                c.description,
                c.status
            FROM products p
            LEFT JOIN product_categories c
            ON p.category_id = c.id
            WHERE p.id=%s
            """

            cursor.execute(query, (params.get("id"),))
            result = cursor.fetchone()

        else:

            query = """
            SELECT 
                p.id,
                p.product_name,
                p.barcode,
                p.price,
                p.stock,
                p.tax,
                p.created_at,
                c.id AS category_id,
                c.category_name,
                c.description,
                c.status
            FROM products p
            LEFT JOIN product_categories c
            ON p.category_id = c.id
            ORDER BY p.id DESC
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
    return get_products_api(event, context)
if __name__ == "__main__":

    event = {
        "queryStringParameters": None
    }

    response = get_products_api(event, None)
    print(response)

    event = {
        "queryStringParameters": {
            "id": "1"
        }
    }

    response = get_products_api(event, None)
    print(response)