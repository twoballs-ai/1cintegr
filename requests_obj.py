from flask import Blueprint, render_template, request, redirect, url_for, Response
import requests_obj
import requests
from flask import make_response
import json  # подключили библиотеку для работы с json
from pprint import pprint  # подключили Pprint для красоты выдачи текста
# request = Blueprint('request', __name__)
from auth import getAccessToken

request_func = Blueprint('request_func', __name__)


def jsonPars():
    with open('static/1cintegr/regions.json', 'r', encoding='utf-8') as f:
        text = json.load(f)  # загнали все, что получилось в переменную
        # pprint(text)  # вывели результат на экран
        return text

def data_params_request():
    headers_get = getAccessToken()
    headers = {'AccessToken': headers_get}
    url_params = "https://localhost/copy_1/hs/HTTP_SERVER/RulesNewObjects"
    response_params = requests.get(url_params, verify=False, headers=headers)

    if response_params.status_code == 200:
        print('Success!')
    elif response_params.status_code == 401:
        print('Not auth.')
    data_params = response_params.json()
    # print(f"большой список значений {data_params}")
    return data_params


def listDepartsments():
    # param_request = {'AccessToken':'e7244dd9-d983-403b-86e0-ff3d5cf2f600'}
    headers_get = getAccessToken()
    headers = {'AccessToken': headers_get}
    response = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/listdepartments/", verify=False, headers=headers)
    data = response.json()['list_DP']
    print('обрати внимание ')
    print(response.json())
    return data


def getUserName():
    username_token = request.cookies.get('username_token')
    print(username_token)
    return username_token


@request_func.route('/post')
def post(*args, **kwargs):
    # if key doesn't exist, returns None
    # param_request = {'RefreshToken': 'afa56ec0-a71c-4829-be59-57fe033bcab5'}
    # param_request = {'region': 'region', 'area': 'area', 'city': 'city', 'settlement': 'settlement', 'street': 'street',
    #                         'house': 'house', 'flat': 'flat', 'postal_code': 'postal_code', 'name': 'name',
    #                         'egrn_nomer': 'egrn_nomer', 'kadastr': 'kadastr', 'object_type': 'object_type',
    #                         'object_area': 'object_area', 'encumbrance': 'encumbrance', 'description': 'description',
    #                         'foto_main': 'foto_main', 'foto_multi': 'foto_multi', 'code': 'new_object'
    #                         }
    param_request = {'department': '000000002', 'page':'1'}
    # param_request = {'AccessToken':'e7244dd9-d983-403b-86e0-ff3d5cf2f600'}
    response = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/objectlist2", param_request, verify=False)
    # response = requests.post("https://localhost/copy_1/hs/HTTP_SERVER/listdepartments/",  verify=False)
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


@request_func.route('/get')
def get():
    url = "https://localhost/copy_1/hs/HTTP_SERVER/object_card"
    # if key doesn't exist, returns None
    # param_request = {'refresh_token': 'b9903a5a-208c-47db-98ce-705a221eb3ea'}
    # response = requests.get(url, verify=False)
    param_request = {'code': '000000103'}
    headers_get = getAccessToken()
    headers = {'AccessToken': headers_get}
    response = requests.get(url,param_request, verify=False, headers=headers )
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
    return "response.text:\n{}\n\n".format(response.text)