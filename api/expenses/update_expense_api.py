from api.customers.create.database import get_connection


def update_expense_api(request_body):

    if not request_body.get("id"):
        return {
            "statusCode": 400,
            "message": "Expense id required"
        }

    conn = get_connection()
    cursor = conn.cursor()

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
            request_body.get("id")
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "Expense updated successfully"
    }


# ✅ Local Test
if __name__ == "__main__":

    request = {
        "id": 1,
        "expense_date": "2026-02-24",
        "category_id": 1,
        "reference_no": "102",
        "expense_for": "Updated Repair",
        "amount": 300,
        "note": "Updated expense"
    }

    print(update_expense_api(request))