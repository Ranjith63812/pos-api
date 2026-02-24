from api.customers.create.database import get_connection


def create_category_api(request_body):

    if not request_body.get("category_name"):
        return {
            "statusCode": 400,
            "message": "Category name required"
        }

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO expense_categories
        (category_name, description)
        VALUES (%s, %s)
    """

    cursor.execute(
        query,
        (
            request_body.get("category_name"),
            request_body.get("description")
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "Category created successfully"
    }


# ✅ Local Test
if __name__ == "__main__":

    request = {
        "category_name": "Petrol",
        "description": "Fuel expenses"
    }

    print(create_category_api(request))