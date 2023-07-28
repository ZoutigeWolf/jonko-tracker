from flask import request, jsonify, send_file
from flask_login import login_required, current_user

from blueprints.blueprint import Blueprint

from models.user import User
from models.session import Session
from models.location import Location

group_names = {
    "users": User,
    "sessions": Session,
    "locations": Location,
}

api = Blueprint("API")


@api.get("/api/<group>")
@login_required
def api_get(group: str):
    cls = group_names.get(group)

    if not cls:
        return f"Group \"{group}\" not found", 404

    return jsonify([x.as_dict() for x in cls.get_all()])


@api.get("/api/<group>/<identifier: int>")
@login_required
def api_get_id(group: str, identifier: int):
    cls = group_names.get(group)

    if not cls:
        return f"Group \"{group}\" not found", 404

    obj = cls.get_by("id", identifier)

    if not obj:
        return f"{cls.__name__} with id {identifier} not found", 404

    if hasattr(obj, "user_id") and getattr(obj, "user_id") != current_user.id:
        return "Forbidden", 403

    return jsonify(obj.as_dict())


@api.post("/api/<group>")
@login_required
def api_post(group: str):
    cls = group_names.get(group)

    if not cls:
        return f"Group \"{group}\" not found", 404

    data = request.json

    return


@api.put("/api/<group>/<identifier: int>")
@login_required
def api_put(group: str, identifier: int):
    cls = group_names.get(group)

    if not cls:
        return f"Group \"{group}\" not found", 404

    obj = cls.get_by("id", identifier)

    if not obj:
        return f"{cls.__name__} with id {identifier} not found", 404

    if hasattr(obj, "user_id") and getattr(obj, "user_id") != current_user.id:
        return "Forbidden", 403


@api.delete("/api/<group>/<identifier: int>")
@login_required
def api_delete(group: str, identifier: int):
    cls = group_names.get(group)

    if not cls:
        return f"Group \"{group}\" not found", 404

    obj = cls.get_by("id", identifier)

    if not obj:
        return f"{cls.__name__} with id {identifier} not found", 404

    if hasattr(obj, "user_id") and getattr(obj, "user_id") != current_user.id:
        return "Forbidden", 403
