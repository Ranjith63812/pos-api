import json
from database import get_connection


def update_product_category_api(event, context):

    request_body = json.loads(event["body"])

    if not request_body.get("id"):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Category id required"})
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:

        query = """
        UPDATE product_categories
        SET category_name=%s,
            description=%s,
            status=%s
        WHERE id=%s
        """

        cursor.execute(query, (
            request_body.get("category_name"),
            request_body.get("description"),
            request_body.get("status"),
            request_body.get("id")
        ))

        conn.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Product category updated successfully"
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
    return update_product_category_api(event, context)

if __name__ == "__main__":

    event = {
        "body": json.dumps({
            "id": 1,
            "category_name": "Clothing",
            "description": "All clothing products",
            "status": "active"
        })
    }

    response = update_product_category_api(event, None)
    print(response)