import functools
from flask import Blueprint
# Create view
global_amount_view = Blueprint(
    "global_amount_view", __name__, url_prefix="/api/user/account")
