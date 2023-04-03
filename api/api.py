import os

from flask import Blueprint, render_template, request, redirect, url_for, Response, flash, jsonify
import requests
from flask import make_response
import json  # подключили библиотеку для работы с json
from pprint import pprint  # подключили Pprint для красоты выдачи текста

from flask.views import MethodView
from werkzeug.utils import secure_filename

from auth import validateAccesToken, getPodved, deleteTokens, refreshAccesToken, login_api, accessTokenApi, \
    validateAccesTokenApi
from models import podved_list, objects_list, objects_list_api, podved_list_api, category_objects_list_api, \
    object_card_api, podved_card, podved_card_api, object_card_api_post
from requests_obj import data_params_request, listDepartsments, getUserName
from views import allowed_file
import config

from config import ALLOWED_EXTENSIONS

api_func = Blueprint('api_func', __name__)


class LoginApi(MethodView):

    def get(self):
        return jsonify('pisulka')

    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.get_json()
            getlogin = json.get('login')
            password = json.get('password')
            # login_api(login, password)
            # print(login_api(login, password))
            return login_api(getlogin, password)
        else:
            return 'Content-Type not supported!'


class GetAccessApi(MethodView):
    def get(self):
        return jsonify('pisulka')

    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.get_json()
            refresh_token = json.get('RefreshToken')
            return accessTokenApi(refresh_token)
        else:
            return 'Content-Type not supported!'


class ValidateAccessApi(MethodView):

    def get(self):
        return jsonify('pisulka')

    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.get_json()
            access_token = json.get('AccessToken')
            # login_api(login, password)
            # print(login_api(login, password))
            return validateAccesTokenApi(access_token)
        else:
            return 'Content-Type not supported!'


