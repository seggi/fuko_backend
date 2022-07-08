from flask import Blueprint,  url_for, render_template_string
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from .. import db
from api.utils.responses import response_with
from api.utils import responses as resp
from api.database.models import User
from api.utils.model_marsh import UserSchema
from api.utils.token import generate_verification_token

admin_auth = Blueprint("auth", __name__, url_prefix="/api/admin")


@admin_auth.post('/signup')
def create_user():
    try:
        data = {
            "password": request.json["password"],
            "username": request.json["username"],
            "email": "nankim45@gmail.com"
        }

        if User.find_by_username(data['username']):
            return response_with(resp.SUCCESS_201)

        data['password'] = User.generate_hash(data['password'])

        user_schema = UserSchema()
        user_data = user_schema.load(data, partial=True)
        token = generate_verification_token(data['email'])
        user_data.create()

        return response_with(resp.SUCCESS_200)

    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)
