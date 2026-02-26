import json
from database import get_connection


def lambda_handler(event, context):

    try:
        query_params = event.get("queryStringParameters")

        conn = get_connection()
        cursor = conn.cursor()

        # ---------- Fetch By ID ----------
        if query_params and query_params.get("id"):

            query = """
                SELECT id, country_name, status
                FROM countries
                WHERE id=%s
            """

            cursor.execute(
                query,
                (query_params.get("id"),)
            )

            data = cursor.fetchone()

        # ---------- Fetch All ----------
        else:

            query = """
                SELECT id, country_name, status
                FROM countries
                ORDER BY id DESC
            """

            cursor.execute(query)
            data = cursor.fetchall()

        cursor.close()
        conn.close()

        return {
            "statusCode": 200,
            "body": json.dumps(data)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }
    
if __name__ == "__main__":

    # Fetch all countries
    event = {
        "queryStringParameters": None
    }

    print(lambda_handler(event, None))


    # Fetch by ID
    event = {
        "queryStringParameters": {
            "id": "1"
        }
    }

    print(lambda_handler(event, None))