import json
from database import get_connection


def get_sales_payments_report_api(event, context):

    params = event.get("queryStringParameters") or {}

    from_date = params.get("from_date")
    to_date = params.get("to_date")
    customer_id = params.get("customer_id")
    payment_type = params.get("payment_type")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        query = """
        SELECT
            s.reference_no AS invoice_number,
            sp.payment_date,
            c.id AS customer_id,
            c.customer_name,
            sp.payment_type,
            sp.payment_note,
            sp.amount AS paid_payment,
            sp.created_by
        FROM sales_payments sp
        LEFT JOIN sales s ON sp.sale_id = s.id
        LEFT JOIN customers c ON s.customer_id = c.id
        WHERE 1=1
        """

        values = []

        if from_date:
            query += " AND sp.payment_date >= %s"
            values.append(from_date)

        if to_date:
            query += " AND sp.payment_date <= %s"
            values.append(to_date)

        if customer_id:
            query += " AND s.customer_id = %s"
            values.append(customer_id)

        if payment_type:
            query += " AND sp.payment_type = %s"
            values.append(payment_type)

        query += " ORDER BY sp.payment_date DESC"

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
    return get_sales_payments_report_api(event, context)

if __name__ == "__main__":

    # Test 1: Fetch all sales payments
    event = {
        "queryStringParameters": None
    }

    response = get_sales_payments_report_api(event, None)
    print("All Sales Payments Report:")
    print(response)


    # Test 2: Filter by date
    event = {
        "queryStringParameters": {
            "from_date": "2026-03-01",
            "to_date": "2026-03-06"
        }
    }

    response = get_sales_payments_report_api(event, None)
    print("\nDate Filter Payments Report:")
    print(response)


    # Test 3: Filter by customer
    event = {
        "queryStringParameters": {
            "customer_id": "1"
        }
    }

    response = get_sales_payments_report_api(event, None)
    print("\nCustomer Filter Payments Report:")
    print(response)


    # Test 4: Filter by payment type
    event = {
        "queryStringParameters": {
            "payment_type": "Cash"
        }
    }

    response = get_sales_payments_report_api(event, None)
    print("\nPayment Type Filter Report:")
    print(response)