import json
from database import get_connection


def lambda_handler(event, context):

    # ✅ Read body from API Gateway
    request_body = json.loads(event.get("body", "{}"))

    # ✅ Validation
    if not request_body.get("id"):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Category id required"
            })
        }

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE expense_categories
        SET category_name=%s,
            description=%s
        WHERE id=%s
    """

    cursor.execute(
        query,
        (
            request_body.get("category_name"),
            request_body.get("description"),
            request_body.get("id")
        )
    )

    conn.commit()

    # ✅ Check record updated or not
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()

        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "Category not found"
            })
        }

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Category updated successfully"
        })
    }


# ==================================================
# ✅ LOCAL TEST (VS CODE)
# ==================================================
if __name__ == "__main__":

    event = {
        "body": json.dumps({
            "id": 1,
            "category_name": "Office Vehicle",
            "description": "Expense on Vehicle"
        })
    }

    print(lambda_handler(event, None))