from api.customers.create.database import get_connection


def delete_expense_api(request_body):

    if not request_body.get("id"):
        return {
            "statusCode": 400,
            "message": "Expense id required"
        }

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM expenses WHERE id=%s"

    cursor.execute(query, (request_body.get("id"),))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "Expense deleted successfully"
    }


# ✅ Local Test
if __name__ == "__main__":

    request = {
        "id": 1
    }

    print(delete_expense_api(request))