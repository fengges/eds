

from eds import app
from gevent import pywsgi,monkey

monkey.patch_all()

server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
server.serve_forever()
# app.jinja_env.auto_reload = True
# app.run(host="0.0.0.0", debug=True, port=80)

#-----session_key-----
# app.SECRET_KEY = os.urandom(24)