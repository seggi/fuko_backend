from flask import Blueprint, request, render_template

document = Blueprint("document", __name__,  url_prefix="/")

@document.route('/')
def get_template():
    welcome_msg = "Welcome to fuko API"
    return render_template('index.html', welcome_msg=welcome_msg)