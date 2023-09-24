def pic_params(pic, con=.9, reg=None):
    return {'pic': pic, 'con': con, 'reg': reg}


class Pics:
    home_active_btn = pic_params('home_active_btn')
    home_inactive_btn = pic_params('home_inactive_btn')
    transfers_active_btn = pic_params('transfers_active_btn')
    transfers_inactive_btn = pic_params('transfers_inactive_btn')
    enter_pwd_field = pic_params('enter_pwd_field')
    homescreen = pic_params('homescreen')
    login_btn = pic_params('login_btn')
    sign_in_btn = pic_params('sign_in_btn')
