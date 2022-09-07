from backend import db

if input("Rest Database? (y/n) >> ") == "y":
    db.create_all()
    print("done")
else:
    print("aborted")