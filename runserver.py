
import sys,os

from eds import app

app.run(host="0.0.0.0",debug=True,port=8080)

#-----session_key-----
# app.SECRET_KEY = os.urandom(24)
