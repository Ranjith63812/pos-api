import json
from database import get_connection


def lambda_handler(event, context):

    try:
        # =====================================
        # ✅ READ BODY SAFELY
        # =====================================
        body = event.get("body") or "{}"
        request_body = json.loads(body)

        expense_id = request_body.get("id")

        if not expense_id:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Expense id required"
                })
            }

        conn = get_connection()
        cursor = conn.cursor()

        # =====================================
        # ✅ CHECK CATEGORY EXISTS
        # =====================================
        cursor.execute(
            "SELECT id FROM expense_categories WHERE id=%s",
            (request_body.get("category_id"),)
        )

        category = cursor.fetchone()

        if not category:
            cursor.close()
            conn.close()

            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Invalid category_id"
                })
            }

        # =====================================
        # ✅ UPDATE EXPENSE
        # =====================================
        query = """
            UPDATE expenses
            SET expense_date=%s,
                category_id=%s,
                reference_no=%s,
                expense_for=%s,
                amount=%s,
                note=%s
            WHERE id=%s
        """

        cursor.execute(
            query,
            (
                request_body.get("expense_date"),
                request_body.get("category_id"),
                request_body.get("reference_no"),
                request_body.get("expense_for"),
                request_body.get("amount"),
                request_body.get("note"),
                expense_id
            )
        )

        conn.commit()

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
                "message": "Expense updated successfully"
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
        "body": json.dumps({
            "id": 1,
            "expense_date": "2026-02-24",
            "category_id": 1,
            "reference_no": "102",
            "expense_for": "Updated Repair",
            "amount": 30000,
            "note": "Updated expense"
        })
    }

    print(lambda_handler(event, None))