# Import view from the current directory
from flask import Blueprint
# Create view
auth_view = Blueprint('auth_view', __name__)
profile_view = Blueprint('profile_view', __name__)

from . import profile_views
from . import auth_views
