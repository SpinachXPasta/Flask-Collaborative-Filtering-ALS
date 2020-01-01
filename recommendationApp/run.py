from startup import create_app,db
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = create_app()

def check_create():
    if "Main.db" not in os.listdir():
        print ("createing db")
        db.create_all(app=create_app())

def check_deb():
    db.create_all(app=create_app())

if __name__ == "__main__":
 check_create()
 check_deb()
 app.run(debug=True, threaded=True)