class CustomersAPI(MethodView):

    def get(self, id):
        id = id
        headers = request.headers.get('access')
        print(headers)

        param_request = {'page': id}
        # берем данные из файла модели
        data = objects_list_api(param_request, headers)
        context = {'data': data}
        return jsonify(context)

    def post(self):
        # create a new user
        name = 'name'
        # name = form.name.data
        description = 'description'
        object_type = 'object_type'
        PurposeObject = 'PurposeObject'
        Condition = 'Condition'
        technicalFloor = 'technicalFloor'
        Lift = 'Lift'
        remontDate = 'remontDate'
        SecurityObligation = 'SecurityObligation'
        # if 'file' not in request.files:
        #     # После перенаправления на страницу загрузки
        #     # покажем сообщение пользователю
        #     flash('Не могу прочитать файл')
        #     print('проблема')
        #     print('проблема', request.url)
        #     return redirect(request.url)
        #
        # file = request.files['file']
        # print(file)
        # # Если файл не выбран, то браузер может
        # # отправить пустой файл без имени.
        #
        # if file.filename == '':
        #     foto_scan = ''
        #
        #     print('dfdf', foto_scan)
        # if file and allowed_file(file.filename):
        #     # безопасно извлекаем оригинальное имя файла
        #     filename = secure_filename(file.filename)
        #     # сохраняем файл
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     foto_scan = "%s/%s" % (app.config['UPLOAD_FOLDER'], filename)
        region = 'region'
        address = 'address'
        object_area = 'object_area'
        LandCategory = 'LandCategory'
        TypeOfPermittedUse = 'TypeOfPermittedUse'

        RNFI = 'RNFI'
        RNFI_date = 'RNFI_date'
        owner_nomer = 'owner_nomer'
        owner_date = 'owner_date'
        RecordNumberVEGRP = 'RecordNumberVEGRP'
        DateRecordsVEGRP = 'DateRecordsVEGRP'
        TypeofRightOwner = 'TypeofRightOwner'
        BalanceAccountNumber = 'BalanceAccountNumber'
        date_of_registration_of_another_right = 'date_of_registration_of_another_right'
        inventory_number = 'inventory_number'
        balance_number = 'balance_number'
        CadastralNumber = 'CadastralNumber'
        Date_of_assignment_cadastral = 'Date_of_assignment_cadastral'
        cadastralcost = 'cadastralcost'
        Initial_cost = 'Initial_cost'
        residual_value = 'residual_value'

        historical_Category = 'historical_Category'
        UGROKN_number = 'UGROKN_number'

        KindEncumbrances = 'KindEncumbrances'
        encumbrance_area = 'encumbrance_area'
        encumbrance_cost ='encumbrance_cost'
        person_encumbrance = 'person_encumbrance'
        Other_payments = 'Other_payments'
        start_encumbrance = 'start_encumbrance'
        end_encumbrance = 'end_encumbrance'
        start_use = 'start_use'
        end_use = 'end_use'
        Payment_foruse = 'Payment_foruse'

        # if 'file' not in request.files:
        #     # После перенаправления на страницу загрузки
        #     # покажем сообщение пользователю
        #     flash('Не могу прочитать файл')
        #     print('проблема')
        #     print('проблема',request.url)
        #     return redirect(request.url)
        # foto_main = request.files['formFile']
        # print(foto_main)
        # # Если файл не выбран, то браузер может
        # # отправить пустой файл без имени.
        #
        # if foto_main.filename == '':
        #     print('название фото не может быть пустым', foto_main)
        #
        # if foto_main and allowed_file(foto_main.filename):
        #     # безопасно извлекаем оригинальное имя файла
        #     filename = secure_filename(foto_main.filename)
        #     print(filename)
        #     # сохраняем файл
        #     foto_main.save(os.path.join(config.UPLOAD_FOLDER, filename))
        #     foto_main = "%s/%s" % (config.UPLOAD_FOLDER, filename)
        #
        # # # загрузка мультифото
        # # if 'files[]' not in request.files:
        # #     flash('No file part')
        # #     return redirect(request.url)
        # files = request.files.getlist('files[]')
        # foto_list = []
        # for file in files:
        #     if file and allowed_file(file.filename):
        #         filename = secure_filename(file.filename)
        #         file.save(os.path.join(config.UPLOAD_FOLDER_MULTI, filename))
        #         foto_list.append("%s/%s" % (config.UPLOAD_FOLDER_MULTI, filename))
        # foto_multi = foto_list
        param_request = {'name': name, 'description': description, 'object_type': object_type,
                        'PurposeObject': PurposeObject, 'Condition': Condition,
                        'technicalFloor': technicalFloor,
                        'Lift': Lift, 'remontDate': remontDate, 'SecurityObligation': SecurityObligation,
                        'region': region, 'address': address,
                        # 'foto_scan':foto_scan,
                        'object_area': object_area, 'LandCategory': LandCategory,
                        'TypeOfPermittedUse': TypeOfPermittedUse,
                        'RNFI': RNFI, 'RNFI_date': RNFI_date, 'owner_nomer': owner_nomer,
                        'owner_date': owner_date,
                        'RecordNumberVEGRP': RecordNumberVEGRP, 'DateRecordsVEGRP': DateRecordsVEGRP,
                        'TypeofRightOwner': TypeofRightOwner, 'BalanceAccountNumber': BalanceAccountNumber,
                        'date_of_registration_of_another_right': date_of_registration_of_another_right,
                        'inventory_number': inventory_number, 'balance_number': balance_number,
                        'CadastralNumber': CadastralNumber,
                        'Date_of_assignment_cadastral': Date_of_assignment_cadastral,
                        'cadastralcost': cadastralcost, 'Initial_cost': Initial_cost,
                        'residual_value': residual_value,
                        'historical_Category': historical_Category, 'UGROKN_number': UGROKN_number,
                        'KindEncumbrances': KindEncumbrances,
                        'encumbrance_area': encumbrance_area, 'encumbrance_cost': encumbrance_cost,
                        'person_encumbrance': person_encumbrance, 'Other_payments': Other_payments,
                        'start_encumbrance': start_encumbrance, 'end_encumbrance': end_encumbrance,
                        'start_use': start_use, 'end_use': end_use, 'Payment_foruse': Payment_foruse,
                        # 'foto_main': foto_main, 'foto_multi': foto_multi,
                         'code': 'new_object'
                        }
        print(param_request)
        headers = request.headers.get('access')
        print(headers)
        data = object_card_api_post(param_request, headers)
        # responsePost.encoding = "ANSI"
        context = {'data': data}
        return jsonify(context)

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass


class PodvedAPI(MethodView):

    def get(self):
        param_request = {'page': '1'}
        headers = request.headers.get('access')
        print(headers)
        # берем данные из файла модели
        data = podved_list_api(param_request, headers)
        context = {'data': data}
        return jsonify(context)

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass


class CategoryAPI(MethodView):

    def get(self):
        param_request = {'page': '1'}
        headers = request.headers.get('access')
        print(headers)
        # берем данные из файла модели
        data = category_objects_list_api(param_request, headers)
        context = {'data': data}
        return jsonify(context)

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass


class CardhouseDetailAPI(MethodView):

    def get(self, id):
        param_request = {'code': id}
        headers = request.headers.get('access')
        print('xc')
        # берем данные из файла модели
        data = object_card_api(param_request, headers)
        url = 'http://10.0.0.13:5000/static/site/'
        context = {'data': data, 'url': url}
        return jsonify(context)

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass


class CardhouseAPI(MethodView):

    def get(self, id):
        param_request = {'code': id}
        headers = request.headers.get('access')
        print('xc')
        # берем данные из файла модели
        data = podved_card_api(param_request, headers)
        url = 'http://10.0.0.13:5000/static/site/'
        context = {'data': data, 'url': url}
        return jsonify(context)

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass
