from flask import Blueprint, render_template, request, redirect, url_for, Response, flash
import requests
from flask import make_response
import json  # подключили библиотеку для работы с json
from pprint import pprint  # подключили Pprint для красоты выдачи текста

auth_func = Blueprint('auth_func', __name__)
# global Permission_SeeAllObjects
# global podved_code


@auth_func.route('/signout')
def signout():
    print('удаляем токены')
    response = make_response(redirect(url_for('auth_func.login')))
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    response.delete_cookie('username_token')

    # возвращаем измененный ответ
    return response


@auth_func.route('/login', methods=['GET', 'POST'])
def login(refresh_token=None):
    # refr = request.cookies.get('refresh_token')
    # if request.cookies.get('refresh_token') != None:
    #
    #     return makeAccesToken()
    if request.cookies.get('access_token') and request.cookies.get('refresh_token'):
        valid = validateAccesToken()
        if valid == 'True':
            flash('Вы уже авторизованы')
            return redirect(url_for('podved'))
    elif request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        return makeAccesToken()

    # если нет ни токена рефреш ни акцес
    elif not request.cookies.get('refresh_token') and not request.cookies.get('access_token'):
        if request.method == 'POST':
            login = request.form.get('username')
            password = request.form.get('password')
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
            # print(success, blockuser)
            if success == True and blockuser == False:
                return makeRefreshToken(refresh_token)
            else:
                return 'вы не имеете права'

    return render_template('login.html', title='Авторизация')

def getPodved():
    podved = podved_code
    permission_see = Permission_SeeAllObjects
    print(podved, permission_see)
    return (podved, permission_see)



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
    username_token = response.json()['UserName']
    success = response.json()['success']
    blockuser = response.json()['blockuser']
    print("response.text:\n{}\n\n".format(response.text))
    if success == True and blockuser == False:
        print('dsvdsvd')
        response = make_response(redirect('podved'))
        response.set_cookie('access_token', access_token, samesite='Lax', max_age=86400)
        response.set_cookie('username_token', username_token, samesite='Lax', max_age=86400)
        return response
    elif success == False and blockuser == False:
        return 'вы не имеете права'


def refreshAccesToken(link_send_to_refresh):
    print(link_send_to_refresh)
    print('судьба вас примвела в refreshAccesToken')
    refresh_token = request.cookies.get('refresh_token')
    # print(refresh_token)
    param_request = {'RefreshToken': refresh_token}
    response = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/Auth20", data=param_request,
                             verify=False)
    access_token = response.json()['AccessToken']
    username_token = response.json()['UserName']
    # print(access_token)
    success = response.json()['success']
    blockuser = response.json()['blockuser']
    # print("response.text:\n{}\n\n".format(response.text))
    link = link_send_to_refresh.get('link')
    id = link_send_to_refresh.get('id')
    print("response.text:\n{}\n\n".format(response.text))
    print(id)
    if success == True and blockuser == False:
        if id == None:
            response = make_response(redirect(url_for(link)))
            print('response')
            response.set_cookie('access_token', access_token, samesite='Lax', max_age=86400)
            response.set_cookie('username_token', username_token, samesite='Lax', max_age=86400)
            print('dsvdsvd if')
            return response
        else:
            response = make_response(redirect(url_for(link, id=id)))
            print('response')
            response.set_cookie('access_token', access_token, samesite='Lax', max_age=86400)
            response.set_cookie('username_token', username_token, samesite='Lax', max_age=86400)
            print('dsvdsvd if')
            return response
    elif success == False and blockuser == False:
        return deleteTokens()


def validateAccesToken():
    global podved_code
    global Permission_SeeAllObjects
    access_token = request.cookies.get('access_token')
    param_request = {'AccessToken': access_token}
    response = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/Auth20", data=param_request,
                             verify=False)
    success = response.json()['success']
    blockuser = response.json()['blockuser']
    token_expired = response.json()['AccessTokenTokenExpired']
    try:
        Permission_SeeAllObjects = response.json()['Permission_SeeAllObjects']
        podved_code = response.json()['podved_code']
    except:
        print('podved_code and permission false')
        return 'False'
    print(podved_code, Permission_SeeAllObjects)
    print('test validateAccesToken:', success, blockuser, token_expired, access_token)
    print("response.text:\n{}\n\n".format(response.text))
    if success == True and blockuser == False and token_expired == False:
        # if podved_code == '' and Permission_SeeAllObjects =='':
        #     return 'False'
        # else:
        return 'True'

    elif success == True and blockuser == False and token_expired == True:
        return refreshAccesToken()
    elif success == False and blockuser == False and token_expired == False:
        print('валидацию не прошел')
        return deleteTokens()


def getAccessToken():
    access_token = request.cookies.get('access_token')
    print(access_token)
    return access_token


def deleteTokens():
    print('удаляем токены')
    response = make_response(redirect(url_for('auth_func.login')))
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    response.delete_cookie('username_token')
    # возвращаем измененный ответ
    return response
