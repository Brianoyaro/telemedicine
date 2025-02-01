from flask import Blueprint

bp = Blueprint('hospital', __name__)

from app.hospital import hospital_routes