import mysql.connector


def connect():
   return mysql.connector.connect(
       host='',
       user='root',
       password=''
   )


def sql_execute(sql):
    db = connect()
    with db.cursor() as cursor:
        cursor.execute('USE starlette;')
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
    return result