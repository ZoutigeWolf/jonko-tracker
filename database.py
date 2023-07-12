import os
import sys
import json
import sqlite3
#from sql_database_zoutigewolf.database import Database

def loadData(file_name: str) -> dict[str]:
    with open(os.path.join(sys.path[0], file_name), "r") as f:
        return json.load(f)


config = loadData("config.json")
#database = Database(**config["db_credentials"])
database = sqlite3.connect("database.db", check_same_thread=False)
