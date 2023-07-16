import os
import sys
import json
from sql_database_zoutigewolf.database import Database


def load_data(file_name: str) -> dict[str]:
    with open(os.path.join(sys.path[0], file_name), "r") as f:
        return json.load(f)


config = load_data("config.json")
database = Database(**config["db_credentials"])
