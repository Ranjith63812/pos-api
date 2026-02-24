from api.customers.create.database import get_connection


def get_categories_api():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, category_name, description, status
        FROM expense_categories
    """

    cursor.execute(query)

    categories = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "data": categories
    }


# ✅ Local test
if __name__ == "__main__":
    print(get_categories_api())