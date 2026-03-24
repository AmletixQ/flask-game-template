import requests

from flask import Flask, redirect, render_template, request, session, url_for, jsonify

from constants import API_URL, APP_SECRET_KEY
from utils.get_points import get_points
from utils.post_points import post_points


app = Flask(__name__)
app.secret_key = APP_SECRET_KEY


@app.route("/")
def index():
    user_id = session.get("user_id", None)
    user_points = session.get("user_points", None)

    return render_template("index.html", user_id=user_id, points=user_points)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    if not (email and password):
        return render_template("login.html", error={"message": "ERROR!!!"})

    user_data = {"email": email, "password": password}

    try:
        response = requests.post(f"{API_URL}/account/login", json=user_data)
        response.raise_for_status()

        data = response.json()
        user_id = None

        if isinstance(data, str):
            user_id = data
        elif isinstance(data, dict):
            user_id = data.get("userId")

        if not user_id:
            return render_template(
                "login.html",
                error={"message": "Не удалось получить ID пользователя"},
            )

        session["user_id"] = user_id

    except requests.exceptions.RequestException as e:
        print(f"Ошибка API login: {e}")
        return render_template("login.html", error={"message": "ERROR!!!"})
    except ValueError:
        return render_template(
            "login.html", error={"message": "Неверный ответ от сервера"}
        )

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_points", None)

    return render_template("index.html")


@app.route("/points", methods=["GET", "POST"])
def points():
    action = request.args.get("action")

    if request.method == "GET":
        session["user_points"] = get_points()
    elif request.method == "POST":
        points = int(request.form.get("points", 0))
        session["user_points"] = post_points(points)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
