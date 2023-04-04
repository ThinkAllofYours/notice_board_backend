from flask import Blueprint, jsonify, request, abort
from ..auth.auth import requires_auth
from ..database.models import Notice, db
from config import app_config
from sqlalchemy import select, func
import datetime
import pytz

bp = Blueprint("notice", __name__, url_prefix="/notice")


@bp.route("/list", methods=["GET"])
def get_notices():
    page = request.args.get("page", 1, type=int)
    NOTICES_PER_PAGE = app_config["NOTICES_PER_PAGE"]
    start = (page - 1) * NOTICES_PER_PAGE
    notices = Notice.query.offset(start).limit(NOTICES_PER_PAGE).all()
    total_cnt = db.session.query(func.count(Notice.id)).scalar()
    formatted_notices = [notice.format() for notice in notices]
    return jsonify(
        {
            "success": True,
            "notices": formatted_notices,
            "total_cnt": total_cnt,
        }
    )


@bp.route("/detail/<int:notice_id>")
def notice_detail(notice_id):
    session = db.session
    stmt = select(Notice).where(Notice.id == notice_id)
    try:
        notice = session.scalars(stmt).one()
        return jsonify({"success": True, "notice": notice.format()})
    except:
        abort(404)


@bp.route("/create", methods=["POST"])
@requires_auth("create:notice")
def create_notice():
    data = request.get_json()
    author_name = data["author_name"]
    title = data["title"]
    content = data["content"]
    if (
        title == None
        or title == ""
        or author_name == None
        or author_name == ""
        or content == None
        or content == ""
    ):
        abort(400)

    created_date = (datetime.datetime.now(pytz.timezone("Asia/Seoul")),)
    updated_date = (datetime.datetime.now(pytz.timezone("Asia/Seoul")),)

    try:
        new_notice = Notice(
            author_name=data["author_name"],
            title=data["title"],
            content=data["content"],
            views_count=0,
            recommends_count=0,
            not_recommends_count=0,
            created_date=datetime.datetime.now(pytz.timezone("Asia/Seoul")),
            updated_date=datetime.datetime.now(pytz.timezone("Asia/Seoul")),
            prev_id=None,
            next_id=None,
        )
        new_notice.insert()
        return jsonify(new_notice.format()), 201
    except:
        abort(422)


@bp.route("/modify/<int:notice_id>", methods=["POST"])
@requires_auth("edit:notice")
def modify_notice(notice_id):
    session = db.session
    stmt = select(Notice).where(Notice.id == notice_id)
    try:
        notice = session.scalars(stmt).one()
    except:
        abort(404)

    data = request.get_json()
    try:
        notice.author_name = data["author_name"]
        notice.title = data["title"]
        notice.content = data["content"]
        notice.updated_date = datetime.datetime.now(pytz.timezone("Asia/Seoul"))
        notice.update()
        return (
            jsonify(
                {
                    "success": True,
                    "notice": notice.format(),
                }
            ),
            200,
        )
    except KeyError:
        abort(400, "Missing fields in request data")
    except ValueError:
        abort(400, "Invalid request data")
    except:
        abort(422)


@bp.route("/delete/<int:notice_id>", methods=["DELETE"])
@requires_auth("delete:notice")
def delete_notice(notice_id):
    session = db.session
    stmt = select(Notice).where(Notice.id == notice_id)
    try:
        notice = session.scalars(stmt).one()
    except:
        abort(404)
    notice.delete()
    return "Notice deleted", 204


@bp.route("/increment-view/<int:notice_id>", methods=["PUT"])
def increment_view_count(notice_id):
    session = db.session
    stmt = select(Notice).where(Notice.id == notice_id)
    try:
        notice = session.scalars(stmt).one()
        notice.views_count += 1
        notice.update()
        return jsonify(success=True, views_count=notice.views_count)
    except:
        abort(404)
