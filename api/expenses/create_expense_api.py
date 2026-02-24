from api.customers.create.database import get_connection


def create_expense_api(request_body):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO expenses
        (expense_date, category_id, reference_no,
         expense_for, amount, note, created_by)
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
        "message": "Expense created successfully"
    }


# ✅ Local Test
if __name__ == "__main__":

    request = {
        "expense_date": "2026-02-23",
        "category_id": 1,
        "reference_no": "101",
        "expense_for": "Vehicle Repair",
        "amount": 200,
        "note": "Repairing vehicle",
        "created_by": "Admin"
    }

    print(create_expense_api(request))