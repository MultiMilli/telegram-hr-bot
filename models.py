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
db = PostgresqlDatabase('d5sna531o243jj', host='ec2-52-48-159-67.eu-west-1.compute.amazonaws.com', user='icazpuovmxnozv', password='f03cb7e3020bf87efaa7d5c54387cd266cd9e37a6bfc67dd3a335d5cc8c28f9e', port=5432)

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


