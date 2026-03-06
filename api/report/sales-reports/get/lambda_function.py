import json
from database import get_connection


def get_sales_report_api(event, context):

    params = event.get("queryStringParameters") or {}

    from_date = params.get("from_date")
    to_date = params.get("to_date")
    customer_id = params.get("customer_id")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        query = """
        SELECT
            s.reference_no AS invoice_number,
            s.sales_date,
            c.id AS customer_id,
            c.customer_name,
            COALESCE(SUM(si.total_amount),0) AS invoice_total,
            COALESCE(SUM(sp.amount),0) AS paid_payment,
            COALESCE(SUM(si.total_amount),0) - COALESCE(SUM(sp.amount),0) AS due_amount,
            DATEDIFF(CURDATE(), s.sales_date) AS due_days
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN sale_items si ON s.id = si.sale_id
        LEFT JOIN sales_payments sp ON s.id = sp.sale_id
        WHERE 1=1
        """

        values = []

        if from_date:
            query += " AND s.sales_date >= %s"
            values.append(from_date)

        if to_date:
            query += " AND s.sales_date <= %s"
            values.append(to_date)

        if customer_id:
            query += " AND s.customer_id = %s"
            values.append(customer_id)

        query += """
        GROUP BY s.id
        ORDER BY s.sales_date DESC
        """

        cursor.execute(query, values)

        result = cursor.fetchall()

        return {
            "statusCode": 200,
            "body": json.dumps(result, default=str)
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    finally:
        cursor.close()
        conn.close()


def lambda_handler(event, context):
    return get_sales_report_api(event, context)

if __name__ == "__main__":

    # Test 1: Fetch all sales reports (no filters)
    event = {
        "queryStringParameters": None
    }

    response = get_sales_report_api(event, None)
    print("All Sales Report:")
    print(response)


    # Test 2: Filter by date range
    event = {
        "queryStringParameters": {
            "from_date": "2026-03-01",
            "to_date": "2026-03-06"
        }
    }

    response = get_sales_report_api(event, None)
    print("\nDate Filter Report:")
    print(response)


    # Test 3: Filter by customer
    event = {
        "queryStringParameters": {
            "customer_id": "1"
        }
    }

    response = get_sales_report_api(event, None)
    print("\nCustomer Filter Report:")
    print(response)