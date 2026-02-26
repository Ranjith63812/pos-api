from api.customers.create.database import get_connection


def create_country_api(request_body):

    if not request_body.get("country_name"):
        return {
            "statusCode": 400,
            "message": "Country name required"
        }

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO countries (country_name, status)
    VALUES (%s, %s)
"""
    

    cursor.execute(
    query,
    (
        request_body.get("country_name"),
        "Active"
    )
)

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "message": "Country added successfully"
    }


if __name__ == "__main__":

    request = {
        "country_name": "India"
    }

    print(create_country_api(request))