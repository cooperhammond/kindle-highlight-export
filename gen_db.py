import os
from app import db, create_app

print("WARNING: This will delete your current database and generate a new one. Do you want to continue? Y/n ")
answer = str(input())

if answer == "n":
    exit()

os.remove("app/db.sqlite")
db.create_all(app=create_app())