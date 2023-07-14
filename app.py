from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from database import config

from models.user import User
from models.session import Session
from models.location import Location

from statistics import Statistics

app = Flask(__name__)
app.secret_key = config["secret_key"]

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login_view"))


@app.get("/")
@login_required
def home_view():
    return redirect(url_for("overview_view"))


@app.get("/overview")
@login_required
def overview_view():
    return render_template("overview.html")


@app.get("/sessions")
@login_required
def sessions_view():
    return render_template("sessions.html")


@app.get("/locations")
@login_required
def locations_view():
    return render_template("locations.html")


@app.get("/map")
@login_required
def map_view():
    return render_template("map.html")


@app.get("/login")
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for("home_view"))

    return render_template("login.html")


@app.post("/login")
def login_post():
    data = request.json

    user = User.get_user_by_username(data["username"])

    if not user or not user.check_pass(data["password"]):
        return "Incorrect username or password", 401

    login_user(user, data["remember"])

    return "Logged in successfully", 200


@app.get("/register")
def register_view():
    if current_user.is_authenticated:
        return redirect(url_for("home_view"))

    return render_template("register.html")


@app.post("/register")
def register_post():
    data = request.json

    user = User.get_user_by_username(data["username"])

    if user:
        return "User already exists", 401

    user = User.create_user(data["username"], data["password"])

    login_user(user)

    return "Registered successfully", 201


@app.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home_view"))


@app.get("/api/sessions")
@login_required
def api_sessions_get():
    return jsonify([s.__dict__ for s in Session.get_all_sessions() if s.user_id == current_user.id])


@app.get("/api/sessions/<id>")
@login_required
def api_sessions_get_id(id: str):
    session = Session.get_session_by_id(int(id))
    return jsonify(session.__dict__) if session else (f"Session with id {id} not found", 404)


@app.post("/api/sessions")
@login_required
def api_sessions_post():
    data = request.json

    Session.create_session(data["location_id"], data["date_time"], current_user.id)

    return "Session created successfully", 201


@app.get("/api/locations/")
@login_required
def api_locations_get():
    return jsonify(
        sorted(
            [l.__dict__ for l in Location.get_all_locations() if l.user_id == current_user.id],
            key=lambda x: x["id"]
        )
    )


@app.get("/api/locations/<id>")
@login_required
def api_locations_get_id(id: str):
    location = Location.get_location_by_id(int(id))
    return jsonify(location.__dict__) if location else (f"Location with id {id} not found", 404)


@app.post("/api/locations")
@login_required
def api_locations_post():
    data = request.json

    name = data.get("name")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if any([
        name is None,
        latitude is None,
        longitude is None
    ]):
        return "Missing data", 400

    location = Location.create_location(data["name"], data["latitude"], data["longitude"], current_user.id)

    return jsonify(location.__dict__), 201


@app.put("/api/locations/<id>")
@login_required
def api_locations_put(id: str):
    location = Location.get_location_by_id(int(id))

    if not Location:
        return f"Location with id {id} not found", 404

    data = request.json

    location.update(
        data.get("name"),
        data.get("latitude"),
        data.get("longitude")
    )

    return "Updated location successfully", 200


@app.delete("/api/locations/<id>")
@login_required
def api_locations_delete(id: str):
    location = Location.get_location_by_id(int(id))

    if not Location:
        return f"Location with id {id} not found", 404

    location.delete()

    return "Deleted location successfully", 200


@app.get("/api/statistics")
@login_required
def api_statistics_get():
    user = User.get_user_by_id(current_user.id)

    if not user:
        return f"User with id {current_user.id} not found", 404

    stats = Statistics(user)

    return jsonify(stats.get_data()), 200


if __name__ == '__main__':
    app.run("0.0.0.0", port=42069)
