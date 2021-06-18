ERROR_MSG = {
    'EXIST_ID' : '이미 존재하는 아이디입니다.',
    'N0_EXIST_ID' : '존재하지 않는 아이디 입니다.',
    'MISSING_INPUT' : '항목을 모두 채워주세요.',
    'PASSWORD_CHECK' : '비밀번호를 확인해주세요.',
}

def build_error_msg(msg_type):
    return {'error' : { 'status' : True, 'msg' : ERROR_MSG[msg_type]} }

def build_success_msg(data):
    return { 'error' : {'status' : False}, 'data' : data }
