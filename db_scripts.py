import sqlite3


def open_connection():
    connection = sqlite3.connect("site_db.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_user(first_name, last_name, user_id, username, password_hash, email):
    connection = open_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO USERS (FIRST_NAME, LAST_NAME, PASSWORD, USERNAME, ID, EMAIL) VALUES (?, ?, ?, ?, ?, ?)",
                       (first_name, last_name, password_hash, username, user_id, email))
        connection.commit()
        cursor.close()
        connection.close()

        return True

    except:
        return False

def get_user_by_id(user_id):
    connection = open_connection()
    cursor = connection.cursor()
    user = cursor.execute("SELECT * FROM USERS WHERE ID = ?", [user_id]).fetchone()
    cursor.close()
    connection.close()
    return user

def update_user(user_id, new_first_name, new_last_name, new_username):
    connection = open_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE USERS SET FIRST_NAME = (?), LAST_NAME = (?), USERNAME = (?) WHERE ID = (?)", (new_first_name, new_last_name, new_username, str(user_id)))
    connection.commit()
    cursor.close()
    connection.close()

def get_all_games():
    connection = open_connection()
    cursor = connection.cursor()
    games = cursor.execute("SELECT * FROM GAMES")
    connection.commit()
    # cursor.close()
    # connection.close()
    return games

def get_all_versions():
    connection = open_connection()
    cursor = connection.cursor()
    versions = cursor.execute("SELECT * FROM VERSIONS")
    connection.commit()
    # cursor.close()
    # connection.close()
    return versions

def get_ver_by_name(version_name):
    connection = open_connection()
    cursor = connection.cursor()
    version = cursor.execute("SELECT * FROM VERSIONS WHERE Version_Name = (?)", [version_name]).fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return version

def create_game(game_name, game_desc, image, dev, game_id):
    connection = open_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO GAMES (Game_name, Game_description, Image, Developer, Game_ID) VALUES (?, ?, ?, ?, ?)",
                   (game_name, game_desc, image, dev, game_id)).fetchall()
    connection.commit()
    cursor.close()
    connection.close()

def create_version(game_name, version_name, version_desc, game_id, story, gameplay, download_link1, download_link2, download_link3):
    connection = open_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO VERSIONS (Game, Version_Name, Version_Description, ID, Story, Gameplay, Download_link1, Download_link2, Download_link3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (game_name, version_name, version_desc, game_id, story, gameplay, download_link1, download_link2, download_link3)).fetchall()
    connection.commit()
    cursor.close()
    connection.close()

def get_user_by_email(email):
    connection = open_connection()
    cursor = connection.cursor()
    user = cursor.execute("SELECT * FROM USERS WHERE EMAIL = ?", [email]).fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return user