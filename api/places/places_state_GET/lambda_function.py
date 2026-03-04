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
                SELECT 
                    s.id,
                    s.state_name,
                    s.country_id,
                    c.country_name
                FROM states s
                JOIN countries c
                    ON s.country_id = c.id
                WHERE s.id=%s
            """

            cursor.execute(
                query,
                (query_params.get("id"),)
            )

            result = cursor.fetchone()
            data = [result] if result else []

        # ---------- Fetch All ----------
        else:

            query = """
                SELECT 
                    s.id,
                    s.state_name,
                    s.country_id,
                    c.country_name
                FROM states s
                JOIN countries c
                    ON s.country_id = c.id
                ORDER BY s.id DESC
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

    # Fetch all states
    event = {
        "queryStringParameters": None
    }

    print(lambda_handler(event, None))

    # Fetch by ID
    event = {
        "queryStringParameters": {
            "id": "3"
        }
    }

    print(lambda_handler(event, None))