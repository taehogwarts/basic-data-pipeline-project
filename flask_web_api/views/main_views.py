from flask import Blueprint, render_template


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():

    ### DB의 ClinicCode 테이블에서 불러오는 게 이상적이지만 배포 시 용량제한으로 DB 파일 업로드가 어려울 것을 감안하여 하드코딩
    clinic_dict_list = [
        {'Key': 0, 'Value': '일반의'},
        {'Key': 1, 'Value': '내과'}, 
        {'Key': 2, 'Value': '신경과'}, 
        {'Key': 3, 'Value': '정신건강의학과'}, 
        {'Key': 4, 'Value': '외과'}, 
        {'Key': 5, 'Value': '정형외과'}, 
        {'Key': 6, 'Value': '신경외과'}, 
        {'Key': 7, 'Value': '흉부외과'}, 
        {'Key': 8, 'Value': '성형외과'}, 
        {'Key': 9, 'Value': '마취통증의학과'}, 
        {'Key': 10, 'Value': '산부인과'}, 
        {'Key': 11, 'Value': '소아청소년과'}, 
        {'Key': 12, 'Value': '안과'}, 
        {'Key': 13, 'Value': '이비인후과'}, 
        {'Key': 14, 'Value': '피부과'}, 
        {'Key': 15, 'Value': '비뇨기과'}, 
        {'Key': 16, 'Value': '영상의학과'}, 
        {'Key': 17, 'Value': '방사선종양학과'}, 
        {'Key': 18, 'Value': '병리과'}, 
        {'Key': 19, 'Value': '진단검사의학과'}, 
        {'Key': 20, 'Value': '결핵과'}, 
        {'Key': 21, 'Value': '재활의학과'}, 
        {'Key': 22, 'Value': '핵의학과'}, 
        {'Key': 23, 'Value': '가정의학과'}, 
        {'Key': 24, 'Value': '응급의학과'}, 
        {'Key': 25, 'Value': '산업의학과'}, 
        {'Key': 26, 'Value': '예방의학과'}, 
        {'Key': 50, 'Value': '구강악안면외과'}, 
        {'Key': 51, 'Value': '치과보철과'}, 
        {'Key': 52, 'Value': '치과교정과'}, 
        {'Key': 53, 'Value': '소아치과'}, 
        {'Key': 54, 'Value': '치주과'}, 
        {'Key': 55, 'Value': '치과보존과'}, 
        {'Key': 56, 'Value': '구강내과'}, 
        {'Key': 57, 'Value': '구강악안면방사선과'}, 
        {'Key': 58, 'Value': '구강병리과'}, 
        {'Key': 59, 'Value': '예방치과'}, 
        {'Key': 80, 'Value': '한방내과'}, 
        {'Key': 81, 'Value': '한방부인과'}, 
        {'Key': 82, 'Value': '한방소아과'}, 
        {'Key': 83, 'Value': '한방안과, 한방이비인후과'}, 
        {'Key': 84, 'Value': '한방신경정신과'}, 
        {'Key': 85, 'Value': '침구과'}, 
        {'Key': 86, 'Value': '한방재활의학과'}, 
        {'Key': 87, 'Value': '사상체질과'}, 
        {'Key': 88, 'Value': '한방응급의학과'}, 
    ]

    return render_template('index.html', clinic_list=clinic_dict_list)
