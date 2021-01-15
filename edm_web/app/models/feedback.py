from datetime import datetime
from app.extensions import db

class FeedBack(db.Model):
	"""
	用户反馈投诉
	"""
	__tablename__ = 't_account_feedback'
	FEEDBACK_ID = db.Column(db.BigInteger, primary_key=True)
	FEEDBACK_ACCOUNT = db.Column(db.String(64))
	FEEDBACK_TYPE = db.Column(db.SMALLINT)
	FEEDBACK_REASON = db.Column(db.String(512))
	STATUS = db.Column(db.SMALLINT, default=1)
	INTIME = db.Column(db.DateTime, default=datetime.now)
	MODTIME = db.Column(db.DateTime, default=datetime.now)

