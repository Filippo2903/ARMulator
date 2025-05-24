import os
# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))

from bottle import get

from mainweb import get
application = get()
