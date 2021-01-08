import os
from app import db, create_app

answer = str(input("WARNING: This will delete your current database and generate a new one. Do you want to continue? Y/n "))

if answer == "n":
    exit()

try:
    os.remove("app/db.sqlite")
except:
    pass
db.create_all(app=create_app())