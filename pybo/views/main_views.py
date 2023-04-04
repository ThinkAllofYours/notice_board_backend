from flask import Blueprint, jsonify, request
from ..auth.auth import requires_auth
from ..database.models import db, Notice
from config import app_config
from sqlalchemy import select

bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/")
def index():
    return jsonify(
        {
            "success": True,
        }
    )
