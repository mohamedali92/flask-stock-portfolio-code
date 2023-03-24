from flask import Blueprint

stocks_blueprint = Blueprint('stocks', __name__, template_folder='templates')

from . import routes
