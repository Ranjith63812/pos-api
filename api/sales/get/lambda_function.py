import json
from database import get_connection


def get_sales_api(event, context):

    params = event.get("queryStringParameters")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        if params and params.get("id"):

            query = """
            SELECT
                s.id AS sale_id,
                s.customer_id,
                s.sales_date,
                s.status,
                s.reference_no,
                p.product_name,
                si.quantity,
                si.unit_price,
                si.total_amount,
                sp.payment_type,
                sp.amount
            FROM sales s
            LEFT JOIN sale_items si ON s.id = si.sale_id
            LEFT JOIN products p ON si.product_id = p.id
            LEFT JOIN sales_payments sp ON s.id = sp.sale_id
            WHERE s.id = %s
            """

            cursor.execute(query, (params.get("id"),))
            result = cursor.fetchall()

        else:

            query = """
            SELECT
                s.id AS sale_id,
                s.customer_id,
                s.sales_date,
                s.status,
                s.reference_no,
                p.product_name,
                si.quantity,
                si.unit_price,
                si.total_amount,
                sp.payment_type,
                sp.amount
            FROM sales s
            LEFT JOIN sale_items si ON s.id = si.sale_id
            LEFT JOIN products p ON si.product_id = p.id
            LEFT JOIN sales_payments sp ON s.id = sp.sale_id
            ORDER BY s.id DESC
            """

            cursor.execute(query)
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
    return get_sales_api(event, context)

if __name__ == "__main__":

    # Test: Fetch all sales
    event = {
        "queryStringParameters": None
    }

    response = get_sales_api(event, None)
    print("Fetch All Sales:")
    print(response)


    # Test: Fetch sale by id
    event = {
        "queryStringParameters": {
            "id": "6"
        }
    }

    response = get_sales_api(event, None)
    print("\nFetch Sale By ID:")
    print(response)