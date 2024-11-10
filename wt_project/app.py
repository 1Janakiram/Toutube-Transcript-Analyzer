from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

from project import extract_keywords,get_videos,get_transcript,get_video_title

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///main.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/', methods=["GET", "POST"])
def main():

     return render_template("login-signup.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
     if request.method == "POST":

         username_ = request.form.get("name")
         password_ = request.form.get("password")
         print(username_)
         if not request.form.get("name"):
              pass
         else:
             opass = db.execute("SELECT username FROM users WHERE username=?",username_)
             if not opass:
                 print("23")
                 return render_template("login-signup.html",msg="Incorrect Username")

             opass = db.execute("SELECT password FROM users WHERE username=?",username_)
             print(opass[0]["password"],password_,"if")

             if opass[0]["password"] == password_:
                 print(opass,password_,"if")
                 #session["user_id"] = opass[0]["id"]
                 return render_template("home.html")
             else:
                 print(opass,password_,"else")
                 return render_template("login-signup.html",msg="Incorrect password")

         username = request.form.get("name1")
         password = request.form.get("pass1")
         print(username,password)
         print("vdf")

         rows = db.execute("SELECT * FROM users WHERE username = ?", username)

         if (len(rows) != 0):
            return render_template("login-signup.html",msg="The username already exists.")


         db.execute("INSERT INTO users(username,password) VALUES(?,?)",username, password)
         return redirect("/")


     else:
         print("else")
         return render_template("login-signup.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form.get("query")
        print(query)
        sub={}


        try:
            keywords = extract_keywords(query)
            vid_id = get_videos(query)
            for i in range(0, len(vid_id)):
                i+=1

                id = vid_id[i]
                responses = get_transcript(id)

                if (responses["is_available"] == True and responses["lang"] == "en"):
                    print()
                    title = get_video_title(id)
                    print(title)
                    print("\n\n")

                    subtitles = responses["subtitles"]
                    video_subtitles = []
                    for part in subtitles:

                        if any(words in part['text'] for words in keywords) or any(words in part['text'].lower() for words in keywords):
                            text = f"{part['text']} at {part['start']}s"
                            line = f"https://www.youtube.com/watch?v={id}&t={part['start']}s"
                            video_subtitles.append(line)

                    sub[id] = video_subtitles
                    print()

                else:
                    continue
            return render_template("result.html",subtitle=sub,vid_name=title)
        except:
             print("Something else went wrong")

    else:

         return render_template("home.html")


