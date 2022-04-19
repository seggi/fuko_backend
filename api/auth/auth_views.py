from flask import Blueprint,  url_for, render_template_string
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from .. import db
from api.utils.responses import response_with
from api.utils import responses as resp
from api.database.models import User
from api.utils.model_marsh import UserSchema
from api.utils.token import generate_verification_token, confirm_verification_token
from api.utils.email import send_email

# Manage route

auth =  Blueprint("auth", __name__, url_prefix="/api/user")

@auth.post('/signup')
def create_user():
    try:
        data = {
            "email": request.json["email"],
            "password": request.json["password"],
            "username": request.json["username"],
            "birth_date": request.json["birth_date"]
        }
        if data['email'] is None or data['username'] is None:
            return response_with(resp.INVALID_INPUT_422)

        if User.find_by_email(data['email']) or User.find_by_username(data['username']):
            return response_with(resp.SUCCESS_201)

        data['password'] = User.generate_hash(data['password'])

        user_schema = UserSchema()
        user_data = user_schema.load(data, partial=True)
        token = generate_verification_token(data['email'])

        verification_email = url_for(
            'auth.verify_email', token=token, _external=True)
        html = render_template_string(
            """
            <div>
                <h2>Welcome to  Fuko</h2>
                <p>
                    Thank you for sign up to our app. 
                    Please click the button below to activate your account:
                </p>
                <p>
                    <a href='{{ verification_email }}' style='padding: 8px; background: blue; width: 20px; color: white; text-decoration: none;'>Confirm Signup</a>
                </p>
                <br/>
                <p> Thanks!</p>  
            </div>
            """, verification_email=verification_email)
        subject = "Please Verify your email"
        send_email(user_data.email, subject, html)
        user_data.create()

        return response_with(resp.SUCCESS_200)

    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)

# Verification token
@auth.get('/confirm/<token>')
def verify_email(token):
    try:
        email = confirm_verification_token(token)
    except:
        return response_with(resp.SERVER_ERROR_404)

    user = User.query.filter_by(email=email).first_or_404()

    if user.confirmed:
        return response_with(resp.INVALID_INPUT_422)
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        return render_template_string("<p>E-mail verified, you can proceed to login now.<p/>")

# Refresh token
@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)

# Login
@auth.post('/login')
def sign_in_user():
    try:
        data = {
            "email": request.json["email"],
            "password": request.json["password"]
        }

        if data['email']:
            current_user = User.find_by_email(data['email'])
        if not current_user:
            return response_with(resp.SERVER_ERROR_404)
        if current_user and not current_user.confirmed:
            return response_with(resp.BAD_REQUEST_400)
        if User.verify_hash(data['password'], current_user.password):
            user = User.query.filter_by(email=data['email']).first()

            access_token = create_access_token(
                identity={"id": user.id, "email": data["email"]})
            access_fresh_token = create_refresh_token(identity={"id": user.id, "email": data["email"]})
            return response_with(resp.SUCCESS_201, value={'message': f'{current_user.username}',
                                                          "access_token": access_token,
                                                          "access_fresh_token": access_fresh_token,
                                                          "data": {
                                                              "first_name": user.first_name,
                                                              "last_name": user.last_name,
                                                              "username": user.username,
                                                              "status": user.status,
                                                              "user_id": user.id
                                                          }
                                                        }
                                                    )
        else:
            return response_with(resp.UNAUTHORIZED_403)

    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)
