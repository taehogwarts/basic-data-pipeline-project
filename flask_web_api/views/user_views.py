from flask import Blueprint, request
from flask_web_api import DB_FILEPATH, PKL_FILEPATH

user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['GET'])
def get_prediction():

    import pandas as pd
    import pickle
    import json

    with open(PKL_FILEPATH,'rb') as pickle_file:
        model = pickle.load(pickle_file)

    user_gender = request.args.get('Gender', default=None, type=int)
    user_age = request.args.get('Age', default=None, type=int)
    user_clinic = request.args.get('ClinicCode', default=None, type=int)

    user_data = [[user_gender, user_age, user_clinic]]
    columns_list = ['Gender', 'Age', 'ClinicCode']

    X_test = pd.DataFrame(data=user_data, columns=columns_list)
    y_pred = model.predict(X_test)

    pred_data = {
        '유저 입력값': {
            '성별코드': user_gender, 
            '연령': user_age, 
            '진료과목코드': user_clinic
        },
        '모델 예측값': {
            '본인부담금 예측금액(원)': round(y_pred[0])
        }
    }
    json_pred_data = json.dumps(pred_data)

    # print_pred = '머신러닝 모델로 예측한 진료비 본인부담금액은 '+str(round(y_pred[0]))+'원입니다.'
    
    return json_pred_data, 200

