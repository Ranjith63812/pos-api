import json
from database import get_connection


def lambda_handler(event, context):

    body = json.loads(event.get("body", "{}"))

    customer_id = body.get("id")

    if not customer_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Customer ID required"})
        }

    conn = get_connection()
    cursor = conn.cursor()

    # remove id from update fields
    body.pop("id")

    update_fields = []
    values = []

    for key, value in body.items():
        update_fields.append(f"{key}=%s")
        values.append(value)

    values.append(customer_id)

    query = f"""
        UPDATE customers
        SET {', '.join(update_fields)}
        WHERE id=%s
    """

    cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Customer updated successfully"
        })
    }