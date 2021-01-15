from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request, render_template_string
from app.extensions import db
from sqlalchemy.sql import text
from app.models import FeedBack
from app.common import BusinessUtil

"""创建蓝本对象"""
edm = Blueprint('edm', __name__)


@edm.route('/complain', methods=['GET'])
def complain():
	"""
	投诉信息
	:return:
	"""
	email = request.args.get("f")
	return render_template("/edm/complain.html", email=email)


@edm.route('/complain/save', methods=['POST'])
def save_complain():
	"""
	保存投诉信息
	:return:
	"""
	email = request.form.get("email")
	reason = request.form.getlist("reason")
	if reason:
		reason = ",".join(reason)
	else:
		reason = ""
	if email:
		email = email.replace(" ", "+")
		SECRET_KEY = current_app.config["SECRET_KEY"]
		try:
			"""解码"""
			email = BusinessUtil.decrypt_aes(SECRET_KEY, email)
			"""添加信息"""
			feed_back = db.session.query(FeedBack).filter(text("FEEDBACK_ACCOUNT=:email and FEEDBACK_TYPE=2")).params(
				email=email).first()
			if feed_back:
				feed_back.FEEDBACK_REASON = reason
			else:
				feed_back = FeedBack(FEEDBACK_ACCOUNT=email, FEEDBACK_REASON=reason, FEEDBACK_TYPE=2)
			db.session.add(feed_back)
			db.session.commit()
		except Exception as e:
			pass
	return "投诉成功"


@edm.route('/unsubscribe', methods=['GET'])
def unsubscribe():
	"""
	退订信息
	:return:
	"""
	email = request.args.get("f")
	return render_template("/edm/unsubscribe.html", email=email)


@edm.route('/unsubscribe/save', methods=['POST'])
def save_unsubscribe():
	"""
	保存退订信息
	:return:
	"""
	email = request.form.get("email")
	reason = request.form.getlist("reason")
	if reason:
		reason = ",".join(reason)
	else:
		reason = ""
	if email:
		email = email.replace(" ", "+")
		SECRET_KEY = current_app.config["SECRET_KEY"]
		try:
			"""解码"""
			email = BusinessUtil.decrypt_aes(SECRET_KEY, email)
			"""添加信息"""
			feed_back = db.session.query(FeedBack).filter(text("FEEDBACK_ACCOUNT=:email and FEEDBACK_TYPE=1")).params(
				email=email).first()
			if feed_back:
				feed_back.FEEDBACK_REASON = reason
			else:
				feed_back = FeedBack(FEEDBACK_ACCOUNT=email, FEEDBACK_REASON=reason, FEEDBACK_TYPE=1)
			db.session.add(feed_back)
			db.session.commit()
		except Exception as e:
			pass
	return "退订成功"
