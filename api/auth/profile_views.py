from flask import jsonify, Blueprint
from flask import request
from flask_jwt_extended import jwt_required

from api.database.models import User, UserProfile

from .. import db
from api.utils.responses import response_with
from api.utils import responses as resp

# User setup profile for first time sign up
# Check if is the first time

profile_view = Blueprint("profile_view", __name__, url_prefix="/api/user/profile")


@profile_view.post('/complete-profile')
@jwt_required()
def user_complete_profile():
    data = {
        "users": {
            "id": request.json["user_id"],
            "first_name": request.json["first_name"],
            "last_name": request.json["last_name"],
            "phone": request.json["phone"],
            "status": request.json["status"],
        },
        "user_profile": {
            "user_id": request.json["user_id"],
            "gender":  request.json["gender"],
        }

    }

    if data["users"]['first_name'] is None or data["users"]['last_name'] is None or data["users"]['phone'] is None\
            or data["user_profile"]['gender'] is None:
        return response_with(resp.INVALID_INPUT_422)

    user = User.query.filter_by(id=data["users"]['id']).first()
    if user:
        User.query.filter_by(id=data["users"]['id']).update(data["users"])
        user_id = UserProfile(**data["user_profile"])
        db.session.add(user_id)
        db.session.commit()
        return jsonify({
            "code": "success",
            "message": "Profile saved successfully. Now you can start your operation!"
        })
    else:
        return response_with(resp.UNAUTHORIZED_403)
