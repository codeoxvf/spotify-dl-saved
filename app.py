from flask import Flask

from download import download_page
from index import index_page


app = Flask(__name__)

app.register_blueprint(download_page)
app.register_blueprint(index_page)
