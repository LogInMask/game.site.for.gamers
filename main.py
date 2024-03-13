from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db_scripts import *
import uuid

app = Flask(__name__)

@app.route("/")
def index():
    games = get_all_games()

    if "AUTH" not in session:
        return render_template("index.html", games=games)

    else:
        return render_template("index_registered.html", games=games)

@app.route("/user/edit", methods=["POST", "GET"])
def edit_user():

    user = get_user_by_id(user_id=str(session['user_id']))

    if request.method == "POST":
        update_user(str(session['user_id']), request.form['new_fn'], request.form['new_ln'], request.form['new_un'])

        return redirect(url_for('index'))

    return render_template('user_edit.html', user=user)

@app.route("/user/edit/confirm")
def confirm_changes():
    return redirect('/user')

@app.route("/post/game/<game_name>")
def cur_game_page(game_name):
    versions = get_all_versions()

    return render_template("game_page.html", game_name=game_name, versions=versions)

@app.route("/post/game/<game_name>/version/<version_name>")
def cur_version_page(game_name, version_name):
    version = get_ver_by_name(version_name)

    return render_template("version_page.html", game_name=game_name, version_name=version_name, version=version)

@app.route("/post/new_version", methods=["POST", "GET"])
def post_version():

    if request.method == "POST":
        create_version(request.form['game'], request.form['version_name'], request.form['version_desc'], str(uuid.uuid4()), request.form['story'], request.form['gameplay'],
                       download_link1=request.form['download_link1'], download_link2=request.form['download_link2'], download_link3=request.form['download_link3'])

    return render_template("new_version_post.html")

@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for('index'))

@app.route("/user")
def user_page():

    user = get_user_by_id(user_id=str(session['user_id']))

    return render_template("user_page.html", user=user)

@app.route("/registration", methods=["GET", "POST"])
def reg():
    if "AUTH" not in session:
        errors = []

        userid = uuid.uuid4()

        if request.method == "POST":

            if len(request.form['username']) >= 8 and len(request.form['password']) >= 8 and request.form['email'] != "" and request.form['password'] != "" and request.form['username'] != "":
                pswd_hash = generate_password_hash(request.form['password'])
                user = create_user(request.form['first_name'], request.form['last_name'], str(userid), "@" + request.form['username'], str(pswd_hash), request.form['email'])

                if user:
                    flash("Successfully registered!")
                    return redirect(url_for("login"))
                else:
                    errors.append("ERROR CODE #308")
                    print(errors[0])

            else:
                errors.append("ERROR CODE #307")
                print(errors[0])

        return render_template("registration.html")

    else:
        return redirect(url_for('index'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "AUTH" not in session:
        errors = []

        if request.method == "POST":
            if request.form['email'] != "":
                user = get_user_by_email(request.form['email'])
                if user:
                    if request.form['password'] != "" and check_password_hash(user['PASSWORD'], request.form['password']):
                        session["AUTH"] = True
                        session["user_id"] = user['ID']
                        return redirect(url_for('index'))
                    else:
                        errors.append("Wrong password!")

                else:
                    errors.append("It seems like there's no user found in database with this email")

            else:
                errors.append("Email can't be empty!")

        return render_template("login.html", errors=errors)

    else:
        return redirect(url_for("index"))

@app.route("/post/new_game", methods=["POST", "GET"])
def create_game_post():
    if request.method == "POST":
        create_game(request.form['game_name'], request.form['game_desc'], request.form['image_url'], request.form['game_dev'], str(uuid.uuid4()))

    return render_template("new_game_post.html")

@app.route("/about")
def about():
    if "AUTH" not in session:
        return render_template("about.html")

    else:
        return render_template("about_registered.html")

if __name__ == '__main__':
    app.secret_key = 'THE SUPER SECRET KEY'
    app.run(host='0.0.0.0', port=5000, debug=True)