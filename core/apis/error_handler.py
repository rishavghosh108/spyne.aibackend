from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from core.libs.exceptions import SnyneError

from flask import jsonify

def handle_error(err):
    if isinstance(err, SnyneError):
        return jsonify(
            error=err.__class__.__name__, message=err.message
        ), err.status_code
    elif isinstance(err, ValidationError):
        return jsonify(
            error=err.__class__.__name__, message=err.messages
        ), 400
    elif isinstance(err, IntegrityError):
        return jsonify(
            error=err.__class__.__name__, message=str(err.orig)
        ), 400
    elif isinstance(err, HTTPException):
        return jsonify(
            error=err.__class__.__name__, message=str(err)
        ), err.code
    raise err