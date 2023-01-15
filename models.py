from peewee import SqliteDatabase, Model, CharField, DateTimeField, PostgresqlDatabase
# import psycopg2
# from config import USERNAME, PASSWORD

# try:
#     conn = psycopg2.connect(
#         database="applicant",
#         host="localhost",
#         port='5432',
#         user=USERNAME,
#         password=PASSWORD)
# except Exception as _ex:
#     print("[INFO] Error when connection to PostgreSQL", _ex)
# finally:
#     if conn:
#         conn.close()
#         print("[INFO] PostgreSQL connection closed")


# # db = SqliteDatabase('applicants') #Test bot on SQLite
# db = PostgresqlDatabase('applicant', host='localhost', port=5432, user=USERNAME, password=PASSWORD)
db = PostgresqlDatabase('dmfe7joaqij2r', host='ec2-99-80-170-190.eu-west-1.compute.amazonaws.com', user='xsoisbziozhtuu', password='4db2c19a091e426ad2091e7ee07457662dcc0235f683a8a46e22e7bb36bd7eb7', port=5432)

class User(Model):
    chat_id = CharField()
    username = CharField()
    first_name = CharField(default='Without first name', null=True)
    apply_time = DateTimeField(null=True)

    class Meta:
        database = db

# db.connect()

if __name__ == '__main__':
    db.connect()
    db.create_tables([User])
else:
    db.connect()


