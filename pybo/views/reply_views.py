from flask import Blueprint, jsonify, request, abort
from ..database.models import Reply, Notice, db
import datetime
import pytz

bp = Blueprint("reply", __name__, url_prefix="/reply")


@bp.route("/list/<int:notice_id>", methods=["GET"])
def get_replies(notice_id):
    notice = db.session.get(Notice, notice_id)
    if notice is None:
        abort(404)

    replies = (
        db.session.query(Reply).filter_by(notice_id=notice_id).all()
    )  # Updated this line
    formatted_replies = [reply.format() for reply in replies]

    return jsonify({"success": True, "replies": formatted_replies})


@bp.route("/create", methods=["POST"])
def create_reply():
    data = request.get_json()
    author_name = data["author_name"]
    content = data["content"]
    notice_id = data["notice_id"]

    if (
        author_name == None
        or author_name == ""
        or content == None
        or content == ""
        or notice_id == None
    ):
        abort(400)

    try:
        new_reply = Reply(
            content=data["content"],
            author_name=data["author_name"],
            created_date=datetime.datetime.now(pytz.timezone("Asia/Seoul")),
            notice_id=data["notice_id"],
        )
        new_reply.insert()
        return jsonify(new_reply.format()), 201
    except:
        abort(422)
