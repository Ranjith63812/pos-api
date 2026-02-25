import json
from database import get_connection


def lambda_handler(event, context):

    try:
        params = event.get("queryStringParameters") or {}
        category_id = params.get("id")

        if not category_id:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Category id required"
                })
            }

        conn = get_connection()
        cursor = conn.cursor()

        # ✅ CHECK USAGE
        cursor.execute(
            "SELECT COUNT(*) AS total FROM expenses WHERE category_id=%s",
            (category_id,)
        )

        result = cursor.fetchone()
        usage_count = result["total"]   # ✅ FIX

        if usage_count > 0:
            cursor.close()
            conn.close()

            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Category already used in expenses"
                })
            }

        # ✅ DELETE
        cursor.execute(
            "DELETE FROM expense_categories WHERE id=%s",
            (category_id,)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Category deleted successfully"
            })
        }

    except Exception as e:
        print("ERROR:", str(e))

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal server error",
                "error": str(e)
            })
        }