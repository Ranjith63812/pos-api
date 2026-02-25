import json
from database import get_connection


def lambda_handler(event, context):

    try:
        # =====================================
        # ✅ READ QUERY PARAMETER
        # =====================================
        params = event.get("queryStringParameters") or {}
        expense_id = params.get("id")

        if not expense_id:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Expense id required"
                })
            }

        conn = get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM expenses WHERE id=%s"

        cursor.execute(query, (expense_id,))
        conn.commit()

        # ✅ Check record exists
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()

            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": "Expense not found"
                })
            }

        cursor.close()
        conn.close()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Expense deleted successfully"
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


# =====================================
# ✅ LOCAL TEST (VS CODE)
# =====================================
if __name__ == "__main__":

    event = {
        "queryStringParameters": {
            "id": "1"
        }
    }

    print(lambda_handler(event, None))