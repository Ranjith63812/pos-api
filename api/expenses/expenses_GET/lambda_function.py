import json
from database import get_connection


def lambda_handler(event, context):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # =====================================
        # ✅ READ QUERY PARAM
        # =====================================
        params = event.get("queryStringParameters") or {}
        expense_id = params.get("id")

        # =====================================
        # ✅ GET BY ID
        # =====================================
        if expense_id:

            query = """
                SELECT
                    e.id,
                    e.expense_date,
                    c.category_name,
                    e.reference_no,
                    e.expense_for,
                    e.amount,
                    e.note,
                    e.created_by
                FROM expenses e
                JOIN expense_categories c
                    ON e.category_id = c.id
                WHERE e.id=%s
            """

            cursor.execute(query, (expense_id,))
            data = cursor.fetchone()

            if not data:
                cursor.close()
                conn.close()

                return {
                    "statusCode": 404,
                    "body": json.dumps({
                        "message": "Expense not found"
                    })
                }

        # =====================================
        # ✅ GET ALL
        # =====================================
        else:

            query = """
                SELECT
                    e.id,
                    e.expense_date,
                    c.category_name,
                    e.reference_no,
                    e.expense_for,
                    e.amount,
                    e.note,
                    e.created_by
                FROM expenses e
                JOIN expense_categories c
                    ON e.category_id = c.id
                ORDER BY e.id DESC
            """

            cursor.execute(query)
            data = cursor.fetchall()

        cursor.close()
        conn.close()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "data": data
            }, default=str)
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

    # ✅ TEST ALL
    event_all = {
        "queryStringParameters": None
    }

    print("\nGET ALL:")
    print(lambda_handler(event_all, None))

    # ✅ TEST BY ID
    event_id = {
        "queryStringParameters": {
            "id": "1"
        }
    }

    print("\nGET BY ID:")
    print(lambda_handler(event_id, None))