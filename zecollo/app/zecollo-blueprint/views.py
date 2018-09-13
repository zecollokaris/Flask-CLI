from . import zecollo-blueprint

@zecollo-blueprint.route('/')
def index():
	return '<h1> Hello world </h1>'