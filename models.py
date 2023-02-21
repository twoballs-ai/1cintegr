from flask import Blueprint, render_template, request, redirect, url_for, Response, flash, jsonify
import requests
from flask import make_response
import json  # подключили библиотеку для работы с json
from pprint import pprint  # подключили Pprint для красоты выдачи текста
from flask.views import View

from auth import getAccessToken

models_func = Blueprint('models_func', __name__)


def podved_list(param_request):
    headers_get = getAccessToken()
    headers = {'AccessToken': headers_get}
    url = "https://localhost/copy_1/hs/HTTP_SERVER/podved_list"
    response = requests.post(url, param_request, verify=False, headers=headers)
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 401:
        print('Not auth.')
    data = response.json()['list_PD']
    print(response.json())
    return data


def category_objects_list(param_request):
    headers_get = getAccessToken()
    headers = {'AccessToken': headers_get}
    url = "https://localhost/copy_1/hs/HTTP_SERVER/category_objects_list"
    response = requests.post(url, param_request, verify=False, headers=headers)
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 401:
        print('Not auth.')
    data = response.json()['list_cat']
    return data


def podved_card(param_request):
    headers_get = getAccessToken()
    headers = {'AccessToken': headers_get}
    url = "https://localhost/copy_1/hs/HTTP_SERVER/podved_card"
    response = requests.post(url, param_request, verify=False, headers=headers)
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 401:
        print('Not auth.')
    data = response.json()
    return data


def object_card(param_request):
    headers_get = getAccessToken()
    headers = {'AccessToken': headers_get}
    url = "https://localhost/copy_1/hs/HTTP_SERVER/object_card"
    response = requests.get(url, param_request, verify=False, headers=headers)
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 401:
        print('Not auth.')
    data = response.json()
    return data


def objects_list(param_request):
    headers_get = getAccessToken()
    headers = {'AccessToken': headers_get}
    url = "https://localhost/copy_1/hs/HTTP_SERVER/objects_list"
    response = requests.get(url, param_request, verify=False, headers=headers)
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 401:
        print('Not auth.')
    data = response.json()['list_OC']
    return data

