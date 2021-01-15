from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from flask_debugtoolbar import DebugToolbarExtension
import pymysql

pymysql.install_as_MySQLdb()
"""创建对象"""
bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
"""上传"""
photos = UploadSet('photos', IMAGES)
"""调试工具"""
toolbar = DebugToolbarExtension()

def config_extensions(app):
	"""
	三方插件配置
	:param app:
	:return:
	"""
	bootstrap.init_app(app)
	db.init_app(app)
	moment.init_app(app)
	login_manager.init_app(app)
	toolbar.init_app(app)

	"""图片上传的配置"""
	configure_uploads(app, photos)
	"""设置上传文件大小"""
	patch_request_class(app, size=None)

	"""指定登录的端点"""
	login_manager.login_view = 'users.login'

	"""需要登录时的提示信息"""
	login_manager.login_message = '需要先登录'
	"""
	设置session保护级别
	None：禁用session保护
	'basic'：基本的保护，默认选项
	'strong'：最严格的保护，一旦用户登录信息改变，立即退出登录
	"""
	login_manager.session_protection = 'strong'
