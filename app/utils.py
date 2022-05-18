from app import database


def logged(host):
    user = database.sql_execute(f"SELECT users_id FROM ip_user WHERE ip='{host}'")
    if user:
        return database.sql_execute(f'SELECT * FROM users WHERE id={user[0][0]}')
    else:
        return False
