import json
from database import get_connection


def delete_sales_api(event, context):

    params = event.get("queryStringParameters")

    if not params or not params.get("id"):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Sale id required"})
        }

    sale_id = params.get("id")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # Delete sale_items first
        query = "DELETE FROM sale_items WHERE sale_id=%s"
        cursor.execute(query, (sale_id,))

        # Delete payments
        query = "DELETE FROM sales_payments WHERE sale_id=%s"
        cursor.execute(query, (sale_id,))

        # Delete sale
        query = "DELETE FROM sales WHERE id=%s"
        cursor.execute(query, (sale_id,))

        conn.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Sale deleted successfully"
            })
        }

    except Exception as e:

        conn.rollback()

        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    finally:
        cursor.close()
        conn.close()


def lambda_handler(event, context):
    return delete_sales_api(event, context)