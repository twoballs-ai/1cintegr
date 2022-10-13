from flask import Blueprint, render_template, request, redirect, url_for, Response
import requests
from flask import make_response
import json  # подключили библиотеку для работы с json
from pprint import pprint  # подключили Pprint для красоты выдачи текста
auth_func = Blueprint('auth_func', __name__)




def jsonPars():
    with open('static/1cintegr/regions.json', 'r', encoding='utf-8') as f:
        text = json.load(f)  # загнали все, что получилось в переменную
        pprint(text)  # вывели результат на экран
        return text


# @auth_func.route('/post')
# def post(*args, **kwargs):
#     # if key doesn't exist, returns None
#     # param_request = {'RefreshToken': '058832e4-2c7b-43f1-8bcc-f81ba3feb4d3'}
#     param_request = {'region': 'region', 'area': 'area', 'city': 'city', 'settlement': 'settlement', 'street': 'street',
#                             'house': 'house', 'flat': 'flat', 'postal_code': 'postal_code', 'name': 'name',
#                             'egrn_nomer': 'egrn_nomer', 'kadastr': 'kadastr', 'object_type': 'object_type',
#                             'object_area': 'object_area', 'encumbrance': 'encumbrance', 'description': 'description',
#                             'foto_main': 'foto_main', 'foto_multi': 'foto_multi', 'code': 'new_object'
#                             }
#     # param_request = {'login': 'test_user', 'password': '1010'}
#     # param_request = {'AccessToken':'e7244dd9-d983-403b-86e0-ff3d5cf2f600'}
#     response = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/object_card", data=param_request,
#                              verify=False)
#     print("response.json:\n{}\n\n".format(response.json()))
#     # if response.status_code == 200:
#     #     print('Success!')
#     #     refresh_token = response.json()['RefreshToken']
#     #     param_request = {'RefreshToken': refresh_token}
#     #     response = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/Auth20", data=param_request,
#     #                              verify=False)
#     #     print("response.json:\n{}\n\n".format(response.json()))
#     # elif response.status_code == 401:
#     #     print('Not auth.')
#     print("response:\n{}\n\n".format(response))
#     print("response.url:\n{}\n\n".format(response.url))  # Посмотреть формат URL (с параметрами)
#     # print("response.headers:\n{}\n\n".format(response.headers))  # Header of the request
#     # print("response.status_code:\n{}\n\n".format(response.status_code))  # Получить код ответа
#     # print("response.text:\n{}\n\n".format(response.text))  # Text Output
#     print("response.json:\n{}\n\n".format(response.json()))
#     # print("response.encoding:\n{}\n\n".format(response.encoding))  # Узнать, какую кодировку использует Requests
#     # print("response.content:\n{}\n\n".format(response.content))  # В бинарном виде
#     return "response.text:\n{}\n\n".format(response.text)
#
@auth_func.route('/get')
def get():
    url = "https://localhost/copy_1/hs/HTTP_SERVER/RulesNewObjects"
    # if key doesn't exist, returns None
    # param_request = {'refresh_token': 'b9903a5a-208c-47db-98ce-705a221eb3ea'}
    # response = requests.get(url, verify=False)
    response = requests.get(url,verify=False)
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

@auth_func.route('/signout')
def signout():
    print('удаляем токены')
    response = make_response(redirect(url_for('auth_func.login')))
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    # возвращаем измененный ответ
    return response

@auth_func.route('/login' ,methods=['GET', 'POST'])
def login(refresh_token = None):
    # refr = request.cookies.get('refresh_token')
    # if request.cookies.get('refresh_token') != None:
    #
    #     return makeAccesToken()
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid:
            return redirect(url_for('podved'))
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


    return render_template('login.html', title='Авторизация')


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
    access_token  = response.json()['AccessToken']
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

def refreshAccesToken(link_send_to_refresh):
    print(link_send_to_refresh)
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
    link = link_send_to_refresh.get('link')
    id = link_send_to_refresh.get('id')
    print(id)
    if success == True and blockuser == False:
        if id == None:
            response = make_response(redirect(url_for(link)))
            print('response')
            response.set_cookie('access_token', access_token, samesite='Lax', max_age=86400)
            print('dsvdsvd if')
            return response
        else:
            response = make_response(redirect(url_for(link, id=id)))
            print('response')
            response.set_cookie('access_token', access_token, samesite='Lax', max_age=86400)
            print('dsvdsvd if')
            return response
    elif success == False and blockuser == False:
        return deleteTokens()


def validateAccesToken():
    access_token = request.cookies.get('access_token')
    param_request = {'AccessToken': access_token}
    response = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/Auth20", data=param_request,
                             verify=False)
    success = response.json()['success']
    blockuser = response.json()['blockuser']
    token_expired = response.json()['AccessTokenTokenExpired']
    print('test validateAccesToken', success, blockuser, token_expired, access_token)
    if success == True and blockuser == False and token_expired == False:
        return 'True'
    elif success == True and blockuser == False and token_expired == True:
        return refreshAccesToken()
    elif success == False and blockuser == False and token_expired == False:
        print('валидацию не прошел')
        return deleteTokens()


def deleteTokens():
    print('удаляем токены')
    response  = make_response(redirect(url_for('auth_func.login')))
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    # возвращаем измененный ответ
    return response