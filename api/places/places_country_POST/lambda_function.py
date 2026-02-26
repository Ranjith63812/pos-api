import json
from database import get_connection


def lambda_handler(event, context):

    try:
        body = json.loads(event.get("body", "{}"))

        if not body.get("country_name"):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Country name required"
                })
            }

        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO countries (country_name)
            VALUES (%s)
        """

        cursor.execute(
            query,
            (body.get("country_name"),)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Country created successfully"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }

# ✅ LOCAL LAMBDA TEST
# ===============================
if __name__ == "__main__":

    event = {
        "body": json.dumps({
            "country_name": "Brazil"
        })
    }

    response = lambda_handler(event, None)

    print(response)