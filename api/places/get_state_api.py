from api.customers.create.database import get_connection


def get_states_api(query_params=None):

    conn = get_connection()
    cursor = conn.cursor()

    # ---------- Fetch By ID ----------
    if query_params and query_params.get("id"):

        query = """
            SELECT 
                s.id,
                s.state_name,
                c.country_name
            FROM states s
            JOIN countries c
                ON s.country_id = c.id
            WHERE s.id=%s
        """

        cursor.execute(query, (query_params.get("id"),))
        result = cursor.fetchone()
        data = [result] if result else []

    # ---------- Fetch All ----------
    else:

        query = """
            SELECT 
                s.id,
                s.state_name,
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
        "data": data
    }


# Local Test
if __name__ == "__main__":
    print(get_states_api())