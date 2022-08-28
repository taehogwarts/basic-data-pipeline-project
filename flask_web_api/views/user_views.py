from flask import Blueprint, request
from flask_web_api import DB_FILEPATH, PKL_FILEPATH

user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['GET'])
def get_prediction():

    import pandas as pd
    import pickle

    with open(PKL_FILEPATH,'rb') as pickle_file:
        model = pickle.load(pickle_file)

    user_gender = request.args.get('Gender', default=None, type=int)
    user_age = request.args.get('Age', default=None, type=int)
    user_clinic = request.args.get('ClinicCode', default=None, type=int)

    user_data = [[user_gender, user_age, user_clinic]]
    columns_list = ['Gender', 'Age', 'ClinicCode']

    X_test = pd.DataFrame(data=user_data, columns=columns_list)
    y_pred = model.predict(X_test)

    print_pred = '머신러닝 모델로 예측한 진료비 본인부담금액은 '+str(round(y_pred[0]))+'원입니다.'
    
    return print_pred, 200

