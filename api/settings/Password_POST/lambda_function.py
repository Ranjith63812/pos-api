import json
from database import get_connection


def lambda_handler(event, context):

    try:
        body = json.loads(event.get("body", "{}"))

        # ---------- Validation ----------
        if not body.get("username"):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Username required"
                })
            }

        if not body.get("current_password"):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Current password required"
                })
            }

        if not body.get("new_password"):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "New password required"
                })
            }

        if not body.get("confirm_password"):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Confirm password required"
                })
            }

        if body.get("new_password") != body.get("confirm_password"):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Passwords do not match"
                })
            }

        conn = get_connection()
        cursor = conn.cursor()

        # ---------- Check Current Password ----------
        query = """
            SELECT password
            FROM users
            WHERE username=%s
        """

        cursor.execute(query, (body.get("username"),))
        result = cursor.fetchone()

        if not result:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": "User not found"
                })
            }

        db_password = result["password"]

        if db_password != body.get("current_password"):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Current password incorrect"
                })
            }

        # ---------- Update Password ----------
        update_query = """
            UPDATE users
            SET password=%s
            WHERE username=%s
        """

        cursor.execute(
            update_query,
            (
                body.get("new_password"),
                body.get("username")
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Password updated successfully"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }