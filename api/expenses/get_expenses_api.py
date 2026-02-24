from api.customers.create.database import get_connection


def get_expenses_api():

    conn = get_connection()
    cursor = conn.cursor()

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

    expenses = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "data": expenses
    }


# ✅ Local Test
if __name__ == "__main__":
    print(get_expenses_api())