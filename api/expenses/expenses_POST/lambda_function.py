import json
from database import get_connection


def lambda_handler(event, context):

    try:
        # =====================================
        # ✅ READ BODY SAFELY
        # =====================================
        body = event.get("body") or "{}"
        request_body = json.loads(body)

        # =====================================
        # ✅ REQUIRED FIELD VALIDATION
        # =====================================
        required_fields = [
            "expense_date",
            "category_id",
            "expense_for",
            "amount"
        ]

        for field in required_fields:
            if not request_body.get(field):
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "message": f"{field} is required"
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
        # ✅ INSERT EXPENSE
        # =====================================
        query = """
            INSERT INTO expenses
            (
                expense_date,
                category_id,
                reference_no,
                expense_for,
                amount,
                note,
                created_by
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
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
                request_body.get("created_by")
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Expense created successfully"
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
            "expense_date": "2026-02-25",
            "category_id": 2,
            "reference_no": "101",
            "expense_for": "Vehicle Repair",
            "amount": 200,
            "note": "Repairing vehicle",
            "created_by": "Admin"
        })
    }

    print(lambda_handler(event, None))