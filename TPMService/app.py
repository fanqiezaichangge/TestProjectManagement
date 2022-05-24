from flask import Flask
from src.apis.user import app_user
from src.apis.product import app_product
from src.apis.app import app_application
from src.apis.form import app_form
from flask_cors import CORS
# from src.configs import configs


app = Flask(__name__)
app.register_blueprint(app_user)
app.register_blueprint(app_product)
app.register_blueprint(app_application)
app.register_blueprint(app_form)
CORS(app, supports_credentials=True)

if __name__ == '__main__':
    app.run(debug=True)
