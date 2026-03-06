import json
from database import get_connection


def update_product_api(event, context):

    request_body = json.loads(event["body"])

    if not request_body.get("id"):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Product id required"})
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:

        query = """
        UPDATE products
        SET product_name=%s,
            category_id=%s,
            barcode=%s,
            price=%s,
            stock=%s,
            tax=%s
        WHERE id=%s
        """

        cursor.execute(query, (
            request_body.get("product_name"),
            request_body.get("category_id"),
            request_body.get("barcode"),
            request_body.get("price"),
            request_body.get("stock"),
            request_body.get("tax"),
            request_body.get("id")
        ))

        conn.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Product updated successfully"
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
    return update_product_api(event, context)

if __name__ == "__main__":

    event = {
        "body": json.dumps({
            "id": 1,
            "product_name": "T-Shirt Premium",
            "category_id": 1,
            "barcode": "TSHIRT001",
            "price": 650,
            "stock": 120,
            "tax": 5
        })
    }

    response = update_product_api(event, None)
    print(response)