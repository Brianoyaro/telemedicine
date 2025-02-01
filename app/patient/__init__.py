from flask import Blueprint

bp = Blueprint('patient', __name__)

from app.patient import patient_routes