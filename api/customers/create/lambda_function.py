import json
from database import get_connection


def lambda_handler(event, context):

    request_body = json.loads(event.get("body", "{}"))

    # Mandatory validation
    if not request_body.get("customer_name"):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Customer name required"})
        }

    if not request_body.get("mobile"):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Mobile required"})
        }

    if not request_body.get("email"):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Email required"})
        }

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO customers
        (customer_name, mobile, email, phone, gst_number, tax_number, previous_due,
        city, postcode, address, country_id, state_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            request_body.get("customer_name"),
            request_body.get("mobile"),
            request_body.get("email"),
            request_body.get("phone", ""),
            request_body.get("gst_number", ""),
            request_body.get("tax_number", ""),
            request_body.get("previous_due", 0),
            request_body.get("city", ""),
            request_body.get("postcode", ""),
            request_body.get("address", ""),
            request_body.get("country_id"),
            request_body.get("state_id")
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Customer created successfully"
        })
    }


# Local testing
if __name__ == "__main__":

    event = {
        "body": json.dumps({
            "customer_name": "Ranjith Kumar",
            "mobile": "9876543210",
            "email": "ranjith@test.com",
            "phone": "9876543210",
            "gst_number": "22AAAAA0000A1Z5",
            "tax_number": "TX12345",
            "previous_due": 0,
            "city": "Chennai",
            "postcode": "600001",
            "address": "Anna Nagar",
            "country_id": 1,
            "state_id": 3
        })
    }

    response = lambda_handler(event, None)

    print(response)