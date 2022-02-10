from crypt import methods
from flask import url_for, jsonify
from flask import request
from flask_jwt_extended import jwt_required
from uritemplate import partial

from services.app.api.database.models import User


from .. import db
from . import profile_view
from api.utils.responses import response_with
from api.utils import responses as reps

from services.app.api.utils.model_marsh import UserProfileSchema, UserSchema


# User setup profile for first time sign up
# Check if is the first time
@profile_view.route('/complete-profile', methods=['GET', 'POST'])
@jwt_required()
def user_complete_profile():
    user_schema = UserSchema()
    user_profile_schema = UserProfileSchema()

    data = {
        "users": {
            "user_id": request.json["user_id"],
            "first_name": request.json["username"],
            "last_name": request.json["username"],
            "phone": request.json["username"],
            "status": request.json["username"],
        },
        "user_profile": {"gender":  request.json["username"]}
    }

    if data["users"]['first_name'] is None or data["users"]['last_name'] is None or data["users"]['phone'] is None\
            or data["user_profile"]['gender'] is None:
        return response_with(resp.INVALID_INPUT_422)

    user = User.query.filter_by(id=data['user_id']).first()
    if user:
        user_data = user_schema.load(data["users"], instance=user, partial=True)
        user_profile_data = user_schema.load(data["user_profile"], instance=user, partial=True)
        result = user_schema.dump(
            user_data.create() + user_profile_data.dump(user_profile_schema.create()))
        return jsonify(data=result)
    else:
        return response_with(resp.UNAUTHORIZED_403)
