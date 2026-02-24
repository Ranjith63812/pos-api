from api.customers.create.database import get_connection


def create_sale_api(request_body):

    # Basic validation
    if not request_body.get("customer_id"):
        return {
            "statusCode": 400,
            "message": "Customer is required"
        }

    if not request_body.get("sales_date"):
        return {
            "statusCode": 400,
            "message": "Sales date is required"
        }

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO sales
        (customer_id, sales_date, status,
         reference_no, created_by)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            request_body.get("customer_id"),
            request_body.get("sales_date"),
            request_body.get("status"),
            request_body.get("reference_no"),
            request_body.get("created_by")
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "Sale created successfully"
    }


# Local testing
if __name__ == "__main__":

    request = {
    "customer_id": 3,
    "sales_date": "2026-02-24",
    "status": "Final",
    "reference_no": "SL003",
    "created_by": "Admin"
}

    print(create_sale_api(request))