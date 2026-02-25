import json
from database import get_connection


def lambda_handler(event, context):

    # ✅ Get request body from API Gateway
    request_body = json.loads(event.get("body", "{}"))

    # ✅ Validation
    if not request_body.get("category_name"):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Category name required"
            })
        }

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO expense_categories
        (category_name, description)
        VALUES (%s, %s)
    """

    cursor.execute(
        query,
        (
            request_body.get("category_name"),
            request_body.get("description")
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Category created successfully"
        })
    }


# ✅ LOCAL TEST
if __name__ == "__main__":

    event = {
        "body": json.dumps({
            "category_name": "Fuel",
            "description": "Petrol and diesel expenses"
        })
    }

    response = lambda_handler(event, None)
    print(response)