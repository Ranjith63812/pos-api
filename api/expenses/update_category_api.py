from api.customers.create.database import get_connection


def update_category_api(request_body):

    if not request_body.get("id"):
        return {"statusCode": 400, "message": "Category id required"}

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE expense_categories
        SET category_name=%s,
            description=%s
        WHERE id=%s
    """

    cursor.execute(
        query,
        (
            request_body.get("category_name"),
            request_body.get("description"),
            request_body.get("id")
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "Category updated successfully"
    }


if __name__ == "__main__":

    request = {
        "id": 1,
        "category_name": "Fuel",
        "description": "Updated category"
    }

    print(update_category_api(request))