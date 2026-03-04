import json
from database import get_connection


def lambda_handler(event, context):

    try:
        query_params = event.get("queryStringParameters")

        # ---------- Validation ----------
        if not query_params or not query_params.get("id"):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "State id required"
                })
            }

        conn = get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM states WHERE id=%s"

        cursor.execute(
            query,
            (query_params.get("id"),)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "State deleted successfully"
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
            "id": "3"
        }
    }

    print(lambda_handler(event, None))