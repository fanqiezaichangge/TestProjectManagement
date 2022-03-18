from flask import Flask
from apis.user import app_user
from apis.product import app_product
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_user)
app.register_blueprint(app_product)
CORS(app, supports_credentials=True)

if __name__ == '__main__':
    app.run(debug=True)
