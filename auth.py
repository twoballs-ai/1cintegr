from flask import Blueprint, render_template, request, redirect, url_for
import requests
from flask import make_response

auth_func = Blueprint('auth_func', __name__)

@auth_func.route('/post')
def post(*args, **kwargs):
    # if key doesn't exist, returns None
    param_request = {'RefreshToken': '2fce707c-2ffc-48d8-afb9-cf1638a53508'}
    # param_request = {'login': 'test_user', 'password': '1010'}
    # param_request = {'AccessToken':'d97a1df3-2e83-40d5-a39e-6c2bf259e2dd'}
    response = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/Auth20", data=param_request,
                             verify=False)
    print("response.json:\n{}\n\n".format(response.json()))
    # if response.status_code == 200:
    #     print('Success!')
    #     refresh_token = response.json()['RefreshToken']
    #     param_request = {'RefreshToken': refresh_token}
    #     response = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/Auth20", data=param_request,
    #                              verify=False)
    #     print("response.json:\n{}\n\n".format(response.json()))
    # elif response.status_code == 401:
    #     print('Not auth.')
    print("response:\n{}\n\n".format(response))
    print("response.url:\n{}\n\n".format(response.url))  # Посмотреть формат URL (с параметрами)
    # print("response.headers:\n{}\n\n".format(response.headers))  # Header of the request
    # print("response.status_code:\n{}\n\n".format(response.status_code))  # Получить код ответа
    # print("response.text:\n{}\n\n".format(response.text))  # Text Output
    print("response.json:\n{}\n\n".format(response.json()))
    # print("response.encoding:\n{}\n\n".format(response.encoding))  # Узнать, какую кодировку использует Requests
    # print("response.content:\n{}\n\n".format(response.content))  # В бинарном виде
    return "response.text:\n{}\n\n".format(response.text)

@auth_func.route('/get')
def get():
    url = "https://localhost/copy_1/hs/HTTP_SERVER/Auth20"
    # if key doesn't exist, returns None
    param_request = {'refresh_token': 'b9903a5a-208c-47db-98ce-705a221eb3ea'}
    # response = requests.get(url, verify=False)
    response = requests.get(url, param_request, verify=False)
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 401:
        print('Not auth.')
    data = response.json()
    # print("response:\n{}\n\n".format(response))
    # print("response.url:\n{}\n\n".format(response.url))  # Посмотреть формат URL (с параметрами)
    # print("response.headers:\n{}\n\n".format(response.headers))  # Header of the request
    # print("response.status_code:\n{}\n\n".format(response.status_code))  # Получить код ответа
    # print("response.text:\n{}\n\n".format(response.text))  # Text Output
    # print("response.json:\n{}\n\n".format(response.json()))
    # print("response.encoding:\n{}\n\n".format(response.encoding))  # Узнать, какую кодировку использует Requests
    # print("response.content:\n{}\n\n".format(response.content))  # В бинарном виде
    # print(response.json())
    context = {'data': data}
    print(context)
    return render_template('get.html', **context)



@auth_func.route('/login' ,methods=['GET', 'POST'])
def login(refresh_token = None):
    # refr = request.cookies.get('refresh_token')
    # if request.cookies.get('refresh_token') != None:
    #
    #     return makeAccesToken()
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        return validateAccesToken()
    elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return makeAccesToken()

    # если нет ни токена рефреш ни акцес
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        if request.method == 'POST':
            login = request.form.get('username')
            password = request.form.get('password')
            print(login, password)
            param_request = {'login': login, 'password': password}
            response_cookie = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/Auth20", data=param_request,
                                 verify=False)
            if response_cookie.status_code == 200:
                print('Success!')
            elif response_cookie.status_code == 401:
                print('Not auth.')
            success = response_cookie.json()['success']
            blockuser = response_cookie.json()['blockuser']
            refresh_token = response_cookie.json()['RefreshToken']
            print(success,blockuser)
            if success == True and blockuser == False:
                return makeRefreshToken(refresh_token)
            else:
                return 'вы не имеете права'


    return render_template('logintest.html')


#
def makeRefreshToken(refresh_token):
    print('судьба вас примвела в makeRefreshToken')
    response = make_response(redirect(url_for('auth_func.login')))
    response.set_cookie('refresh_token', refresh_token, samesite='Lax', max_age=30 * 24 * 3600)
    return response


def makeAccesToken():
    print('судьба вас примвела в makeAccesToken')
    refresh_token = request.cookies.get('refresh_token')
    print(refresh_token)
    param_request = {'RefreshToken': refresh_token}
    response = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/Auth20", data=param_request,
                                    verify=False)
    access_token = response.json()['AccessToken']
    success = response.json()['success']
    blockuser = response.json()['blockuser']
    print("response.text:\n{}\n\n".format(response.text))
    if success == True and blockuser == False:
        print('dsvdsvd')
        response = make_response(redirect('podved'))
        response.set_cookie('access_token', access_token, samesite='Lax', max_age=86400)
        return response
    elif success == False and blockuser == False:
        return 'вы не имеете права'

def refreshAccesToken(*args,**kwargs):
    print(*args)
    print('судьба вас примвела в refreshAccesToken')
    refresh_token = request.cookies.get('refresh_token')
    print(refresh_token)
    param_request = {'RefreshToken': refresh_token}
    response = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/Auth20", data=param_request,
                                    verify=False)
    access_token = response.json()['AccessToken']
    print(access_token)
    success = response.json()['success']
    blockuser = response.json()['blockuser']
    print("response.text:\n{}\n\n".format(response.text))
    if success == True and blockuser == False:

        response = make_response(redirect(url_for(*args)))
        response.set_cookie('access_token', access_token, samesite='Lax', max_age=86400)
        print('dsvdsvd')
        return response
    elif success == False and blockuser == False:
        return 'вы не имеете права'


def validateAccesToken(*args, **kwargs):
    access_token = request.cookies.get('access_token')
    param_request = {'AccessToken': access_token}
    response = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/Auth20", data=param_request,
                             verify=False)
    success = response.json()['success']
    blockuser = response.json()['blockuser']
    token_expired = response.json()['AccessTokenTokenExpired']
    print('test', success, blockuser, token_expired)
    if success == True and blockuser == False and token_expired == False:
        return True
    elif success == True and blockuser == False and token_expired == True:
        return refreshAccesToken()

