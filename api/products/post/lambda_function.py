import json
from database import get_connection


def create_product_api(event, context):

    request_body = json.loads(event["body"])

    if not request_body.get("product_name"):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Product name required"})
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:

        query = """
        INSERT INTO products
        (product_name, category_id, barcode, price, stock, tax)
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(query, (
            request_body.get("product_name"),
            request_body.get("category_id"),
            request_body.get("barcode"),
            request_body.get("price"),
            request_body.get("stock"),
            request_body.get("tax")
        ))

        conn.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Product created successfully"
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
    return create_product_api(event, context)

if __name__ == "__main__":

    event = {
        "body": json.dumps({
            "product_name": "T-Shirt",
            "category_id": 1,
            "barcode": "TSHIRT001",
            "price": 500,
            "stock": 100,
            "tax": 5
        })
    }

    response = create_product_api(event, None)
    print(response)