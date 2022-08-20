import sqlalchemy as sql

import database as db

import json
import sys

def add_index(engine, name, column):
    index_command = "create index {index} on {tour}_match ({column});"

    index = index_command.format(index=name,
                                 tour=sys.argv[1],
                                 column=column)

    engine.execute(index)

def main():
    with open("./glicko/config.json") as cfg:
        config = json.load(cfg)

    columns = [" ".join(t) for t in zip(config['columns'], config['datatypes'])]
    columns = ", ".join(columns)

    init_command = ("create table {tour}_match "
                   "({c}, primary key (match_id));".format(tour=sys.argv[1],
                                                           c=columns))

    with open("./settings.json") as cfg:
        settings = json.load(cfg)

    engine = db.create_engine(settings)
    engine.execute(init_command)

    add_index(engine, "date", "tourney_date")
    add_index(engine, "name", "tourney_name")

if __name__ == "__main__":
    main()