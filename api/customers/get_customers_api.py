from api.customers.create.database import get_connection


def get_customers_api():

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM customers"

    cursor.execute(query)

    customers = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "data": customers
    }


# local test
if __name__ == "__main__":
    response = get_customers_api()
    print(response)