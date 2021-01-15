import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
	"""
	定义配置基类
	"""
	"""秘钥"""
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'adsawdws'

	"""
	数据库公用配置
	"""
	"""无警告"""
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	"""自动提交"""
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True

	"""文件上传的位置"""
	MAX_CONTENT_LENGTH = 8 * 1024 * 1024
	UPLOADED_PHOTOS_DEST = os.path.join(BASE_DIR, 'static/uploads')

	"""额外的初始化操作"""
	@staticmethod
	def init_app(app):
		pass


# 开发环境配置
class DevelopmentConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1/edm'


# 测试环境配置
class TestConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/edm'


# 生产环境
class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://edm:@dalianyoukai888@106.12.139.138/edm'



"""生成字典 用于查找配置类"""
config = {
	'development': DevelopmentConfig,
	'testing': TestConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}


