from .edm import edm

DEFAULT_BLUEPRINT = [
	(edm, '/edm')
]

def config_blueprint(app):
	"""
	循环读取元组中的蓝本
	:param app:
	:return:
	"""
	for blueprint, prefix in DEFAULT_BLUEPRINT:
		app.register_blueprint(blueprint, url_prefix=prefix)
