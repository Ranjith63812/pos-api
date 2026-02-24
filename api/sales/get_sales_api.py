from api.customers.create.database import get_connection


def get_sales_api():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            s.id,
            c.customer_name,
            s.sales_date,
            s.status,
            s.reference_no,
            s.created_by
        FROM sales s
        JOIN customers c
        ON s.customer_id = c.id
        ORDER BY s.id DESC
    """

    cursor.execute(query)

    sales = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "data": sales
    }


# Local test
if __name__ == "__main__":
    print(get_sales_api())