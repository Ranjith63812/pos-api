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
                    "message": "State id required"
                })
            }

        if not body.get("state_name"):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "State name required"
                })
            }

        if not body.get("country_id"):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Country required"
                })
            }

        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE states
            SET state_name=%s,
                country_id=%s
            WHERE id=%s
        """

        cursor.execute(
            query,
            (
                body.get("state_name"),
                body.get("country_id"),
                query_params.get("id")
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "State updated successfully"
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
            "id": "4"
        },
        "body": json.dumps({
            "state_name": "Kerala Updated",
            "country_id": 3
        })
    }

    print(lambda_handler(event, None))