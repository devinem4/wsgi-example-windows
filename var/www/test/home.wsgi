import bottle

application = bottle.default_app()

@bottle.route('/')
def home():
    return "hello world from my bottle mod_wsgi home.wsgi!"
