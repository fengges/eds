

from eds import app
from gevent import pywsgi,monkey

# app.run(host="0.0.0.0",debug=True,port=8080)

monkey.patch_all()

server = pywsgi.WSGIServer(('0.0.0.0', 8080), app)
server.serve_forever()
# WSGIServer(('0.0.0.0', 8080), app).serve_forever()

#-----session_key-----
# app.SECRET_KEY = os.urandom(24)