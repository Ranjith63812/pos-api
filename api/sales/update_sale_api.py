from api.customers.create.database import get_connection


def update_sale_api(request_body):

    if not request_body.get("id"):
        return {
            "statusCode": 400,
            "message": "Sale ID required"
        }

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE sales
        SET
            customer_id = %s,
            sales_date = %s,
            status = %s,
            reference_no = %s
        WHERE id = %s
    """

    cursor.execute(
        query,
        (
            request_body.get("customer_id"),
            request_body.get("sales_date"),
            request_body.get("status"),
            request_body.get("reference_no"),
            request_body.get("id")
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "Sale updated successfully"
    }


# ✅ Local Test
if __name__ == "__main__":

    request = {
        "id": 1,
        "customer_id": 2,
        "sales_date": "2026-02-24",
        "status": "Quotation",
        "reference_no": "SL001-UPDATED"
    }

    print(update_sale_api(request))