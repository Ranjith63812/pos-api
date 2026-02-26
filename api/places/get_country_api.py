from api.customers.create.database import get_connection


def get_country_api(query_params=None):

    conn = get_connection()
    cursor = conn.cursor()

    # ---------- Fetch By ID ----------
    if query_params and query_params.get("id"):

        query = """
            SELECT id, country_name, status
            FROM countries
            WHERE id=%s
        """

        cursor.execute(query, (query_params.get("id"),))
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
        "data": data
    }


# Local testing
if __name__ == "__main__":
    print(get_country_api())


if __name__ == "__main__":

    query = {"id": 1}

    print(get_country_api(query))