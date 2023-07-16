import io
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_minify import Minify

from database import config

from models.user import User
from models.password_reset_session import PasswordResetSession
from models.session import Session
from models.location import Location

from statistics import Statistics
from mail import send_mail_async

app = Flask(__name__)
app.secret_key = config["secret_key"]

login_manager = LoginManager()
login_manager.init_app(app)

Minify(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by("id", user_id)


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
    id = request.args.get("id")

    if id is not None:
        return render_template("location.html")

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

    user = User.get_by("email", data["email"])

    if not user or not user.check_pass(data["password"]):
        return "Incorrect email or password", 401

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

    user = User.get_by("id", data["email"])

    if user:
        return "User already exists", 401

    user = User.create(data["username"], data["password"], data["email"])

    login_user(user)

    return "Registered successfully", 201


@app.get("/forgot-password")
def forgot_password_view():
    args = request.args

    token = args.get("token")

    if not token:
        return render_template("forgot-password.html")

    session = PasswordResetSession.get_by("token", token)

    if not session or (datetime.now() - session.created_at).total_seconds() / 3600 > 24:
        return "This password reset token is invalid or expired", 400

    return render_template("forgot-password-new.html")


@app.post("/forgot-password")
def forgot_password_post():
    data = request.json

    email = data.get("email")

    if email is None:
        return "Missing email", 400

    user = User.get_by("email", email)

    if not user:
        return "Invalid email", 404

    session = PasswordResetSession.get_by("user_id", user.id)

    if session:
        session.delete()

    session = PasswordResetSession.create(user.id)

    send_mail_async(
        user.email,
        "Password reset",
        f"""
        Click the following link to reset your password, this request is valid for 24 hours.
        
        http://127.0.0.1:42069/forgot-password?token={session.token}
        """
    )

    return "Password reset request created successfully", 201


@app.put("/forgot-password")
def forgot_password_put():
    args = request.args

    token = args.get("token")

    if not token:
        return "Missing token", 400

    session = PasswordResetSession.get_by("token", token)

    if not session or (datetime.now() - session.created_at).total_seconds() / 3600 > 24:
        return "This password reset token is invalid or expired", 400

    data = request.json

    password = data.get("password")

    if not password:
        return "Missing new password", 400

    user = User.get_by("id", session.user_id)

    user.update(password=password)

    session.delete()

    return "Password updated successfully", 200


@app.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home_view"))


@app.get("/api/sessions")
@login_required
def api_sessions_get():
    return jsonify([s.as_dict() for s in Session.get_all() if s.user_id == current_user.id])


@app.get("/api/sessions/<id>")
@login_required
def api_sessions_get_id(id: str):
    session = Session.get_by("id", int(id))
    return jsonify(session.as_dict()) if session else (f"Session with id {id} not found", 404)


@app.post("/api/sessions")
@login_required
def api_sessions_post():
    data = request.json

    Session.create(data["location_id"], data["date_time"], current_user.id)

    return "Session created successfully", 201


@app.get("/api/locations/")
@login_required
def api_locations_get():
    return jsonify(
        sorted(
            [l.as_dict() for l in Location.get_all() if l.user_id == current_user.id],
            key=lambda l: l["id"]
        )
    )


@app.get("/api/locations/<id>")
@login_required
def api_locations_get_id(id: str):
    location = Location.get_by("id", int(id))
    return jsonify(location.as_dict()) if location else (f"Location with id {id} not found", 404)


@app.get("/api/locations/<id>.png")
@login_required
def api_locations_get_id_image(id: str):
    location = Location.get_by("id", int(id))

    if not location:
        return f"Location with id {id} not found", 404

    return send_file(
        io.BytesIO(location.cover_image) if location.cover_image else "static/placeholder.png",
        "image/png",
        download_name=f"location_{id}_{location.name.replace(' ', '_')}.png"
    )


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

    location = Location.create(data["name"], data["latitude"], data["longitude"], current_user.id, None, None)

    return jsonify(location.as_dict()), 201


@app.put("/api/locations/<id>")
@login_required
def api_locations_put(id: str):
    location = Location.get_by("id", int(id))

    if not Location:
        return f"Location with id {id} not found", 404

    data = request.json

    location.update(
        name=data.get("name"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude")
    )

    return "Updated location successfully", 200


@app.delete("/api/locations/<id>")
@login_required
def api_locations_delete(id: str):
    location = Location.get_by("id", int(id))

    if not Location:
        return f"Location with id {id} not found", 404

    location.delete()

    return "Deleted location successfully", 200


@app.get("/api/statistics")
@login_required
def api_statistics_get():
    user = User.get_by("id", current_user.id)

    if not user:
        return f"User with id {current_user.id} not found", 404

    stats = Statistics(user)

    return jsonify(stats.get_data()), 200


if __name__ == '__main__':
    app.run("0.0.0.0", port=42069)
