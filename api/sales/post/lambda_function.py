import json
from database import get_connection


def create_sales_api(event, context):

    request_body = json.loads(event["body"])

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # 1️⃣ Insert sales
        sales_query = """
        INSERT INTO sales
        (customer_id, sales_date, status, reference_no, created_by)
        VALUES (%s,%s,%s,%s,%s)
        """

        cursor.execute(sales_query, (
            request_body.get("customer_id"),
            request_body.get("sales_date"),
            request_body.get("status"),
            request_body.get("reference_no"),
            request_body.get("created_by")
        ))

        sale_id = cursor.lastrowid


        # 2️⃣ Insert sale_items
        items = request_body.get("items")

        for item in items:

            item_query = """
            INSERT INTO sale_items
            (sale_id, product_id, quantity, unit_price, discount, tax_amount, total_amount)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """

            cursor.execute(item_query, (
                sale_id,
                item.get("product_id"),
                item.get("quantity"),
                item.get("unit_price"),
                item.get("discount"),
                item.get("tax_amount"),
                item.get("total_amount")
            ))


        # 3️⃣ Insert payment
        payment = request_body.get("payment")

        payment_query = """
        INSERT INTO sales_payments
        (sale_id, payment_date, payment_type, payment_note, amount, created_by)
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(payment_query, (
            sale_id,
            payment.get("payment_date"),
            payment.get("payment_type"),
            payment.get("payment_note"),
            payment.get("amount"),
            payment.get("created_by")
        ))

        conn.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Sale created successfully",
                "sale_id": sale_id
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
    return create_sales_api(event, context)

if __name__ == "__main__":

    import json

    event = {
        "body": json.dumps({
            "customer_id": 1,
            "sales_date": "2026-03-04",
            "status": "completed",
            "reference_no": "INV-1001",
            "created_by": "admin",

            "items": [
                {
                    "product_id": 1,
                    "quantity": 2,
                    "unit_price": 500,
                    "discount": 0,
                    "tax_amount": 50,
                    "total_amount": 1050
                }
            ],

            "payment": {
                "payment_date": "2026-03-04",
                "payment_type": "Cash",
                "payment_note": "Paid",
                "amount": 1050,
                "created_by": 1
            }
        })
    }

    response = create_sales_api(event, None)

    print(response)