from peewee import Model, CharField, DateTimeField, PostgresqlDatabase, BigIntegerField

from config import DB_NAME, DB_HOST, DB_PASSWORD, DB_PORT, DB_USERNAME

db = PostgresqlDatabase(database=DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USERNAME, password=DB_PASSWORD)

class User(Model):
    chat_id = BigIntegerField()
    username = CharField()
    first_name = CharField(default='Without first name', null=True)
    apply_time = DateTimeField(null=True)

    class Meta:
        database = db

if __name__ == '__main__':
    db.connect()
    db.create_tables([User])

