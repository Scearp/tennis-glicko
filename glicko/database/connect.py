import sqlalchemy as sql

def create_engine(settings):
    database  = "mysql://{user}:{password}@{host}/tennis"

    database = database.format(user=settings['sql_user'],
                               password=settings['sql_password'],
                               host=settings['sql_host'])

    return sql.create_engine(database)