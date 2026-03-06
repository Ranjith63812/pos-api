import json
from database import get_connection


def create_employee_attendance_api(event, context):

    request_body = json.loads(event["body"])

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Insert office
        office_query = """
        INSERT INTO office (office_location, office_head)
        VALUES (%s,%s)
        """

        cursor.execute(office_query, (
            request_body.get("office_location"),
            request_body.get("office_head")
        ))

        office_id = cursor.lastrowid


        # Insert employee
        employee_query = """
        INSERT INTO employee (role, location)
        VALUES (%s,%s)
        """

        cursor.execute(employee_query, (
            request_body.get("role"),
            request_body.get("location")
        ))

        emp_id = cursor.lastrowid


        # Insert attendance
        attendance_query = """
        INSERT INTO attendance (office_id, emp_id, status)
        VALUES (%s,%s,%s)
        """

        cursor.execute(attendance_query, (
            office_id,
            emp_id,
            request_body.get("status")
        ))

        conn.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "All records inserted successfully"})
        }

    except Exception as e:
        conn.rollback()
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    finally:
        cursor.close()
        conn.close()
if __name__ == "__main__":

    event = {
        "body": "{\"office_location\":\"Chennai\",\"office_head\":\"Ramesh\",\"role\":\"Developer\",\"location\":\"Chennai\",\"status\":\"Present\"}"
    }

    response = create_employee_attendance_api(event, None)
    print(response)