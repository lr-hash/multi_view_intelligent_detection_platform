from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Import the API modules to register the routes
from . import auth
from . import integration
from . import processing
from . import visualization
from . import evaluation
from . import auxiliary
