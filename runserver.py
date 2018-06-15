

from eds import app
from gevent import pywsgi,monkey

# monkey.patch_all()

# server = pywsgi.WSGIServer(('0.0.0.0', 8080), app)
# server.serve_forever()
app.run(host="0.0.0.0",  port=8080)

#-----session_key-----
# app.SECRET_KEY = os.urandom(24)