import json
from database import get_connection


def create_product_category_api(event, context):

    request_body = json.loads(event["body"])

    if not request_body.get("category_name"):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Category name required"})
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:

        query = """
        INSERT INTO product_categories
        (category_name, description, status)
        VALUES (%s,%s,%s)
        """

        cursor.execute(query, (
            request_body.get("category_name"),
            request_body.get("description"),
            request_body.get("status")
        ))

        conn.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Product category created successfully"
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
    return create_product_category_api(event, context)

if __name__ == "__main__":
    import json

    event = {
        "body": json.dumps({
            "category_name": "Electronics",
            "description": "Electronic devices",
            "status": "active"
        })
    }

    response = create_product_category_api(event, None)
    print(response)