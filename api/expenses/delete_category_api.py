from api.customers.create.database import get_connection


def delete_category_api(request_body):

    if not request_body.get("id"):
        return {"statusCode": 400, "message": "Category id required"}

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM expense_categories WHERE id=%s"

    cursor.execute(query, (request_body.get("id"),))
    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "Category deleted successfully"
    }


if __name__ == "__main__":

    request = {"id": 1}

    print(delete_category_api(request))