from flask import Flask, render_template,request
from flask_smorest import Blueprint
from flask_cors import CORS

from routes import databases_bp

#resolve to the application path
app = Flask(__name__)
CORS(app)
#cors = CORS(app,resources={r'*':{'origins':'*'}})

#creating the routes
app.register_blueprint(databases_bp)


@app.route("/")
def home():
    return "/home"


if __name__ == '__main__':
    app.run(host='0.0.0.0',ssl_context='adhoc')