from flask import Blueprint, request, render_template

from ..utils.documents import doc

document = Blueprint("document", __name__,  url_prefix="/")

@document.route('/')
def get_template():
    welcome_msg = "Welcome to fuko API"
    return render_template('index.html', welcome_msg=welcome_msg)

@document.route('/api/docs')
def api_doc():

    return render_template(
        'display_doc.html', 
        app_title=doc['app_title'],
        app_sections = doc["app_sections"]
    )