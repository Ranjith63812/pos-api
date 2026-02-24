from api.customers.create.database import get_connection


def delete_sale_api(request_body):

    if not request_body.get("id"):
        return {
            "statusCode": 400,
            "message": "Sale ID required"
        }

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM sales WHERE id = %s"

    cursor.execute(query, (request_body.get("id"),))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "Sale deleted successfully"
    }


# ✅ Local Test
if __name__ == "__main__":

    request = {
        "id": 1
    }

    print(delete_sale_api(request))