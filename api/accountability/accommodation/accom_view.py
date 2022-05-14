from datetime import date
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.accountability.global_amount.global_amount_views import QUERY
from sqlalchemy import extract, desc

from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.core.objects import ManageQuery
from api.core.labels import AppLabels

from ... import db
from api.database.models import LessorOrLandlordToRentPayment, RentPaymentOption

accommodation = Blueprint("accommodation", __name__,  url_prefix="/api/user/account/accommodation")

todays_date = date.today()
QUERY = QueryGlobalRepport()
manage_query = ManageQuery()
APP_LABEL = AppLabels()
now = datetime.now()


# Add rent payment option period
@accommodation.post("/add-rent-payment-option")
@jwt_required(refresh=True)
def add_rent_payment_option():
    try:
        data = request.json
        QUERY.insert_data(db=db, table_data=RentPaymentOption(**data))
        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Rent payment option added with success")
        })
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

# Invite Landlorder or lessor
@accommodation.post("/invite-partner-to-rent-payment")
@jwt_required(refresh=True)
def invite_partner_to_rent_payment():
    user_id = get_jwt_identity()['id']
    try:
        data = request.json
        if data["landlord_id"] == "":
            get_data = data | {"landlord_id": user_id}
            request_sent = db.session.query(LessorOrLandlordToRentPayment).\
                filter(LessorOrLandlordToRentPayment.lessor_id == get_data['lessor_id']).\
                filter(LessorOrLandlordToRentPayment.landlord_id == get_data['landlord_id']).first()

            if request_sent:
                return jsonify({
                    "code": APP_LABEL.label("Alert"),
                    "message": APP_LABEL.label("Request already sent."),
                }) 
            QUERY.insert_data(db=db, table_data=LessorOrLandlordToRentPayment(**get_data))
            return jsonify({
                "code": APP_LABEL.label("success"),
                "message": APP_LABEL.label("Request sent")
            })
        else:
            get_data = data | {"lessor_id": user_id}
            request_sent = db.session.query(LessorOrLandlordToRentPayment).\
                filter(LessorOrLandlordToRentPayment.lessor_id == get_data['lessor_id']).\
                filter(LessorOrLandlordToRentPayment.landlord_id == get_data['landlord_id']).first()

            if request_sent:
                return jsonify({
                    "code": APP_LABEL.label("Alert"),
                    "message": APP_LABEL.label("Request already sent."),
                }) 
            QUERY.insert_data(db=db, table_data=LessorOrLandlordToRentPayment(**get_data))
            return jsonify({
                "code": APP_LABEL.label("success"),
                "message": APP_LABEL.label("Request sent")
            })

    except Exception:
        return response_with(resp.INVALID_INPUT_422)

# Confirm request
@accommodation.put("/confirm-request/<int:request_id>")
@jwt_required(refresh=True)
def confirm_request(request_id):
    get_data = request.json
    try:
        request_confirm = db.session.query(LessorOrLandlordToRentPayment).\
                filter(LessorOrLandlordToRentPayment.request_status == get_data['request_status']).\
                first()
        if request_confirm:
            return jsonify({
                "code": APP_LABEL.label("Alert"),
                "message": APP_LABEL.label("You Already confirmed this request.")
            })
        else:
            confirm = db.session.query(LessorOrLandlordToRentPayment).\
                filter(LessorOrLandlordToRentPayment.id == request_id).one()
            confirm.request_status = get_data["request_status"]
            confirm.confirmed_at = now
            db.session.commit()
            return jsonify({
                "code": APP_LABEL.label("Success"),
                "message": APP_LABEL.label("Request confirm.")
            })

    except Exception:
        return response_with(resp.INVALID_INPUT_422)

