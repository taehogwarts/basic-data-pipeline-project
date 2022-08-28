import os
from flask import Flask

DB_FILENAME = 'nhis_treatment_records_2021.db'
DB_FILEPATH = os.path.join(os.getcwd(), __name__, 'database/'+DB_FILENAME)

PKL_FILENAME = 'model.pkl'
PKL_FILEPATH = os.path.join(os.getcwd(), __name__, PKL_FILENAME) 


def create_app():

    app = Flask(__name__)
    
    from flask_web_api.views.main_views import main_bp
    from flask_web_api.views.user_views import user_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/api')

    return app