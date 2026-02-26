import json
from database import get_connection


def lambda_handler(event, context):

    try:
        query_params = event.get("queryStringParameters")
        body = json.loads(event.get("body", "{}"))

        # ---------- Validation ----------
        if not query_params or not query_params.get("id"):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Country id required"
                })
            }

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
            UPDATE countries
            SET country_name=%s
            WHERE id=%s
        """

        cursor.execute(
            query,
            (
                body.get("country_name"),
                query_params.get("id")
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Country updated successfully"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }
    
if __name__ == "__main__":

    event = {
        "queryStringParameters": {
            "id": "1"
        },
        "body": json.dumps({
            "country_name": "India Updated"
        })
    }

    print(lambda_handler(event, None))