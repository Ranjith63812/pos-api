import json
from database import get_connection


def lambda_handler(event, context):

    conn = get_connection()
    cursor = conn.cursor()

    # ✅ safely read query param
    category_id = (
        event.get("queryStringParameters", {}) or {}
    ).get("id")

    # =====================================
    # ✅ GET BY ID
    # =====================================
    if category_id:

        query = """
            SELECT id, category_name, description, status
            FROM expense_categories
            WHERE id = %s
        """

        cursor.execute(query, (category_id,))
        data = cursor.fetchone()

        if not data:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": "Category not found"
                })
            }

    # =====================================
    # ✅ GET ALL
    # =====================================
    else:

        query = """
            SELECT id, category_name, description, status
            FROM expense_categories
        """

        cursor.execute(query)
        data = cursor.fetchall()

    cursor.close()
    conn.close()

    # ✅ Proper structured response
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "success": True,
            "data": data
        }, default=str)
    }


# =====================================
# ✅ LOCAL TEST
# =====================================
if __name__ == "__main__":

    print("\nGET ALL")
    event_all = {"queryStringParameters": None}
    print(lambda_handler(event_all, None))

    print("\nGET BY ID")
    event_id = {"queryStringParameters": {"id": "2"}}
    print(lambda_handler(event_id, None))